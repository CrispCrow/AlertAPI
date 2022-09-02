# -*- coding: utf-8 -*-
# cython: language_level=3
# Copyright (c) 2022 Crisp Crow
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""Implementation for an event manager."""

from __future__ import annotations

__all__: typing.Sequence[str] = ('EventManagerImpl',)

import asyncio
import typing
import inspect
import json

import attr

from alertapi.impl import event_factory
from alertapi.impl import entity_factory
from alertapi.internal import aio
from alertapi.events import base_events
from alertapi.api import event_manager

if typing.TYPE_CHECKING:
    from aiohttp_sse_client import client as sse_client


@attr.define(weakref_slot=False)
class _Consumer:
    callback: typing.Callable = attr.field(hash=True)
    """The callback function for this consumer."""


class EventManagerBase(event_manager.EventManager):
    __slots__: typing.Sequence[str] = (
        '_listeners',
        '_event_factory',
        '_entity_factory',
        '_consumers'
    )

    def __init__(
        self,
        event_factory: event_factory.EventFactoryImpl,
        entity_factory: entity_factory.EntityFactoryImpl
    ) -> None:
        self._listeners: dict[base_events.Event, typing.Callable] = {}
        self._consumers: dict[str, _Consumer] = {}
        self._event_factory = event_factory
        self._entity_factory = entity_factory

        for name, member in inspect.getmembers(self):
            if name.startswith('on_'):
                event_name = name[3:]
                self._consumers[event_name] = _Consumer(member)

    def _check_event(self, event_type: typing.Type[typing.Any]) -> None:
        try:
            is_event = issubclass(event_type, base_events.Event)
        except TypeError:
            is_event = False

        if not is_event:
            raise TypeError("'event_type' is a non-Event type")

    def subscribe(
        self,
        event_type: typing.Type[base_events.Event],
        callback: typing.Callable
    ) -> None:
        if not inspect.iscoroutinefunction(callback):
            raise TypeError('Cannot subscribe a non-coroutine function callback')

        self._check_event(event_type)

        try:
            self._listeners[event_type].append(callback)
        except KeyError:
            self._listeners[event_type] = [callback]

    def listen(self, event_type: typing.Type[base_events.EventT]) -> typing.Callable:
        def decorator(callback: typing.Callable) -> typing.Callable:
            self.subscribe(event_type, callback)

            return callback

        return decorator

    async def dispatch(self, event: base_events.Event) -> asyncio.Future[typing.Any]:
        tasks: typing.List[typing.Coroutine] = []

        for cls in event.dispatches():
            if listeners := self._listeners.get(cls):
                for callback in listeners:
                    tasks.append(self._invoke_callback(callback, event))

        return asyncio.gather(*tasks) if tasks else aio.completed_future()

    def consume_raw_event(self, event: sse_client.MessageEvent) -> None:
        consumer = self._consumers[event.type]
        asyncio.create_task(
            self._handle_dispatch(consumer, event.data),
            name=f'dispatch {event}'
        )

    async def _invoke_callback(self, callback: typing.Callable, event: base_events.EventT):
        await callback(event)

    async def _handle_dispatch(self, consumer: _Consumer, payload: str) -> None:
        try:
            await consumer.callback(payload)
        except TypeError:
            await consumer.callback()


class EventManagerImpl(EventManagerBase):
    __slots__: typing.Sequence[str] = ()

    def __init__(
        self,
        event_factory: event_factory.EventFactoryImpl,
        entity_factory: entity_factory.EntityFactoryImpl
    ) -> None:
        super().__init__(event_factory=event_factory, entity_factory=entity_factory)

    async def on_hello(self) -> None:
        await self.dispatch(self._event_factory.deserialize_hello_event())

    async def on_update(self, payload: str) -> None:
        json_payload = json.loads(payload)
        state = self._entity_factory.deserialize_state(json_payload['state'])

        await self.dispatch(
            self._event_factory.deserialize_state_update_event(state=state)
        )

    async def on_ping(self) -> None:
        await self.dispatch(self._event_factory.deserialize_ping_event())

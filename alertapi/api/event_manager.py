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
"""Core interface for components that manage events in the library."""

from __future__ import annotations

__all__: typing.Sequence[str] = ('EventManager',)

import typing
import abc

if typing.TYPE_CHECKING:
    import asyncio

    from aiohttp_sse_client import client as sse_client

    from alertapi.events import base_events


class EventManager(abc.ABC):
    """Base interface for event manager implementations.

    This is a listener of a `alertapi.events.base_events.Event` object and
    consumer of raw event payloads, and is expected to invoke one or more
    corresponding event listeners where appropriate.
    """

    __slots__: typing.Sequence[str] = ()

    @abc.abstractmethod
    def subscribe(
        self,
        event_type: typing.Type[base_events.Event],
        callback: typing.Callable
    ) -> None:
        """Subscribe a given callback to a given event type.

        Parameters
        ----------
        event_type : typing.Type[alertapi.events.base_events.Event]
            The event type to listen for. This will also listen for any
            subclasses of the given type.
        callback : typing.Callable
            Must be a coroutine function to invoke. This should
            consume an instance of the given event.

        Example
        -------
        The following demonstrates subscribing a callback to state update event.

        .. code-block :: python

            from alertapi.events.base_events import StateUpdateEvent

            async def on_state_update(event):
                ...

            client.subscribe(StateUpdateEvent, on_state_update)
        """

    @abc.abstractmethod
    def listen(self, event_type: typing.Type[base_events.EventT]) -> typing.Callable:
        """Generate a decorator to subscribe a callback to an event type.

        Parameters
        ----------
        event_type : typing.Type[alertapi.events.base_events.Event]
            The event type to subscribe to.

        Returns
        -------
        typing.Callable
            A decorator for a coroutine function that passes it to
            `EventManager.subscribe` before returning the function
            reference.
        """
        def decorator(callback: typing.Callable) -> typing.Callable:
            self.subscribe(event_type, callback)

            return callback

        return decorator

    @abc.abstractmethod
    async def dispatch(self, event: base_events.Event) -> asyncio.Future[typing.Any]:
        """Dispatch an event.

        Parameters
        ----------
        event : alertapi.events.base_events.Event
            The event to dispatch.

        Returns
        -------
        asyncio.Future[typing.Any]
            A future that can be optionally awaited. If awaited, the future
            will complete once all corresponding event listeners have been
            invoked. If not awaited, this will schedule the dispatch of the
            events in the background for later.
        """

    @abc.abstractmethod
    def consume_raw_event(self, event: sse_client.MessageEvent) -> None:
        """Consume a raw MessageEvent event.

        Parameters
        ----------
        event : aiohttp_sse_client.client.MessageEvent
            The name of the event being triggered.

        Raises
        ------
        builtins.KeyError
            If there is no consumer for the event.
        """

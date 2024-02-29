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
"""Base types for events in Alert API."""

from __future__ import annotations

__all__: typing.Sequence[str] = (
    'Event',
    'ClientConnectedEvent',
    'PingEvent',
    'StateUpdateEvent'
)

import typing
import abc

import attr

if typing.TYPE_CHECKING:
    from alertapi.impl import client
    from alertapi import states


class Event(abc.ABC):
    """Base event type that all AlertAPI events should subclass."""

    __slots__: typing.Sequence[str] = ()

    __dispatches: typing.ClassVar[typing.Tuple[typing.Type[Event], ...]]

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        try:
            Event.__dispatches
        except AttributeError:
            Event.__dispatches = (Event,)

        mro = cls.mro()
        cls.__dispatches = tuple(sub_cls for sub_cls in mro if issubclass(sub_cls, Event))

    @classmethod
    def dispatches(cls) -> typing.Sequence[typing.Type[Event]]:
        """Sequence of the event classes this event is dispatched as."""
        return cls.__dispatches

    @property
    @abc.abstractmethod
    def api(self) -> client.APIClient:
        """App instance for this application.

        Returns
        -------
        alertapi.impl.client.APIClient
            The APIClient app.
        """


EventT = typing.TypeVar('EventT', bound=Event)


@attr.define(kw_only=True, weakref_slot=False)
class ClientConnectedEvent(Event):
    """Event fired when client connected to API SSE endpoint."""

    api: client.APIClient = attr.field()


@attr.define(kw_only=True, weakref_slot=False)
class PingEvent(Event):
    """Event fired when SSE endpoint sends ping packet (every 5 seconds)."""

    api: client.APIClient = attr.field()


@attr.define(kw_only=True, weakref_slot=False)
class StateUpdateEvent(Event):
    """Event fired when one of 25 states has updated."""

    api: client.APIClient = attr.field()
    state: states.State = attr.field()

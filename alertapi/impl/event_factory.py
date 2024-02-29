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
"""Implementation of an event factory for events in Air Raid Alert API."""

from __future__ import annotations

__all__: typing.Sequence[str] = ('EventFactoryImpl',)

import typing
import attr

from alertapi.events import base_events
from alertapi.api import event_factory

if typing.TYPE_CHECKING:
    from alertapi.impl import client
    from alertapi import states


@attr.define(slots=True, frozen=True)
class EventFactoryImpl(event_factory.EventFactory):
    api: client.APIClient = attr.field()

    def deserialize_hello_event(self) -> base_events.ClientConnectedEvent:
        return base_events.ClientConnectedEvent(api=self.api)

    def deserialize_state_update_event(self, state: states.State) -> base_events.StateUpdateEvent:
        return base_events.StateUpdateEvent(api=self.api, state=state)

    def deserialize_ping_event(self) -> base_events.PingEvent:
        return base_events.PingEvent(api=self.api)

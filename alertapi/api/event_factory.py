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
"""Component that provides the ability to generate event models."""

from __future__ import annotations

__all__: typing.Sequence[str] = ('EventFactory',)

import abc
import typing

if typing.TYPE_CHECKING:
    from alertapi.events import base_events
    from alertapi.internal import data_binding


class EventFactory(abc.ABC):
    """Interface for components that deserialize event payloads."""

    @abc.abstractmethod
    def deserialize_hello_event(self) -> base_events.ClientConnectedEvent:
        """Parse hello event payload into client connected object.

        Returns
        -------
        alertapi.events.base_events.ClientConnectedEvent
            The parsed client connected event object.
        """

    @abc.abstractmethod
    def deserialize_state_update_event(self, payload: data_binding.JSONObject) -> base_events.StateUpdateEvent:
        """Parse state update event payload into state update object.

        Parameters
        ----------
        payload : alertapi.internal.data_binding.JSONObject
            JSON payload for deserialize.

        Returns
        -------
        alertapi.events.base_events.StateUpdateEvent
            The parsed state update event object.
        """

    @abc.abstractmethod
    def deserialize_ping_event(self) -> base_events.PingEvent:
        """Parse ping event payload into ping update object.

        Returns
        -------
        alertapi.events.base_events.PingEvent
            The parsed ping update event object.
        """

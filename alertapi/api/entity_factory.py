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
"""Core interface for an object that deserializes API objects."""

from __future__ import annotations

__all__: typing.Sequence[str] = ('EntityFactory',)

import typing
import abc

if typing.TYPE_CHECKING:
    from alertapi.internal import data_binding
    from alertapi import states
    from alertapi import images


class EntityFactory(abc.ABC):
    """Interface for components that deserialize JSON payloads."""

    @abc.abstractmethod
    def deserialize_state(self, payload: data_binding.JSONObject) -> states.State:
        """Parse a raw payload from Alert API into a state object.

        Parameters
        ----------
        payload : alertapi.internal.data_binding.JSONObject
            The JSON payload to deserialize.

        Returns
        -------
        alertapi.states.State
            The deserialized state information object.
        """

    @abc.abstractmethod
    def deserialize_states(self, payload: tuple[data_binding.JSONObject]) -> tuple[states.State]:
        """Parse a tuple of raw payload from Alert API into a state objects.

        Parameters
        ----------
        payload : builtins.tuple[alertapi.internal.data_binding.JSONObject]
            The tuple of JSON payload to deserialize.

        Returns
        -------
        builtins.tuple[alertapi.states.State]
            The tuple of deserialized state information objects.
        """

    @abc.abstractmethod
    def deserialize_image(self, url: str) -> images.Image:
        """Parse a url to static map into Image object.

        Parameters
        ----------
        url : builtins.str

        Returns
        -------
        alertapi.images.Image
            The parsed Image object.
        """

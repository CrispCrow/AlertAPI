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
"""Provides an interface for HTTP-client implementations to follow."""

from __future__ import annotations

__all__: typing.Sequence[str] = ('HTTPClient',)

import typing
import abc

if typing.TYPE_CHECKING:
    from alertapi.internal import routes
    from alertapi.internal import data_binding
    from alertapi import snowflakes
    from alertapi import states


class HTTPClient(abc.ABC):
    """Interface for functionality that a HTTP-client implementation provides.

    Parameters
    ----------
        session : aiohttp.ClientSession
            Session for making API calls
        access_token : builtins.str
            Access token to Alert API.
    """

    __slots__: typing.Sequence[str] = ()

    @abc.abstractmethod
    async def _request(
        self,
        compiled_route: routes.CompiledRoute
    ) -> typing.Optional[typing.Union[data_binding.JSONObject], str]:
        """Method for making HTTP-requests.

        Parameters
        ----------
        compiled_route : alertapi.internal.routes.CompiledRoute

        Returns
        -------
        typing.Optional[typing.Union[alertapi.internal.data_binding.JSONObject], str]
            JSON-object with recieved data or route to static map image.

        Raises
        ------
        alertapi.errors.StateNotFound
            * If specified state does not exists.
        """

    @abc.abstractmethod
    async def fetch_states(
        self,
        with_alert: typing.Union[bool, None], limit: int
    ) -> tuple[states.State]:
        """Fetch all state entities in Alert API.

        Parameters
        ----------
        with_alert : typing.Optional[builtins.bool]
            * If `builtins.True`, returns states with active alarms.
            * If `builtins.False`, returns states with inactive alarms.
        limit : builtins.int
            Limit of states.

        Returns
        -------
        builtins.tuple[alertapi.states.State]
            Tuple of deserialised state objects.
        """

    @abc.abstractmethod
    async def fetch_state(self, state: snowflakes.Snowflake) -> states.State:
        """Fetch state entity.

        Parameters
        ----------
        state : alertapi.snowflakes.Snowflake
            State for search.

        Returns
        -------
        alertapi.states.State
            Deserialied state object.
        """

    @abc.abstractmethod
    async def is_alert(self, state: snowflakes.Snowflake) -> bool:
        """Check is active alert in specified state.

        Parameters
        ----------
        state : alertapi.snowflakes.Snowflake
            State for search.

        Returns
        -------
        builtins.bool
            * `builtins.True` if alert is active.
            * `builtins.False` if alert is inactive.
        """

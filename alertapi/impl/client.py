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
"""Alert API client module."""

from __future__ import annotations

__all__: typing.Sequence[str] = ('Client',)

import typing

import aiohttp

from alertapi.impl import http
from alertapi.internal import converters

if typing.TYPE_CHECKING:
    from alertapi.internal.converters import StateConverter
    from alertapi import snowflakes
    from alertapi import states


class Client:
    """Alert API client.

    This is the class, you will want to create Alert API client.

    Parameters
    ----------
    session : aiohttp.ClientSession
        Session for making API calls.
    access_token : builtins.str
        An access token to the Air Raid Alert API.
        Can be obtained from https://alerts.com.ua

    Example
    -------
        .. code-block:: python
            import os
            import asyncio

            import alertapi
            import aiohttp


            async def main() -> None:
                async with aiohttp.ClientSession() as session:
                    client = alertapi.Client(session=session, access_token='...')
                    print(await client.fetch_states())


            loop = asyncio.get_event_loop()
            loop.run_until_complete(main)
    """

    __slots__: typing.Sequence[str] = (
        '_session',
        '_access_token',
        '_http',
        '_state_converter'
    )

    def __init__(self, session: aiohttp.ClientSession, access_token: str) -> None:
        self._access_token = access_token
        self._http = http.HttpClientImpl(session, access_token)
        self._state_converter = converters.StateConverter()

    @property
    def access_token(self) -> str:
        return self._access_token

    @typing.overload
    async def fetch_states(self, state: snowflakes.Snowflake) -> states.State:
        ...

    @typing.overload
    async def fetch_states(self, with_alert: bool) -> tuple[states.State]:
        ...

    @typing.overload
    async def fetch_states(self, limit: int) -> tuple[states.State]:
        ...

    async def fetch_states(
        self,
        state: typing.Optional[snowflakes.Snowflake] = None,
        with_alert: typing.Optional[bool] = None,
        limit: typing.Optional[int] = 25
    ) -> tuple[states.State]:
        """Fetch all state entities from Alert API.

        Parameters
        ----------
        state : typing.Optional[alertapi.snowflakes.Snowflake]
            State for search. If specified,
            returns state object with information.
        with_alert : typing.Optional[builtins.bool]
            Fetch states with active/inactive alert.
        limit : typing.Optional[builtins.int]
            Limit of states. Defaults to 25.

        Returns
        -------
        alertapi.states.State
            Deserialied state entity if state is specified.
        builtins.tuple[alertapi.states.State]
            Tuple of deserialised state entities.

        Raises
        ------
        alertapi.errors.StateNotFound
            * If specified state does not exists.
        """
        if state:
            return await self.fetch_state(state)

        return await self._http.fetch_states(with_alert=with_alert, limit=limit)

    async def fetch_state(
        self,
        state: typing.Union[
            typing.Literal[StateConverter.STATES], snowflakes.Snowflake
        ]
    ) -> states.State:
        """Fetch state entity from Alert API

        Parameters
        ----------
        state : typing.Union[typing.Literal[alertapi.internal.converters.StateConverter.STATES], alertapi.snowflakes.Snowflake]
            State for search.

        Returns
        -------
        alertapi.states.State
            Deserialied state entity.

        Raises
        ------
        alertapi.errors.StateNotFound
            * If specified state does not exists.
        """
        if isinstance(state, str):
            state = self._state_converter.convert(state)

        return await self._http.fetch_state(state=state)

    async def is_alert(
        self,
        state: typing.Union[
            typing.Literal[StateConverter.STATES], snowflakes.Snowflake
        ]
    ) -> bool:
        """Check whether active alert in specified state or not.

        Parameters
        ----------
        state : typing.Union[typing.Literal[alertapi.internal.converters.StateConverter.STATES], alertapi.snowflakes.Snowflake]
            State for search.

        Returns
        -------
        builtins.bool
            * `builtins.True` if alert is active.
            * `builtins.False` if alert is inactive.

        Raises
        ------
        alertapi.errors.StateNotFound
            * If specified state does not exists.
        """
        if isinstance(state, str):
            state = self._state_converter.convert(state)

        return await self._http.is_alert(state=state)

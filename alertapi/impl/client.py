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
"""Air Raid Alert API client module."""

from __future__ import annotations

__all__: typing.Sequence[str] = ('APIClient', 'GatewayClient')

import asyncio
import typing

import aiohttp
from aiohttp_sse_client import client as sse_client

from alertapi.impl import http
from alertapi.impl import event_manager
from alertapi.impl import event_factory
from alertapi.impl import entity_factory
from alertapi.internal import converters
from alertapi.internal import routes

if typing.TYPE_CHECKING:
    from alertapi.internal.converters import StateConverter
    from alertapi.events import base_events
    from alertapi import snowflakes
    from alertapi import states
    from alertapi import images


class APIClient:
    """Alert API client.

    Api client for Air Raid Alert API.

    Parameters
    ----------
    access_token : builtins.str
        An access token to the Air Raid Alert API.
        Can be obtained `here <https://alerts.com.ua>`_

    Example
    -------
        .. code-block:: python

            import asyncio

            import alertapi


            async def main() -> None:
                client = alertapi.APIClient(access_token='...')
                print(await client.fetch_states())


            loop = asyncio.get_event_loop()
            loop.run_until_complete(main())
    """

    __slots__: typing.Sequence[str] = (
        '_session',
        '_access_token',
        '_http',
        '_state_converter'
    )

    def __init__(self, access_token: str) -> None:
        self._access_token = access_token
        self._session = aiohttp.ClientSession
        self._http = http.HttpClientImpl(access_token, self._session)
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
        state : typing.Union[typing.Literal[converters.StateConverter.STATES], snowflakes.Snowflake]
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
        state : typing.Union[typing.Literal[converters.StateConverter.STATES], snowflakes.Snowflake]
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

    async def static_map(self) -> images.Image:
        """Fetch static map of states.

        Returns
        -------
        alertapi.images.Image
            Deserialized Image object.
        """
        return await self._http.fetch_static_map()


class GatewayClient:
    """Gateway Alert API client.

    Parameters
    ----------
    access_token : builtins.str
        An access token to the Air Raid Alert API.
        Can be obtained `here <https://alerts.com.ua>`_

    Example
    -------
    .. code-block:: python

        import alertapi

        client = alertapi.GatewayClient(access_token='...')


        @client.listen(alertapi.ClientConnectedEvent)
        async def on_client_connected(event: alertapi.ClientConnectedEvent) -> None:
            states = await event.api.fetch_states()
            print(states)


        @client.listen(alertapi.StateUpdateEvent)
        async def on_state_update(event: alertapi.StateUpdateEvent) -> None:
            print('State updated': event.state)


        client.connect()
    """

    __slots__: typing.Sequence[str] = (
        '_access_token',
        '_event_source',
        '_client',
        '_event_factory',
        '_entity_factory',
        '_event_manager',
        '_loop'
    )

    def __init__(self, access_token: str) -> None:
        self._access_token = access_token
        self._event_source = sse_client.EventSource
        self._client = APIClient(access_token=self._access_token)
        self._event_factory = event_factory.EventFactoryImpl(self._client)
        self._entity_factory = entity_factory.EntityFactoryImpl()
        self._event_manager = event_manager.EventManagerImpl(self._event_factory, self._entity_factory)
        self._loop = asyncio.get_event_loop()

    @property
    def access_token(self) -> str:
        return self._access_token

    @property
    def loop(self) -> str:
        return self._loop

    @property
    def entity_factory(self) -> entity_factory.EntityFactoryImpl:
        return self._entity_factory

    @property
    def event_factory(self) -> event_factory.EventFactoryImpl:
        return self._event_factory

    @property
    def client(self) -> APIClient:
        return self._client

    def connect(self) -> None:
        """Connect client to Air Raid Alert API endpoint."""

        compiled_route = routes.SSE_LIVE.compile()
        url = compiled_route.create_url(routes.BASE_URL)
        headers = {'X-API-Key': self._access_token}

        self._loop.run_until_complete(self._listen_event_source(url, headers))

    async def _listen_event_source(self, url: str, headers: dict[str, typing.Any]) -> None:
        """Connect to SSE endpoint and listen events.

        Parameters
        ----------
        url : builtins.str
            Url to endpoint.
        headers : builtins.dict[builtins.str, typing.Any]
            Headers for HTTP-request body.
        """
        async with self._event_source(url, timeout=None, headers=headers) as event_source:
            async for event in event_source:
                self._event_manager.consume_raw_event(event)

    def listen(self, event_type: typing.Type[base_events.Event]) -> typing.Callable:
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
        return self._event_manager.listen(event_type)

    def subscribe(self, event_type: typing.Type[base_events.Event], callback: typing.Callable) -> None:
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
        self._event_manager.subscribe(event_type, callback)

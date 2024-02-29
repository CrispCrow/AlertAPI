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
"""Implementation of a HTTP-client for Air Raid Alert API."""

from __future__ import annotations

__all__: typing.Sequence[str] = ('HttpClientImpl',)

import typing

import aiohttp

from alertapi.api import http
from alertapi.impl import entity_factory
from alertapi.internal import routes
from alertapi import errors

if typing.TYPE_CHECKING:
    from alertapi.internal import data_binding
    from alertapi import snowflakes
    from alertapi import states
    from alertapi import images


class HttpClientImpl(http.HTTPClient):
    __slots__: typing.Sequence[str] = (
        '_session',
        '_access_token',
        '_entity_factory',
        '_api_url'
    )

    def __init__(self, access_token: str, session: aiohttp.ClientSession) -> None:
        self._access_token = access_token
        self._session = session
        self._entity_factory = entity_factory.EntityFactoryImpl()
        self._api_url = routes.BASE_URL

    async def _request(
        self, compiled_route: routes.CompiledRoute
    ) -> typing.Optional[typing.Union[data_binding.JSONObject], str]:
        headers = {'X-API-Key': self._access_token}
        url = compiled_route.create_url(self._api_url)

        async with self._session() as session:
            response = await session.request(
                compiled_route.method,
                url,
                headers=headers
            )
            response.raise_for_status()

            if compiled_route.compiled_path.endswith('.png'):
                return response.url
            json_payload = await response.json()

            if not (json_payload.get('state') or json_payload.get('states')):
                raise errors.StateNotFound(f'Route with state {compiled_route.compiled_path} has not found.')
            return json_payload

    async def fetch_states(
        self, with_alert: typing.Union[bool, None], limit: int
    ) -> tuple[states.State]:
        route = routes.GET_STATES.compile()
        response = (await self._request(route))['states']

        if isinstance(with_alert, bool):
            response = tuple(filter(
                lambda state: state['alert'] is with_alert, response
            ))
        return self._entity_factory.deserialize_states(response[:limit])

    async def fetch_state(self, state: snowflakes.Snowflake) -> states.State:
        route = routes.GET_STATE.compile(state=state)
        response = await self._request(route)

        return self._entity_factory.deserialize_state(response['state'])

    async def is_alert(self, state: snowflakes.Snowflake) -> bool:
        route = routes.GET_STATE.compile(state=state)
        response = await self._request(route)

        return response['state']['alert']

    async def fetch_static_map(self) -> images.Image:
        route = routes.GET_STATIC_MAP.compile()
        response = await self._request(route)

        return self._entity_factory.deserialize_image(response)

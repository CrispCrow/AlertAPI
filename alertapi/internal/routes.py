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
"""Provides the valid routes that can be used on the API."""

from __future__ import annotations

__all__: typing.Sequence[str] = ('CompiledRoute', 'Route')

import typing

import attr


@attr.define(slots=True, frozen=True)
@typing.final
class CompiledRoute:
    route: Route = attr.field()
    compiled_path: str = attr.field()

    @property
    def method(self) -> str:
        return self.route.method

    def create_url(self, base_url: str) -> str:
        return base_url + self.compiled_path

    def __str__(self) -> str:
        return f'{self.method} {self.compiled_path}'


@attr.define(slots=True)
@typing.final
class Route:
    method: str = attr.field()
    path_template: str = attr.field()

    def compile(self, **kwargs: typing.Any) -> CompiledRoute:
        return CompiledRoute(
            route=self,
            compiled_path=self.path_template.format_map(kwargs)
        )


# HTTP METHOD
GET: typing.Final[str] = 'GET'

# BASIC URL
BASE_URL: typing.Final[str] = 'https://alerts.com.ua'

# STATES
GET_STATES: typing.Final[Route] = Route(GET, '/api/states')
GET_STATE: typing.Final[Route] = Route(GET, '/api/states/{state}')

# STATIC MAP
GET_STATIC_MAP: typing.Final[Route] = Route(GET, '/map.png')

# SSE ENDPOINT
SSE_LIVE: typing.Final[Route] = Route(GET, '/api/states/live')

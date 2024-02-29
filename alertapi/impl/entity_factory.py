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
"""Implementation of an entity factory for entities in Air Raid Alert API."""

from __future__ import annotations

__all__: typing.Sequence[str] = ('EntityFactoryImpl',)

import typing

from alertapi.api import entity_factory
from alertapi import snowflakes
from alertapi import states
from alertapi import images

if typing.TYPE_CHECKING:
    from alertapi.internal import data_binding


class EntityFactoryImpl(entity_factory.EntityFactory):
    def deserialize_state(self, payload: data_binding.JSONObject) -> states.State:
        return states.State(
            id=snowflakes.Snowflake(payload['id']),
            name=payload['name'],
            name_en=payload['name_en'],
            alert=payload['alert'],
            changed=payload['changed']
        )

    def deserialize_states(
        self, payload: tuple[data_binding.JSONObject]
    ) -> tuple[states.State]:
        return tuple(map(self.deserialize_state, payload))

    def deserialize_image(self, url: str) -> images.Image:
        return images.Image(url)

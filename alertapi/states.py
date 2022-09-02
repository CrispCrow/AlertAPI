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
"""Entities that are used to describe states on Air Raid Alert API."""

from __future__ import annotations

__all__: typing.Sequence[str] = ('State',)

import typing

import attr

if typing.TYPE_CHECKING:
    import datetime

    from alertapi import snowflakes


@attr.define(slots=True, frozen=True)
class State:
    """Interface of state information.

    Attributes
    ----------
    id : alertapi.snowflakes.Snowflake
        State identificator.
    name : builtins.str
        Ukrainian state name.
    name_en : builtins.str
        English state name.
    alert : builtins.bool
        Alert status in state.
    changed : typing.Literal[datetime.datetime]
        Last changes of state.
    """

    id: snowflakes.Snowflake = attr.field()
    name: str = attr.field()
    name_en: str = attr.field()
    alert: bool = attr.field()
    changed: typing.Literal[datetime.datetime] = attr.field()

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
"""Converter utilities."""

from __future__ import annotations

__all__: typing.Sequence[str] = ('StateConverter',)

import typing

from alertapi import snowflakes
from alertapi import errors


class StateConverter:
    """State converter.

    Using for converting state name to state id.
    """
    STATES: typing.Final[dict[str, snowflakes.Snowflake]] = {
        'Vinnytsia oblast': snowflakes.Snowflake(1),
        'Volyn oblast': snowflakes.Snowflake(2),
        'Dnipropetrovsk oblast': snowflakes.Snowflake(3),
        'Donetsk oblast': snowflakes.Snowflake(4),
        'Zhytomyr oblast': snowflakes.Snowflake(5),
        'Zakarpattia oblast': snowflakes.Snowflake(6),
        'Zaporizhzhia oblast': snowflakes.Snowflake(7),
        'Ivano-Frankivsk oblast': snowflakes.Snowflake(8),
        'Kyiv oblast': snowflakes.Snowflake(9),
        'Kirovohrad oblast': snowflakes.Snowflake(10),
        'Luhansk oblast': snowflakes.Snowflake(11),
        'Lviv oblast': snowflakes.Snowflake(12),
        'Mykolaiv oblast': snowflakes.Snowflake(13),
        'Odesa oblast': snowflakes.Snowflake(14),
        'Poltava oblast': snowflakes.Snowflake(15),
        'Rivne oblast': snowflakes.Snowflake(16),
        'Sumy oblast': snowflakes.Snowflake(17),
        'Ternopil oblast': snowflakes.Snowflake(18),
        'Kharkiv oblast': snowflakes.Snowflake(19),
        'Kherson oblast': snowflakes.Snowflake(20),
        'Khmelnytskyi oblast': snowflakes.Snowflake(21),
        'Cherkasy oblast': snowflakes.Snowflake(22),
        'Chernivtsi oblast': snowflakes.Snowflake(23),
        'Chernihiv oblast': snowflakes.Snowflake(24),
        'Kyiv': snowflakes.Snowflake(25)
    }

    def convert(self, state: str) -> snowflakes.Snowflake:
        """Convert name variation of state to his identificator.

        Parameters
        ----------
        state : builtins.str
            Name of state.

        Returns
        -------
        alertapi.snowflakes.Snowflake
            Snowflake representation of state.
        """
        try:
            return StateConverter.STATES[state]
        except KeyError:
            raise errors.StateNotFound(f'State with name {state!r} does not exists.')

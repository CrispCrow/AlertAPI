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
"""Asyncio extensions and utilities."""

from __future__ import annotations

__all__: typing.Sequence[str] = ('completed_future',)

import asyncio
import typing

T_inv = typing.TypeVar('T_inv')


def completed_future(result: typing.Optional[T_inv] = None, /) -> asyncio.Future[typing.Optional[T_inv]]:
    """Create a future on the current running loop that is completed, then return it.

    Parameters
    ----------
    result : T
        The value to set for the result of the future.
        `T` is a generic type placeholder for the type that
        the future will have set as the result. `T` may be `builtins.None`, in
        which case, this will return `asyncio.Future[builtins.None]`.

    Returns
    -------
    asyncio.Future[T]
        The completed future.

    Raises
    ------
    RuntimeError
        When called in an environment with no running event loop.
    """

    future = asyncio.get_running_loop().create_future()
    future.set_result(result)
    return future

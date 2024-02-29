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

import os
import re
import types

import setuptools


def long_description():
    with open('README.md') as file:
        return file.read()


def parse_meta():
    with open(os.path.join('alertapi', '_about.py')) as fp:
        code = fp.read()

    token_pattern = re.compile(r"^__(?P<key>\w+)?__.*=\s*(?P<quote>(?:'{3}|\"{3}|'|\"))(?P<value>.*?)(?P=quote)", re.M)

    groups = {}

    for match in token_pattern.finditer(code):
        group = match.groupdict()
        groups[group['key']] = group['value']

    return types.SimpleNamespace(**groups)

metadata = parse_meta()

setuptools.setup(
    name=metadata.name,
    version=metadata.version,
    description=metadata.description,
    long_description=long_description(),
    long_description_content_type='text/markdown',
    author=metadata.author,
    author_email=metadata.email,
    license=metadata.license,
    url=metadata.url,
    python_requires='>=3.8',
    packages=setuptools.find_namespace_packages(include=['alertapi*']),
    install_requires=['attrs==21.4.0', 'aiohttp==3.8.4', 'aiohttp-sse-client==0.2.1'],
    include_package_data=True,
    zip_safe=False,
    project_urls={
        'Source (GitHub)': metadata.url,
        'Issue Tracker': metadata.issue_tracker,
    },
    classifiers=[
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: Implementation :: CPython',
    'Natural Language :: English',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
    ]
)

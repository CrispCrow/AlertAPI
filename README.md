<h1 align="center">AlertAPI</h1>
<p>
Static typed Air Raid Alert API wrapper for Python3.

Python 3.8+ are currently supported.
</p>

## Installation
Install AlertAPI from PyPi with the following command:

```bash
python -m pip install -U alertapi
# Windows users may need to use this instead...
py -3 -m pip install -U alertapi
```

----

## Updating

```bash
pip install --upgrade alertapi
```

----

## Start up client

```py
import asyncio

import aiohttp
import alertapi


async def main() -> None:
    async with aiohttp.ClientSession() as session:
        client = alertapi.Client(session=session, access_token='...')
        print(await client.fetch_states())


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

----

## Example

```py
import asyncio

import aiohttp
import alertapi


async def main() -> None:
    async with aiohttp.ClientSession() as session:
        client = alertapi.Client(session=session, access_token='...')

        print('State list:', await client.fetch_states())
        print('First 5 active alerts:', await client.fetch_states(with_alert=True, limit=5))
        print('Inactive alerts:', await client.fetch_states(with_alert=False))
        print('Kyiv info:', await client.fetch_state(25))
        print('Kyiv info:', await client.fetch_state('Kyiv'))
        print('Is active alert in Lviv oblast:', await client.is_alert('Lviv oblast'))


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

----

## Python optimization flags
CPython provides two optimisation flags that remove internal safety checks that are useful for development, and change other internal settings in the interpreter.

- python main.py - no optimisation - this is the default.
- python -O main.py - first level optimisation - features such as internal
    assertions will be disabled.
- python -OO main.py - second level optimisation - more features (**including
    all docstrings**) will be removed from the loaded code at runtime.

**A minimum of first level of optimizations** is recommended when running applications in a production environment.
<h1 align="center">AlertAPI</h1>
<p>
Async and static typed Air Raid Alert microframework for Python3.

Python 3.8, 3.9 and 3.10 are currently supported.
</p>

## Installation
Install AlertAPI from PyPi with the following command:

```bash
pip install alertapi
```

----

## Updating

```bash
pip install --upgrade alertapi
```

----

## Start up basic API client

```py
import asyncio

import alertapi


async def main() -> None:
    client = alertapi.APIClient(access_token='...')
    print(await client.fetch_states())


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

----

## Example

```py
import asyncio

import alertapi


async def main() -> None:
    client = alertapi.APIClient(access_token='...')

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

## On run GatewayClient 

```py
import alertapi

client = alertapi.GatewayClient(access_token='...')


@client.listen(alertapi.ClientConnectedEvent)
async def on_client_connected(event: alertapi.ClientConnectedEvent) -> None:
    states = await event.api.fetch_states()
    print(states)


@client.listen(alertapi.PingEvent)
async def on_ping(event: alertapi.PingEvent) -> None:
    print('Ping event')


@client.listen(alertapi.StateUpdateEvent)
async def on_state_update(event: alertapi.StateUpdateEvent) -> None:
    print('State updated:', event.state)


client.connect()
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
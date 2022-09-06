Getting started
===============

Installation
------------
Install AlertAPI from PyPi with the following command:

.. code-block :: bash

	pip install alertapi

----

Updating
--------

.. code-block :: bash

	pip install --upgrade alertapi


----

Start up basic API client
-------------------------

.. code-block :: python

	import asyncio

	import alertapi


	async def main() -> None:
	    client = alertapi.APIClient(access_token='...')
	    print(await client.fetch_states())


	loop = asyncio.get_event_loop()
	loop.run_until_complete(main())

----

Example
-------

.. code-block :: python

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

----

Or run GatewayClient
----

.. code-block :: python

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

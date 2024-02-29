import asyncio

import alertapi


async def main() -> None:
    client = alertapi.Client(access_token='...')

    print('State list:', await client.fetch_states())
    print('First 5 active alerts:', await client.fetch_states(with_alert=True, limit=5))
    print('Inactive alerts:', await client.fetch_states(with_alert=False))
    print('Kyiv info:', await client.fetch_state(25))
    print('Kyiv info:', await client.fetch_state('Kyiv'))
    print('Is active alert in Lviv oblast:', await client.is_alert('Lviv oblast'))


loop = asyncio.get_event_loop()
loop.run_until_complete(main())

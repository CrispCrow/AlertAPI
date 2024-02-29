import alertapi

client = alertapi.GatewayClient(access_token='...')


@client.listen(alertapi.ClientConnectedEvent)
async def on_client_connected(event: alertapi.ClientConnectedEvent) -> None:
    states = await event.app.fetch_states()
    print(states)


@client.listen(alertapi.PingEvent)
async def on_ping(event: alertapi.PingEvent) -> None:
    print('Ping event')


@client.listen(alertapi.StateUpdateEvent)
async def on_state_update(event: alertapi.StateUpdateEvent) -> None:
    print('State updated:', event.state)


client.connect()
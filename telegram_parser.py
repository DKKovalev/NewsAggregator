from telethon import TelegramClient, events, version
from secrets import secrets


def telegram_parser(send_message_func=None, loop=None):
    api_id = secrets.get('TELEGRAM_API_TOKEN')
    api_hash = secrets.get('TELEGRAM_API_HASH')

    session_name = 'News Aggregation'

    device_version = secrets.get('DEVICE_VERSION')

    client = TelegramClient(
        session=session_name,
        api_id=api_id,
        api_hash=api_hash,
        loop=loop,
        system_version=device_version,
        device_model='News Aggregation Bot',
        app_version=version.__version__
    )
    client.start()

    channel_sources = [
        'https://t.me/IAechosevera',
        'https://t.me/infoarch',
        'https://t.me/nnnewsch'
    ]

    @client.on(events.NewMessage(chats=channel_sources))
    async def handler(event):
        channel = await event.get_chat()
        channel_name = channel.title if channel.title else 'Неизвестный канал'
        message = event.raw_text
        print(event.raw_text, '\n')

        formatted_message = f"**{channel_name}**\n{message}"

        await send_message_func(f"'{formatted_message}'")

    return client


if __name__ == "__main__":
    client = telegram_parser()
    client.run_until_disconnected()


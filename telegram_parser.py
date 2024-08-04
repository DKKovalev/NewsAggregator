from telethon import TelegramClient, events, version

from config_loader import ConfigLoader


def telegram_parser(send_message_func=None, loop=None):
    config_loader = ConfigLoader('config.yaml')
    config = config_loader.get_config()

    secrets = config.get('secrets', {})
    telegram_channels = config.get('telegram_channels', [])
    vk_channels = config.get('vk_channels', [])

    api_id = secrets.get('TELEGRAM_API_TOKEN')
    api_hash = secrets.get('TELEGRAM_API_HASH')

    session_name = 'News Aggregation'

    device_version = secrets.get('DEVICE_VERSION')

    print(f"Secrets: {secrets}")
    print(f"Telegram Channels: {telegram_channels}")
    print(f"VK Channels: {vk_channels}")

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

    @client.on(events.NewMessage(chats=telegram_channels))
    async def handler(event):
        channel = await event.get_chat()
        channel_name = channel.title if channel.title else 'Неизвестный канал'
        channel_url = f"https://t.me/{channel.username}"
        message = event.raw_text

        print(f"Hello, im working here")

        print(event.raw_text, '\n')

        formatted_message = f"**{channel_name}**\n{message}"

        data = {
            'from': 'Telegram',
            'channel_name': channel_name,
            'channel_url': channel_url,
            'post_text': message
        }

        await send_message_func(data)

    return client


if __name__ == "__main__":
    client = telegram_parser()
    client.run_until_disconnected()

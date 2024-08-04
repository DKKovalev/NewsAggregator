import asyncio

from config_loader import ConfigLoader
from telegram_parser import telegram_parser
from vk_parser import create_vk_parser

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

config_loader = ConfigLoader('config.yaml')
config = config_loader.get_config()

secrets = config.get('secrets', {})

telegram_api_id = secrets.get('TELEGRAM_API_ID')
telegram_api_hash = secrets.get('TELEGRAM_API_HASH')
device_version = secrets.get('DEVICE_VERSION')
telegram_channels = config.get('telegram_channels', [])

vk_api_token = secrets.get('VK_API_TOKEN')
vk_channels = config.get('vk_channels', [])

target_telegram_channel_url = secrets.get('TARGET_TELEGRAM_CHANNEL_URL')


async def send_message_func(message):
    channel_name = message.get('channel_name')
    channel_url = message.get('channel_url')
    channel_message = message.get('post_text')

    formatted_message = f"**{channel_name}** ({channel_url})\n\n{channel_message}"

    await telegram_client.send_message(entity=target_telegram_channel_url, message=formatted_message)


# Создаем клиенты для Telegram и VK
telegram_client = telegram_parser(send_message_func=send_message_func, loop=loop)
vk_client = create_vk_parser(vk_api_token, vk_channels, send_message_func)

# Запускаем оба клиента
loop.create_task(vk_client)
telegram_client.run_until_disconnected()
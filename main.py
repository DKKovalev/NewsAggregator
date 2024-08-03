import asyncio

import secrets
from telegram_parser import telegram_parser

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

target_channel = secrets.secrets.get('TARGET_TELEGRAM_CHANNEL_URL')

async def send_message_func(message):
    await telegram_client.send_message(entity=target_channel, message=message)


telegram_client = telegram_parser(send_message_func=send_message_func, loop=loop)
telegram_client.run_until_disconnected()

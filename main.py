import asyncio
from aiogram import Bot, Dispatcher, executor, types
from telethon import TelegramClient
from telethon.sessions import StringSession

from config import BOT_API_TOKEN, SESSION_TOKEN, CHANNEL_ENTITY
from utils.message_tools import get_messages
bot = Bot(token=BOT_API_TOKEN)
dp = Dispatcher(bot)
client = TelegramClient(StringSession(SESSION_TOKEN),
                        15580631, "f2aad44cd49a6d10f05d2e9d84ea23a0",
                        device_model="Lenovo S340",
                        system_version="32x-amd",
                        app_version="0.0.4 beta")
client.start()


async def run():
    await get_messages(bot=bot, client=client, channel_entity=CHANNEL_ENTITY)
    print("All messages edited.")

asyncio.get_event_loop().run_until_complete(run())

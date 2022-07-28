import asyncio
from typing import Union

from aiogram import Bot
from telethon import TelegramClient
from telethon.tl.types import Message

from config import MESSAGE_FOR_REMOVE, MESSAGE_FOR_SET


async def get_messages(bot: Bot, client: TelegramClient, channel_entity: Union[str | int]) -> None:
    """function for get entity channel by id"""
    async for message in client.iter_messages(channel_entity, reverse = True):
        await change_text(bot=bot, message=message)


async def change_text(bot: Bot, message: Message) -> None:
    """function send request api for change message in channel"""
    async with await bot.get_session():
        try:
            channel_id = message.peer_id.channel_id
            if hasattr(message,'media'):
                if message.media is not None:
                    await bot.edit_message_caption(chat_id=f"-100{channel_id}",
                                                   message_id=message.id,
                                                   caption=replace_text(
                                                       message_text=message.message,
                                                       bad_word=MESSAGE_FOR_REMOVE,
                                                       set_word=MESSAGE_FOR_SET
                                                   )
                                                   )
                else:
                    await bot.edit_message_text(chat_id=f"-100{channel_id}",
                                               message_id=message.id,
                                               text=replace_text(
                                                   message_text=message.message,
                                                   bad_word=MESSAGE_FOR_REMOVE,
                                                   set_word=MESSAGE_FOR_SET
                                               )
                                               )
            print(f"Message with id {message.id} successfully edited.")
        except Exception as e:
            print(f"Error by level with change_text function: {e}")
            print(message)
        finally:
            session = await bot.get_session()
            await session.close()
        await asyncio.sleep(10)


def replace_text(message_text: str, bad_word: str, set_word: str) -> str:
    """function for replace bad words with good"""
    return message_text.replace(bad_word, set_word)

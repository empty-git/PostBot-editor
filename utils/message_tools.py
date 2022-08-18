import asyncio
from typing import Union

from aiogram import Bot
from telethon import TelegramClient
from telethon.tl.types import Message
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from config import MESSAGE_FOR_REMOVE, MESSAGE_FOR_SET


async def get_messages(bot: Bot, client: TelegramClient, channel_entity: Union[str | int]) -> None:
    """function for get entity channel by id"""
    async for message in client.iter_messages(channel_entity, reverse = False):
        await change_keyboard(bot=bot, message=message)

async def change_keyboard(bot: Bot, message: Message) -> None:
    async with await bot.get_session():
        try:
            channel_id = message.peer_id.channel_id
            if hasattr(message,'media'):
                url_keyboard = InlineKeyboardMarkup(row_width=2)
                url_keyboard.add(InlineKeyboardButton('Больше новостей ✅', url='https://t.me/hub_404'))
                url_keyboard.add(InlineKeyboardButton('Хочешь заказать рекламу?  📈', url='https://t.me/contact_alisa'))
                if message.media is not None:
                    await bot.edit_message_reply_markup(chat_id=f"-100{channel_id}",
                                                   message_id=message.id,
                                                   reply_markup = url_keyboard
                                                   )
                else:
                    await bot.edit_message_reply_markup(chat_id=f"-100{channel_id}",
                                               message_id=message.id,
                                               reply_markup = url_keyboard
                                               )
            print(f"Message with id {message.id} successfully edited.")
        except Exception as e:
            print(f"Error by level with change_text function: {e}")
            print(message)
        finally:
            session = await bot.get_session()
            await session.close()
        await asyncio.sleep(10)

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

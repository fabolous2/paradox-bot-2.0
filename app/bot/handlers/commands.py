import os
from typing import Union

from aiogram import Router, Bot, F
from aiogram.filters import CommandStart
from aiogram.types import Message, Chat, CallbackQuery, FSInputFile

from app.bot.keyboards import inline


router = Router()


@router.message(CommandStart())
async def start_handler(
    message: Message,
    bot: Bot,
    event_chat: Chat,
) -> None:
    await bot.send_photo(
        photo=FSInputFile(os.path.normpath("app/bot/files/paradox.jpg")),
        chat_id=event_chat.id,
        caption="🛍 <a href='https://t.me/loudly_club1'>Paradox Shop</a> - сервис внутриигровых покупок и услуг!\n\n🔰 Наш приоритет дать возможность купить любую игровую валюту по лучшим ценам, а также предоставить вам скорейшее получение доната с гарантией безопасности вашего аккаунта",
        reply_markup=inline.main_keyboard_markup,
    )

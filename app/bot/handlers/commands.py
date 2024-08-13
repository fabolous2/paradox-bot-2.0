import os

from aiogram import Router, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, Chat, FSInputFile

from dishka import FromDishka

from src.bot.app.bot.keyboards import inline
from src.services import UserService


router = Router()


@router.message(CommandStart())
async def start_handler(
    message: Message,
    bot: Bot,
    event_chat: Chat,
    user_service: FromDishka[UserService],
) -> None:
    user_id = message.from_user.id
    exists = await user_service.exists(user_id=user_id)
    if not exists:
        await user_service.add_user(
            user_id=user_id,
            referral_code=str(user_id),
        )
        
    await bot.send_photo(
        photo=FSInputFile(os.path.normpath("src/bot/app/bot/files/paradox.jpg")),
        chat_id=event_chat.id,
        caption="🛍 <a href='https://t.me/loudly_club1'>Paradox Shop</a> - сервис внутриигровых покупок и услуг!\n\n🔰 Наш приоритет дать возможность купить любую игровую валюту по лучшим ценам, а также предоставить вам скорейшее получение доната с гарантией безопасности вашего аккаунта",
        reply_markup=inline.main_keyboard_markup,
    )

import os

from aiogram import Router, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, Chat, FSInputFile, ReplyKeyboardRemove

from dishka import FromDishka

from src.bot.app.bot.keyboards import inline
from src.services import UserService
from src.main.config import settings


router = Router()


@router.message(CommandStart())
async def start_handler(
    message: Message,
    bot: Bot,
    event_chat: Chat,
    user_service: FromDishka[UserService],
) -> None:
    await bot.send_photo(
        photo=FSInputFile(os.path.normpath("src/bot/app/bot/files/paradox.jpg")),
        chat_id=event_chat.id,
        caption="🛍 <a href='https://t.me/loudly_club1'>Paradox Shop</a> - сервис внутриигровых покупок и услуг!\n\n🔰 Наш приоритет дать возможность купить любую игровую валюту по лучшим ценам, а также предоставить вам скорейшее получение доната с гарантией безопасности вашего аккаунта",
        reply_markup=inline.main_keyboard_markup,
    )

    exists = await user_service.exists(user_id=message.from_user.id)
    if not exists:
        reffer_id = None
        start_command = message.text   
        if len(start_command) >= 7:
            reffer_id = start_command[7:] if start_command[7:].isdigit() else None
            reffer_id = reffer_id[4:]

        user_photos = await message.from_user.get_profile_photos()
        if user_photos.total_count > 0:
            photo = user_photos.photos[0][-1]
            file = await bot.get_file(photo.file_id)
            file_url = f"https://api.telegram.org/file/bot{settings.BOT_TOKEN}/{file.file_path}"
        else:
            file_url = None
            
        user_fullname = None
        if message.from_user.first_name and message.from_user.last_name:
            user_fullname = f"{message.from_user.first_name} {message.from_user.last_name}"
        elif message.from_user.first_name:
            user_fullname = message.from_user.first_name
        elif message.from_user.last_name:
            user_fullname = message.from_user.last_name
            
        await user_service.add_user(
            user_id=message.from_user.id,
            referral_code=str(message.from_user.id),
            referral_id=int(reffer_id) if reffer_id else None,
            nickname=user_fullname,
            profile_photo=file_url,
        )


@router.message(Command('remove_kb'))
async def remove_kb_handler(
    message: Message,
    bot: Bot,
    event_chat: Chat,
    user_service: FromDishka[UserService],
) -> None:
    users = await user_service.get_users()
    for user in users:
        await bot.send_message(chat_id=user.user_id, text="test", reply_markup=ReplyKeyboardRemove())


from aiogram import Router, Bot, F
from aiogram.types import Message, Chat, FSInputFile, InputMediaPhoto
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.media_group import MediaGroupBuilder

from aiogram_album.album_message import AlbumMessage

from src.bot.app.bot.filters import AdminFilter
from src.bot.app.bot.keyboards import inline
from src.bot.app.bot.states import MailingSG


router = Router()
router.message.filter(AdminFilter())


@router.message(Command("admin"))
async def admin_panel_handler(
    message: Message,
    bot: Bot,
    event_chat: Chat,
) -> None:
    await bot.send_message(
        chat_id=event_chat.id,
        text="Админ-меню",
        reply_markup=inline.admin_menu_kb_markup,
    )


# MAILING HANDLERS
@router.message(MailingSG.MESSAGE, F.media_group_id)
async def mailing_message_handler(
    album_message: AlbumMessage,
    state: FSMContext,
    bot: Bot,
    event_chat: Chat,
) -> None:
    album_photo = [message.photo[-1].file_id for message in album_message]
    media_group = MediaGroupBuilder(caption=album_message.caption)

    for photo in album_photo:
        media_group.add_photo(media=photo)

    await state.update_data(media_group=media_group)
    await bot.send_message(
        chat_id=event_chat.id,
        text="Вы уверены, что хотите разослать это сообщение всем?",
        reply_markup=inline.mailing_choice_kb_markup,
    )
    await state.set_state(MailingSG.CHECKOUT)


@router.message(MailingSG.MESSAGE)
async def mailing_message_handler(
    message: Message,
    state: FSMContext,
    bot: Bot,
    event_chat: Chat,
) -> None:
    await state.update_data(message_id=message.message_id)
    await bot.send_message(
        chat_id=event_chat.id,
        text="Вы уверены, что хотите разослать это сообщение всем?",
        reply_markup=inline.mailing_choice_kb_markup,
    )
    await state.set_state(MailingSG.CHECKOUT)

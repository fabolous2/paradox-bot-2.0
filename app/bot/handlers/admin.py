from aiogram import Router, Bot
from aiogram.types import Message, Chat
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

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
@router.message(MailingSG.MESSAGE)
async def mailing_message_handler(
    message: Message,
    state: FSMContext,
    bot: Bot,
    event_chat: Chat,
) -> None:
    await state.update_data(mailing_message_id=message.message_id)
    await bot.send_message(
        chat_id=event_chat.id,
        text="Вы уверены, что хотите разослать это сообщение всем?",
        reply_markup=inline.mailing_choice_kb_markup,
    )
    await state.set_state(MailingSG.CHECKOUT)

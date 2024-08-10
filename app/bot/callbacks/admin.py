from aiogram import Router, Bot
from aiogram.types import Message, Chat

from app.bot.filters import AdminFilter
from app.bot.keyboards import inline


router = Router()
router.message.filter(AdminFilter)


@router.message("/admin")
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
    
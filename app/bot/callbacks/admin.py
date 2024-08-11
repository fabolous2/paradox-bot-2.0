from aiogram import Router, Bot, F
from aiogram.types import CallbackQuery, Chat
from aiogram.fsm.context import FSMContext

from src.bot.app.bot.filters import AdminFilter
from src.bot.app.bot.keyboards import inline
from src.bot.app.bot.states import MailingSG


router = Router()
router.callback_query.filter(AdminFilter)


@router.callback_query(F.data == 'back_apanel')
async def admin_panel_handler(
    query: CallbackQuery,
    bot: Bot,
    event_chat: Chat,
) -> None:
    await bot.edit_message_text(
        message_id=query.message.message_id,
        chat_id=event_chat.id,
        text="Админ-меню",
        reply_markup=inline.admin_menu_kb_markup,
    )


#MAILING HANDLERS
@router.callback_query(F.data == 'admin_mailing')
async def mailing_handler(
    query: CallbackQuery,
    bot: Bot,
    event_chat: Chat,
    state: FSMContext,
) -> None:
    await bot.edit_message_text(
        message_id=query.message.message_id,
        chat_id=event_chat.id,
        text="Введите текст рассылки:",
        reply_markup=inline.back_to_apanel_kb_markup,
    )
    await state.set_state(MailingSG.MESSAGE)


@router.callback_query(F.data == 'mailing_yes')
async def mailing_sender_handler(
    query: CallbackQuery,
    state: FSMContext,
    bot: Bot,
    event_chat: Chat,
) -> None:
    state_data = await state.get_data()
    mailing_message_id = state_data.get("mailing_message_id")

    users = [6384960822, 5297779345]
    for chat_id in users:
        try:    
            await bot.copy_message(
                chat_id=chat_id,
                from_chat_id=event_chat.id,
                message_id=mailing_message_id,
            )
        except Exception as ex:
            print(ex)

    await bot.send_message(chat_id=event_chat.id, text="Сообщение успешно разослано пользователям!")
    await bot.delete_message(
        chat_id=event_chat.id,
        message_id=query.message.message_id,
    )
    await state.clear()


@router.callback_query(F.data == 'mailing_no')
async def mailing_sender_handler(
    query: CallbackQuery,
    state: FSMContext,
    bot: Bot,
    event_chat: Chat,
) -> None:
    await state.clear()
    await bot.delete_message(chat_id=event_chat.id, message_id=query.message.message_id)
    await bot.send_message(chat_id=event_chat.id, text="Рассылка успешно отменена")

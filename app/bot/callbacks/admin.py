import uuid

from aiogram import Router, Bot, F
from aiogram.types import CallbackQuery, Chat
from aiogram.fsm.context import FSMContext

from dishka import FromDishka

from src.bot.app.bot.filters import AdminFilter
from src.bot.app.bot.keyboards import inline
from src.bot.app.bot.states import MailingSG, UpdateUserSG
from src.services import OrderService, ProductService, UserService
from src.schema.order import OrderStatus


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
        text="Отправьте сообщение, которое желаете разослать всем пользователям:",
        reply_markup=inline.back_to_apanel_kb_markup,
    )
    await state.set_state(MailingSG.MESSAGE)


@router.callback_query(F.data == 'confirm_mailing')
async def mailing_sender_handler(
    query: CallbackQuery,
    state: FSMContext,
    bot: Bot,
    event_chat: Chat,
) -> None:
    state_data = await state.get_data()
    media_group = state_data.get("media_group")
    message_id = state_data.get("message_id")

    users = [6384960822, 5297779345]
    for chat_id in users:
        try:
            if media_group:
                await bot.send_media_group(chat_id=chat_id, media=media_group.build())
            elif message_id:
                await bot.copy_message(
                    chat_id=chat_id,
                    message_id=message_id,
                    from_chat_id=event_chat.id,
                )
        except Exception as ex:
            print(ex)

    await bot.send_message(chat_id=event_chat.id, text="Сообщение успешно разослано пользователям!")
    await bot.delete_message(
        chat_id=event_chat.id,
        message_id=query.message.message_id,
    )
    await state.clear()


@router.callback_query(F.data == 'cancel_mailing')
async def mailing_sender_handler(
    query: CallbackQuery,
    state: FSMContext,
    bot: Bot,
    event_chat: Chat,
) -> None:
    await state.clear()
    await bot.delete_message(chat_id=event_chat.id, message_id=query.message.message_id)
    await bot.send_message(chat_id=event_chat.id, text="Рассылка успешно отменена")


#User Management
@router.callback_query(F.data == 'user_management')
async def user_profiles_handler(query: CallbackQuery, state: FSMContext) -> None:
    await query.message.answer('👤 Введите ID пользователя, чей профиль хотите редактировать.')
    await state.set_state(UpdateUserSG.USER_ID)


@router.callback_query(F.data.startswith('top_up_balance'))
async def top_up_handler(
    query: CallbackQuery, 
    state: FSMContext,
    bot: Bot,
    event_chat: Chat,
) -> None:
    user_id = query.data.split(':')[-1]
    await state.update_data(user_id=user_id)
    
    await bot.edit_message_text(
        chat_id=event_chat.id,
        text='Введите сумму, на которую хотите пополнить баланс пользователя.',
        message_id=query.message.message_id,
    )
    await state.set_state(UpdateUserSG.TOP_UP_BALANCE)


@router.callback_query(F.data.startswith('lower_balance'))
async def lower_balance_handler(
    query: CallbackQuery, 
    state: FSMContext,
    bot: Bot,
    event_chat: Chat,
) -> None:
    user_id = query.data.split(':')[-1]
    await state.update_data(user_id=user_id)

    await bot.edit_message_text(
        chat_id=event_chat.id,
        text='Введите сумму, которую хотите отнять у пользователя.',
        message_id=query.message.message_id,
    )
    await state.set_state(UpdateUserSG.LOWER_BALANCE)


@router.callback_query(F.data.startswith('set_balance'))
async def set_balance_handler(
    query: CallbackQuery, 
    state: FSMContext,
    bot: Bot,
    event_chat: Chat,
) -> None:
    user_id = query.data.split(':')[-1]
    await state.update_data(user_id=user_id)
    
    await bot.edit_message_text(
        chat_id=event_chat.id,
        text='Введите сумму, которую хотите установить пользователю.',
        message_id=query.message.message_id,
    )
    await state.set_state(UpdateUserSG.SET_BALANCE)


#ORDER
@router.callback_query(F.data.startswith('confirm_order'))
async def confirm_order_handler(
    query: CallbackQuery,
    order_service: FromDishka[OrderService],
    product_service: FromDishka[ProductService],
    bot: Bot,
    event_chat: Chat,
) -> None:
    order_id = query.data.split(':')[-1]
    order = await order_service.get_one_order(id=order_id)

    if order.status == OrderStatus.PROGRESS.value:
        product = await product_service.get_one_product(id=order.product_id)

        await order_service.update_order(
            order_id=uuid.UUID(order_id),
            status=OrderStatus.COMPLETED,
        )
        await product_service.update_product(product_id=order.product_id, purchase_count=product.purchase_count + 1)

        await bot.send_message(
            chat_id=order.user_id,
            text='✅ Ваш заказ выполнен! Спасибо за покупку, буду рад увидеться снова, могли бы оставить отзыва по кнопке снизу 👇',
            reply_markup=inline.post_feedback_kb_markup(product_id=order.product_id),
        )
        await bot.delete_message(chat_id=event_chat.id, message_id=query.message.message_id)
    else:
        await query.answer(text='Заказ уже обработан другим администратором', show_alert=True)
        await bot.delete_message(chat_id=event_chat.id, message_id=query.message.message_id)


@router.callback_query(F.data.startswith('cancel_order'))
async def cancel_order_handler(
    query: CallbackQuery,
    order_service: FromDishka[OrderService],
    product_service: FromDishka[ProductService],
    user_service: FromDishka[UserService],
    bot: Bot,
    event_chat: Chat,
) -> None:
    order_id = query.data.split(':')[-1]
    order = await order_service.get_one_order(id=order_id)
    
    if order.status == OrderStatus.PROGRESS.value:
        user = await user_service.get_one_user(user_id=order.user_id)
        product = await product_service.get_one_product(id=order.product_id)

        await order_service.update_order(
            order_id=uuid.UUID(order_id),
            status=OrderStatus.CLOSED,
        )
        await user_service.update_user(user_id=order.user_id, balance=user.balance + order.price)

        await bot.send_message(
            chat_id=order.user_id,
            text=f'❌ Ваш заказ на {product.name} был отклонен! Средства были возвращены на ваш счет.',
        )
        await bot.delete_message(chat_id=event_chat.id, message_id=query.message.message_id)
    else:
        await query.answer(text='Заказ уже обработан другим администратором', show_alert=True)
        await bot.delete_message(chat_id=event_chat.id, message_id=query.message.message_id)

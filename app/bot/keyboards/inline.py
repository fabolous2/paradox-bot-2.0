from uuid import UUID

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo


main_keyboard_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Открыть Магазин", web_app=WebAppInfo(url="https://paradox-shop.ru/"))
        ],
        [
            InlineKeyboardButton(text="Поддержка", callback_data="support"),
            InlineKeyboardButton(text="Правила", url="https://telegra.ph/ParadoxShop-06-03"),
        ],
    ]
)

back_to_main_menu_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu"),
        ],
    ]
)

def web_app_button(game_id: int) -> InlineKeyboardMarkup:
    if int(game_id) == 1:
        url = "https://paradox-shop.ru/game/1"
    elif int(game_id) == 2:
        url = "https://paradox-shop.ru/game/2"
    elif int(game_id) == 3:
        url = "https://paradox-shop.ru/game/3"
    elif int(game_id) == 4:
        url = "https://paradox-shop.ru/game/4"
    elif int(game_id) == 5:
        url = "https://paradox-shop.ru/game/5"
    elif int(game_id) == -1:
        url = "https://paradox-shop.ru/"

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="ЗА ДОНАТОМ!", web_app=WebAppInfo(url=url))
            ]
        ]
    )


admin_menu_kb_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Рассылка", callback_data="admin_mailing"),
            InlineKeyboardButton(text="Промокоды", callback_data="admin_promo"),
        ],
        [
            InlineKeyboardButton(text="Управление товарами", callback_data="product_management"),
            InlineKeyboardButton(text="Управление пользователями", callback_data="user_management"),
        ],
    ]
)


back_to_apanel_kb_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="◀️ Вернуться назад", callback_data="back_apanel"),
        ],
    ]
)


mailing_choice_kb_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Да", callback_data="confirm_mailing"),
            InlineKeyboardButton(text="Нет", callback_data="cancel_mailing"),
        ],
    ]
)


admin_promo_kb_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='➕ Создать промокод', callback_data='create_promo'),
            InlineKeyboardButton(text='🔧 Редактировать промокод', callback_data='edit_promo')
        ],
        [
            InlineKeyboardButton(text='ℹ️ Информация о промокоде', callback_data='info_promo'),
            InlineKeyboardButton(text='❌ Удалить промокод', callback_data='delete_promo')
        ],
        [
            InlineKeyboardButton(text="↪️ Вернуться назад", callback_data="back_apanel"),
        ],
    ]
)


def edit_promo_kb_markup(name: int | str) -> InlineKeyboardMarkup:
    kb_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='💵 Изменить сумму', callback_data=f'change_gift_amount|{name}'),
                InlineKeyboardButton(text='🔧 Изменить кол-во использований', callback_data=f'change_uses|{name}')
            ]
        ]
    )
    return kb_markup


def update_user_kb_markup(user_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Пополнить баланс', callback_data=f'top_up_balance:{user_id}'),
            ],
            [
                InlineKeyboardButton(text='Отнять баланс', callback_data=f'lower_balance:{user_id}'),
            ],
            [
                InlineKeyboardButton(text='Установить баланс', callback_data=f'set_balance:{user_id}'),
            ],
        ]
    )


def order_confirmation_kb_markup(order_id: UUID) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='✅ Подтвердить', callback_data=f'confirm_order:{order_id}'),
            ],
            [
                InlineKeyboardButton(text='❌ Отменить', callback_data=f'cancel_order:{order_id}'),
            ],
        ]
    )


def post_feedback_kb_markup(order_id: UUID) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
        [
                InlineKeyboardButton(text='👀 Оставить отзыв', web_app=WebAppInfo(url=f'https://paradox-shop.ru/post-feedback/{order_id}'))
            ]
        ]
    )

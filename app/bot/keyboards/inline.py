from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

from app.main.config import dev_config


main_keyboard_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        # [
        #     InlineKeyboardButton(text="Открыть Магазин", callback_data='not_implemented'), #web_app=WebAppInfo(url="https://localhost:5173/")
        # ],
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


admin_menu_kb_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Рассылка", callback_data="admin_mailing"),
            InlineKeyboardButton(text="Промокоды", callback_data="admin_promo"),
        ],
        [
            InlineKeyboardButton(text="Управление сайтом", callback_data="web_management"),
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
            InlineKeyboardButton(text="Да", callback_data="mailing_yes"),
            InlineKeyboardButton(text="Нет", callback_data="mailing_no"),
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

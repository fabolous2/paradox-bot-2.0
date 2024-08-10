from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

from app.main.config import dev_config


main_keyboard_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Открыть Магазин", web_app=WebAppInfo(url="http://localhost:5173/")),
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

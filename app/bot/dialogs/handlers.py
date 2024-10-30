import uuid

from aiogram import Bot
from aiogram.types import CallbackQuery, Message
from aiogram.utils.media_group import MediaGroupBuilder

from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput, TextInput
from aiogram_dialog.widgets.kbd import Button, Row, Back, Select
from aiogram_dialog.widgets.text import Format

from dishka import FromDishka

from app.bot.states.product import ProductManagementSG
from .inject_wrappers import inject_on_click
from app.services import ProductService, YandexStorageClient, UserService
from app.bot.states.mailing import MailingSG
from app.bot.keyboards import inline


async def message_input_fixing(
    message: Message,
    widget: MessageInput,
    dialog_manager: DialogManager,
):
    dialog_manager.show_mode = ShowMode.NO_UPDATE


async def add_product(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
):
    await dialog_manager.switch_to(ProductManagementSG.ADD_PRODUCT_NAME)


async def selected_game(
    callback_query: CallbackQuery,
    widget: Select,
    dialog_manager: DialogManager,
    item_id: str,
):
    dialog_manager.show_mode = ShowMode.EDIT
    dialog_manager.dialog_data["game_id"] = item_id
    await dialog_manager.switch_to(ProductManagementSG.GAME_MANAGEMENT)


async def selected_product(
    callback_query: CallbackQuery,
    widget: Select,
    dialog_manager: DialogManager,
    item_id: str,
):
    dialog_manager.show_mode = ShowMode.EDIT
    dialog_manager.dialog_data["product_id"] = item_id
    await dialog_manager.switch_to(ProductManagementSG.PRODUCT)


@inject_on_click
async def delete_product(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    product_service: FromDishka[ProductService],
):
    await product_service.delete_product(product_id=dialog_manager.dialog_data["product_id"])
    await dialog_manager.switch_to(ProductManagementSG.GAME_MANAGEMENT)


async def back_to_product(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
):
    await dialog_manager.switch_to(ProductManagementSG.PRODUCT)


async def back_to_game_management(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
):
    await dialog_manager.switch_to(ProductManagementSG.GAME_MANAGEMENT)


async def edit_product_name(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
):
    await dialog_manager.switch_to(ProductManagementSG.EDIT_PRODUCT_NAME)


async def edit_product_description(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
):
    await dialog_manager.switch_to(ProductManagementSG.EDIT_PRODUCT_DESCRIPTION)


async def edit_product_instruction(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
):
    await dialog_manager.switch_to(ProductManagementSG.EDIT_PRODUCT_INSTRUCTION)


async def edit_product_photo(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
):
    await dialog_manager.switch_to(ProductManagementSG.EDIT_PRODUCT_PHOTO)


async def edit_product_price(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
):
    await dialog_manager.switch_to(ProductManagementSG.EDIT_PRODUCT_PRICE)


@inject_on_click
async def on_product_name(
    callback_query: CallbackQuery,
    widget: TextInput,
    dialog_manager: DialogManager,
    value: str,
    product_service: FromDishka[ProductService],
):  
    await product_service.update_product(
        product_id=dialog_manager.dialog_data["product_id"],
        name=value,
    )
    await dialog_manager.switch_to(ProductManagementSG.PRODUCT)
    await callback_query.answer("Название товара успешно изменено", show_alert=True)


@inject_on_click
async def on_product_description(
    callback_query: CallbackQuery,
    widget: TextInput,
    dialog_manager: DialogManager,
    value: str,
    product_service: FromDishka[ProductService],
):  
    await product_service.update_product(
        product_id=dialog_manager.dialog_data["product_id"],
        description=value,
    )
    await dialog_manager.switch_to(ProductManagementSG.PRODUCT)
    await callback_query.answer("Описание товара успешно изменено", show_alert=True)


@inject_on_click
async def on_product_instruction(
    callback_query: CallbackQuery,
    widget: TextInput,
    dialog_manager: DialogManager,
    value: str,
    product_service: FromDishka[ProductService],
):  
    await product_service.update_product(
        product_id=dialog_manager.dialog_data["product_id"],
        instruction=value,
    )
    await dialog_manager.switch_to(ProductManagementSG.PRODUCT)
    await callback_query.answer("Инструкция товара успешно изменена", show_alert=True)


@inject_on_click
async def on_product_price(
    callback_query: CallbackQuery,
    widget: TextInput,
    dialog_manager: DialogManager,
    value: str,
    product_service: FromDishka[ProductService],
):  
    await product_service.update_product(
        product_id=dialog_manager.dialog_data["product_id"],
        price=float(value),
    )
    await dialog_manager.switch_to(ProductManagementSG.PRODUCT)
    await callback_query.answer("Цена товара успешно изменена", show_alert=True)


@inject_on_click
async def on_input_photo(
    message: Message,
    widget: MessageInput,
    dialog_manager: DialogManager,
    product_service: FromDishka[ProductService],
    yandex_storage_client: FromDishka[YandexStorageClient],
):  
    bot = dialog_manager.middleware_data.get("bot")
    file = await bot.get_file(message.photo[-1].file_id)
    photo_bytes = await bot.download_file(file.file_path)
    
    image_url = await yandex_storage_client.upload_file(photo_bytes, object_name=f"{message.photo[-1].file_id}.jpg")
    await product_service.update_product(
        product_id=dialog_manager.dialog_data["product_id"],
        image_url=image_url,
    )
    await message.delete()
    await dialog_manager.switch_to(ProductManagementSG.PRODUCT)


async def on_product_name_new_product(
    callback_query: CallbackQuery,
    widget: TextInput,
    dialog_manager: DialogManager,
    value: str,
):
    dialog_manager.dialog_data["product_name"] = value
    await dialog_manager.switch_to(ProductManagementSG.ADD_PRODUCT_DESCRIPTION)


async def on_product_description_new_product(
    callback_query: CallbackQuery,
    widget: TextInput,
    dialog_manager: DialogManager,
    value: str,
):
    dialog_manager.dialog_data["product_description"] = value
    await dialog_manager.switch_to(ProductManagementSG.ADD_PRODUCT_INSTRUCTION)


async def on_product_instruction_new_product(
    callback_query: CallbackQuery,
    widget: TextInput,
    dialog_manager: DialogManager,
    value: str,
):
    dialog_manager.dialog_data["product_instruction"] = value
    await dialog_manager.switch_to(ProductManagementSG.ADD_PRODUCT_PRICE)


async def on_product_price_new_product(
    callback_query: CallbackQuery,
    widget: TextInput,
    dialog_manager: DialogManager,
    value: str,
):
    dialog_manager.dialog_data["product_price"] = float(value)
    await dialog_manager.switch_to(ProductManagementSG.ADD_PRODUCT_PHOTO)


@inject_on_click
async def on_input_photo_new_product(
    message: Message,
    widget: MessageInput,
    dialog_manager: DialogManager,
    product_service: FromDishka[ProductService],
    yandex_storage_client: FromDishka[YandexStorageClient],
):  
    try:
        bot = dialog_manager.middleware_data.get("bot")
        file = await bot.get_file(message.photo[-1].file_id)
        photo_bytes = await bot.download_file(file.file_path)

        games_dict = {
            "1": "Brawl Stars",
            "2": "Squad Busters",
            "3": "Clash of Clans",
            "4": "Clash Royale",
            "5": "Roblox",
            "6": "Fortnite",
            "7": "PUBG",
            "8": "FIFA Mobile",
            "9": "Minecraft",
            "10": "Stumble Guys",
            "11": "My Singing Monsters",
            "12": "World of Tanks [Евро]",
            "13": "Blockman Go",
            "14": "Supercell Store",
            "15": "Brawl Stars",
            "16": "Squad Busters",
            "17": "Clash of Clans",
            "18": "Clash Royale",
        }

        image_url = await yandex_storage_client.upload_file(photo_bytes, object_name=f"{message.photo[-1].file_id}.jpg")
        await product_service.create_product(
            id=uuid.uuid4(),
            name=dialog_manager.dialog_data["product_name"],
            description=dialog_manager.dialog_data["product_description"],
            instruction=dialog_manager.dialog_data["product_instruction"],
            price=int(dialog_manager.dialog_data["product_price"]),
            image_url=image_url,
            category="something",
            game_id=int(dialog_manager.dialog_data["game_id"]),
            game_name=games_dict[dialog_manager.dialog_data["game_id"]],
        )
        await message.delete()
    except Exception as e:
        print(e)
    finally:
        await dialog_manager.switch_to(ProductManagementSG.GAME_MANAGEMENT)


@inject_on_click
async def selected_game_button(
    callback_query: CallbackQuery,
    widget: Select,
    dialog_manager: DialogManager,
    item_id: str,
) -> None:
    dialog_manager.dialog_data["game_button_id"] = item_id
    await dialog_manager.switch_to(MailingSG.CHECKOUT)


@inject_on_click
async def main_menu_button(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
) -> None:
    dialog_manager.dialog_data["game_button_id"] = -1
    await dialog_manager.switch_to(MailingSG.CHECKOUT)



@inject_on_click
async def confirm_mailing(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    user_service: FromDishka[UserService],
) -> None:
    album_photo = dialog_manager.start_data.get("album_photo")
    users = await user_service.get_users()
    bot: Bot = dialog_manager.middleware_data.get("bot")
    message_id = dialog_manager.start_data.get("message_id")
    album_caption = dialog_manager.start_data.get("album_caption")

    for user in users:
        try: 
            if album_photo:
                media_group = MediaGroupBuilder(caption=album_caption)
                for photo in album_photo:
                    media_group.add_photo(media=photo)
                await bot.send_media_group(chat_id=user.user_id, media=media_group.build())
            elif message_id:
                await bot.copy_message(
                    chat_id=user.user_id,
                    message_id=message_id,
                    caption=album_caption,
                    from_chat_id=callback_query.message.chat.id,
                    reply_markup=inline.web_app_button(dialog_manager.dialog_data["game_button_id"]),
                )
        except Exception as ex:
            print(ex)

    await bot.send_message(chat_id=callback_query.message.chat.id, text="Сообщение успешно разослано пользователям!")
    await bot.delete_message(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
    )
    await dialog_manager.done()


async def cancel_mailing(
    callback_query: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
) -> None:
    bot = dialog_manager.middleware_data.get("bot")
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
    await bot.send_message(chat_id=callback_query.message.chat.id, text="Рассылка успешно отменена")
    await dialog_manager.done()

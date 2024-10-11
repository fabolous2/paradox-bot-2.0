from typing import Coroutine, Any
import uuid

from aiogram import Bot
from aiogram.types import InputFile
from aiogram_dialog import DialogManager
from aiogram_dialog.manager.message_manager import MessageManager
from aiogram_dialog.api.entities import MediaAttachment, MediaId

from aiogram.types import BufferedInputFile
from aiogram.enums import ContentType

from dishka import FromDishka

from src.services import GameService, ProductService, YandexStorageClient
from src.main.config import settings
from .inject_wrappers import inject_getter


class YandexStorageMedia(MessageManager):
    async def get_media_source(self, media: MediaAttachment, bot: Bot) -> Coroutine[Any, Any, InputFile | str]:
        yandex_storage_client = YandexStorageClient(
            token=settings.YANDEX_STORAGE_TOKEN,
            bucket_name=settings.YANDEX_STORAGE_BUCKET_NAME,
            secret=settings.YANDEX_STORAGE_SECRET,
        )

        if media.file_id:
            return await super().get_media_source(media, bot)
        if media.url:
            object_name = media.url.split('/')[-1]
            file = yandex_storage_client.get_file(object_url=media.url)
            return BufferedInputFile(file, filename=object_name)
        return await super().get_media_source(media, bot)


@inject_getter
async def games_getter(
    dialog_manager: DialogManager,
    game_service: FromDishka[GameService],
    **kwargs
) -> dict:
    games = await game_service.get_all_games()
    
    for game in games:
        if game.id in [15, 16, 17, 18]:
            game.name += "⭐"
    
    return {
        "games": games,
    }


@inject_getter
async def one_game_getter(
    dialog_manager: DialogManager,
    game_service: FromDishka[GameService],
    product_service: FromDishka[ProductService],
    **kwargs,
) -> dict:
    game_id = dialog_manager.dialog_data["game_id"]
    game = await game_service.get_game(id=int(game_id))
    products = await product_service.get_products(game_id=int(game_id))

    if game.id in [15, 16, 17, 18]:
        game.name += "⭐"

    return {
        "products": products,
        "game": game,
    }


@inject_getter
async def one_product_getter(
    dialog_manager: DialogManager,
    product_service: FromDishka[ProductService],
    **kwargs,
) -> dict:
    product_id = dialog_manager.dialog_data["product_id"]
    product = await product_service.get_one_product(id=uuid.UUID(product_id))
    
    return {
        "photo": MediaAttachment(
           url=product.image_url,
           type=ContentType.PHOTO,
        ),
        "product": product,
    }

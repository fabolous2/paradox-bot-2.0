from aiogram.types import Message
from aiogram.filters import BaseFilter

from app.main.config import dev_config


class AdminFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in dev_config.admin.admins
    
from typing import Any, Awaitable, Callable, Dict

from dishka import AsyncContainer, Scope

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import TelegramObject, Message

from src.services import UserService


class UserMiddleware(BaseMiddleware):

    def __init__(self, dishka_container: AsyncContainer) -> None:
        self._dishka_container = dishka_container

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        async with self._dishka_container(scope=Scope.REQUEST) as request_container:
            user_service = await request_container.get(UserService)

        user = data['event_from_user']
        exists = await user_service.exists(user_id=user.id)
        if not exists:
            reffer_id = None
            if isinstance(event, Message):
                start_command = event.text   
                reffer_id = start_command[7:] if len(start_command) > 7 and start_command[7:].isdigit() else None
                reffer_id = reffer_id[4:]
                
            await user_service.add_user(
                user_id=user.id,
                referral_code=str(user.id),
                referral_id=reffer_id,
            )
        
        return await handler(event, data)
    
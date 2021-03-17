from dataclasses import dataclass

from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.handler import ctx_data
from aiogram.types.base import TelegramObject

from ...models.user import User


@dataclass
class IsSuperUserFilter(BoundFilter):
    key = "is_superuser"
    is_superuser: bool

    async def check(self, obj: TelegramObject) -> bool:
        data: dict = ctx_data.get()
        db_user: User = data["db_user"]
        return db_user.is_superuser

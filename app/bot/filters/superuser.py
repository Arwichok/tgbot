from dataclasses import dataclass

from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.filters.builtin import Command
from aiogram.dispatcher.handler import ctx_data
from aiogram.types import Message
from aiogram.types.base import TelegramObject
from aiogram.utils.exceptions import ChatNotFound
from asyncpg import Connection

from ...models.user import User

USER_ARG_COMMANDS = ["superuser", "restrict"]


@dataclass
class IsSuperUserFilter(BoundFilter):
    key = "is_superuser"
    is_superuser: bool

    async def check(self, obj: TelegramObject) -> bool:
        data: dict = ctx_data.get()
        db = data["db"]
        db_user: User = await User.create(db, obj.from_user.id)
        return db_user.is_superuser


class SuperUserCommand(Command):
    def __init__(self, command):
        super().__init__(command, ".")
        self.command = command

    async def check(self, msg: Message):
        """
        Check is user is superuser
        If command in list USER_ARG_COMMANDS:
            Get second argument, check if argument it's user id, transfer to handler
            user obj with id from argument
        """
        db: Connection = ctx_data.get()["db"]
        db_user = await User.create(db, msg.from_user.id)
        check = db_user.is_superuser and await super().check(msg)

        if self.command in USER_ARG_COMMANDS and check:
            try:
                second_arg = msg.text.split()[1]
                user_arg = await msg.bot.get_chat(second_arg)
                check = {"user_arg": user_arg}
            except (IndexError, ChatNotFound):
                await msg.answer("Chat not found")
                return
        return check

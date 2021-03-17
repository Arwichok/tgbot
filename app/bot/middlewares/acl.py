from aiogram.dispatcher.middlewares import BaseMiddleware
from asyncpg import Connection

from ...models.user import User


class ACLMiddleware(BaseMiddleware):
    async def setup_chat(self, data, tg_user, tg_chat):
        user_id = tg_user.id
        # chat_id = tg_chat.id if tg_chat else tg_user.id
        # chat_type = tg_chat.type if tg_chat else "private"
        db: Connection = data["db"]

        db_user: User = await User.get(db, user_id)
        if not db_user:
            db_user: User = await User.create(db, user_id)

        data["db_user"] = db_user

    async def on_pre_process_message(self, message, data):
        await self.setup_chat(data, message.from_user, message.chat)

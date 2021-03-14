import logging

from aiogram import Dispatcher
from aiogram.types import Update
from aiogram.utils.exceptions import BotBlocked
from asyncpg import Connection

from ...models.user import stopped_by_user


async def bot_blocked_error(update: Update, exception, db: Connection):
    user_id: int = update.message.from_user.id
    await stopped_by_user(db, user_id)
    logging.warning(f"User: {user_id} blocked bot")
    return True


async def errors(update: Update, exception: Exception):
    logging.error(f"Error: {exception} \nin Update: {update}")


def setup(dp: Dispatcher):
    dp.register_errors_handler(bot_blocked_error, exception=BotBlocked)
    dp.register_errors_handler(errors)

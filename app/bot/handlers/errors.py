import logging

from aiogram import Dispatcher
from aiogram.utils.exceptions import BotBlocked

from ...models.user import stopped_by_user


async def bot_blocked_error(update, exception, db):
    user_id = update.message.from_user.id
    await stopped_by_user(db, user_id)
    logging.warning(f"User: {user_id} blocked bot")
    return True


async def errors(update, exception):
    logging.error("##3333333333333333333333333333")


def setup(dp: Dispatcher):
    dp.register_errors_handler(bot_blocked_error, exception=BotBlocked)
    dp.register_errors_handler(errors)

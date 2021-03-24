import logging

from aiogram import Dispatcher, md
from aiogram.dispatcher.filters.builtin import CommandHelp
from aiogram.types import Message
from asyncpg import Connection

from ...models.user import User
from ..filters.superuser import SuperUserCommand


async def superuser_help(msg: Message):
    await msg.answer(
        "/ping Pong\n"
        "/help Show this page\n"
        "<b>Superuser commands:</b>\n"
        ".superuser {id}\n"
        ".restrict {id}"
    )


async def create_superuser(msg: Message, db: Connection, user_arg):
    if not user_arg:
        await msg.answer("Chat not found")
        return
    super_id = user_arg.id
    name = user_arg.first_name
    link = f"tg://user?id={super_id}"

    await User.create_super(db, super_id)
    await msg.answer(f"{md.hlink(name, link)} now is superuser")
    logging.info(f"Created superuser {name}({super_id})")


async def restrict_superuser(msg: Message, db: Connection, user_arg):
    if not user_arg:
        await msg.answer("Chat not found")
        return
    super_id = user_arg.id
    name = user_arg.first_name
    link = md.hlink(name, f"tg://user?id={super_id}")

    await User.restrict_super(db, super_id)
    await msg.answer(f"{link} restricted to user")
    logging.info(f"Restricted to user {name}({super_id})")


def setup(dp: Dispatcher):
    dp.register_message_handler(superuser_help, CommandHelp(), is_superuser=1)
    dp.register_message_handler(create_superuser, SuperUserCommand("superuser"))
    dp.register_message_handler(restrict_superuser, SuperUserCommand("restrict"))

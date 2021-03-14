from aiogram import Dispatcher

from . import commands, errors


def setup_handlers(dp: Dispatcher):
    commands.setup(dp)
    errors.setup(dp)

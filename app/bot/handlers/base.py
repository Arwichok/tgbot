from aiogram import Dispatcher

from . import commands, errors, superuser


def setup_handlers(dp: Dispatcher):
    superuser.setup(dp)
    commands.setup(dp)
    errors.setup(dp)

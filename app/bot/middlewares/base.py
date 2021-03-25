from aiogram import Dispatcher
from asyncpg.pool import Pool

from .db import DBMiddleware


def setup_middlewares(dp: Dispatcher, pool: Pool):
    dp.middleware.setup(DBMiddleware(pool))

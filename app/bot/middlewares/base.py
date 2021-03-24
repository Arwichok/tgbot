from aiogram import Dispatcher
from asyncpg.pool import Pool

from .acl import ACLMiddleware
from .db import DBMiddleware
from .log import LogMiddleware


def setup_middlewares(dp: Dispatcher, pool: Pool):
    dp.middleware.setup(DBMiddleware(pool))
    # dp.middleware.setup(LogMiddleware())
    # dp.middleware.setup(ACLMiddleware())

import logging
import asyncpg

from .. import models
from .handlers.base import setup_handlers
#from .middlewares impor DBMiddleware



def setup(dp):
    setup_handlers(dp)


async def on_startup(dp):
    ... # dp.middleware.setup(DBMiddleware(pool))


async def on_shutdown(dp):
    logging.info('Shutdown')

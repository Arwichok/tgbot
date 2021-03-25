import asyncio
import logging

from aiogram import Dispatcher
from aiohttp.web import Application
from asyncpg.pool import Pool

from .base import init_dp, on_shutdown, on_startup
from ..models.base import init_pool


def run_polling():
    dp: Dispatcher = init_dp()
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(_on_startup_polling(dp))
        loop.run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        loop.run_until_complete(_on_shutdown_polling(dp))


async def _on_startup_polling(dp: Dispatcher, pool: Pool=init_pool()):
    await on_startup(dp, pool)
    loop = asyncio.get_event_loop()
    loop.create_task(dp.start_polling())


async def _on_shutdown_polling(dp: Dispatcher):
    dp.stop_polling()
    await on_shutdown(dp)
    await dp.bot.session.close()


def setup_web_polling(app: Application):
    dp: Dispatcher = init_dp()
    logging.warning("\033[1;31mDO NOT USE FOR PRODUCTION\033[0m")

    async def _up(_):
        await _on_startup_polling(dp, app["pool"])

    async def _down(_):
        await _on_shutdown_polling(dp)

    app.on_startup.append(_up)
    app.on_shutdown.append(_down)

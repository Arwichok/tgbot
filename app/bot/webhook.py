import asyncio
import logging

from aiogram import Bot, Dispatcher, executor
from aiogram.dispatcher.webhook import (
    WebhookRequestHandler,
    DEFAULT_ROUTE_NAME,
    BOT_DISPATCHER_KEY as DP_KEY
    )

from ..utils import config
from .base import init_dp, on_startup, on_shutdown



def setup_webhook(app):
    dp = init_dp()
    _install_bot(app, dp)


def _install_bot(app, dp):
    app[DP_KEY] = dp
    app['_check_ip'] = config.CHECK_IP
    app.router.add_route(
        method='*',
        path=config.WH_PATH,
        handler=WebhookRequestHandler,
        name=DEFAULT_ROUTE_NAME)
    app.on_startup.append(_startup)
    app.on_shutdown.append(_shutdown)


async def _startup(app):
    dp = app[DP_KEY]
    await dp.bot.set_webhook(config.WH_URL)
    await on_startup(dp)
    await _welcome(dp)
    if config.SKIP_UPDATES:
        await _skip_updates(dp)


async def _shutdown(app):
    dp = app[DP_KEY]
    await on_shutdown(dp)
    await _shutdown_webhook(dp)
    logging.info("Stop webhook")


async def _welcome(dp):
    me = await dp.bot.me
    logging.info("Start webhook")


async def _skip_updates(dp):
    await dp.reset_webhook(True)
    await dp.skip_updates()


async def _shutdown_webhook(dp):
    await dp.storage.close()
    await dp.storage.wait_closed()
    await dp.bot.delete_webhook()
    await dp.bot.session.close()

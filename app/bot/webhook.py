import logging

from aiogram import Dispatcher
from aiogram.dispatcher.webhook import (BOT_DISPATCHER_KEY, DEFAULT_ROUTE_NAME,
                                        WebhookRequestHandler)
from aiohttp.web import Application

from ..utils import config
from .base import init_dp, on_shutdown, on_startup


def setup_webhook(app: Application):
    dp = init_dp()
    _install_bot_to_app(app, dp)


def _install_bot_to_app(app: Application, dp: Dispatcher):
    app[BOT_DISPATCHER_KEY] = dp
    app["_check_ip"] = config.CHECK_IP
    app.router.add_route(
        method="*",
        path=config.WH_PATH,
        handler=WebhookRequestHandler,
        name=DEFAULT_ROUTE_NAME,
    )
    app.on_startup.append(_startup)
    app.on_shutdown.append(_shutdown)


async def _startup(app: Application):
    dp = app[BOT_DISPATCHER_KEY]
    await dp.bot.set_webhook(config.WH_URL)
    await on_startup(dp)
    if config.SKIP_UPDATES:
        await _skip_updates(dp)
    logging.info("Start webhook")


async def _shutdown(app: Application):
    dp = app[BOT_DISPATCHER_KEY]
    await on_shutdown(dp)
    await _shutdown_webhook(dp)
    logging.info("Stop webhook")


async def _skip_updates(dp: Dispatcher):
    await dp.reset_webhook(True)
    await dp.skip_updates()


async def _shutdown_webhook(dp: Dispatcher):
    await dp.storage.close()
    await dp.storage.wait_closed()
    await dp.bot.delete_webhook()
    await dp.bot.session.close()

import asyncio
import logging

import aiohttp
import click

from . import config
from .logging import setup_log
from ..bot.polling import run_polling, setup_web_polling
from ..bot.webhook import setup_webhook
from ..web.base import setup_web



@click.group()
def cli():
    setup_log()


@cli.command()
def polling():
    run_polling()


@cli.command()
def web_polling():
    app = init_app()
    setup_web_polling(app)
    run_app(app)


@cli.command()
def webhook():
    app = init_app()
    setup_webhook(app)
    run_app(app)


def init_app():
    app = aiohttp.web.Application()
    setup_web(app)
    return app


async def wsgi():
    app = init_app()
    setup_webhook(app)
    return app


def run_app(app):
    aiohttp.web.run_app(app, **config.APP_CONFIG)
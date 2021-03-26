import aiohttp
import click
from aiohttp.web import Application

from .._version import __version__
from ..bot.polling import run_polling, setup_web_polling
from ..bot.webhook import setup_webhook
from ..models.base import init_pool
from ..web.base import setup_web
from . import config
from .logging import setup_log


@click.group()
def cli():
    setup_log()


@cli.command()
def polling():
    run_polling()


@cli.command()
def web_polling():
    app: Application = init_app()
    setup_web_polling(app)
    run_app(app)


@cli.command()
def webhook():
    app: Application = init_app()
    setup_webhook(app)
    run_app(app)


@cli.command()
def version():
    click.echo(__version__)


def init_app():
    app = Application()
    setup_web(app)
    app["pool"] = init_pool()
    return app


async def wsgi():
    app: Application = init_app()
    setup_webhook(app)
    return app


def run_app(app: Application):
    aiohttp.web.run_app(app, **config.WEB_APP)

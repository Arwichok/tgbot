import logging

from aiohttp.web import Application
from asyncpg.pool import Pool

from ..models.base import init_db
from .routes import setup_routes


async def on_startup(app: Application):
    db_pool: Pool = await init_db()
    app["db_pool"] = db_pool
    logging.info("Startup web")


def setup_web(app: Application):
    app.on_startup.append(on_startup)
    setup_routes(app)

from aiohttp.web import Application
from asyncpg.pool import Pool

from ..models.base import startup_db
from .routes import setup_routes


async def on_startup(app: Application):
    pool: Pool = app["pool"]
    await startup_db(pool)


def setup_web(app: Application):
    app.on_startup.append(on_startup)
    setup_routes(app)

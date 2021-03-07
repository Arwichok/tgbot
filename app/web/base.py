import logging

from ..models.base import init_db
from .routes import setup_routes


async def on_startup(app):
    db_pool = await init_db()
    app["db_pool"] = db_pool
    logging.info("Startup web")


def setup_web(app):
    app.on_startup.append(on_startup)
    setup_routes(app)

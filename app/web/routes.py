from aiohttp.web import Application

from . import views


def setup_routes(app: Application):
    app.router.add_get("/", views.index)

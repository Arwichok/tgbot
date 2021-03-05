from . import views


def setup_routes(_app):
	_app.router.add_get('/', views.index)

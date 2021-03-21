include .env

VENV    = venv
PROJECT = app
WSGI = $(PROJECT).utils.run:wsgi
CONFIG  = $(PROJECT).utils.config
export PATH := $(PWD)/$(VENV)/bin:$(PATH)


clean:
	rm -rf $(VENV)
	find . -type d -name '__pycache__' -exec rm -r {} +


venv:
	python3 -m venv $(VENV)


install:
	pip install -r requirements.txt


install_dev: install
	pip install -r requirements-dev.txts


gunicorn:
	gunicorn $(WSGI) -c python:$(CONFIG)


start:
	python -m $(PROJECT)


webhook:
	python -m $(PROJECT) webhook


polling:
	python -m $(PROJECT) polling


web_polling:
	python -m $(PROJECT) web-polling

tree:
	tree -I 'venv|__p*' --dirsfirst

lint:
	isort .
	black .
	flake8 .

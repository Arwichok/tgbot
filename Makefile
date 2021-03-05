VENV    = venv
PROJECT = app
WEB_APP = $(PROJECT).utils.run:init_app
CONFIG  = $(PROJECT).utils.config



clear:
	rm -rf $(VENV)
	find . -type d -name '__pycache__' -exec rm -r {} +


init:
	python3 -m venv $(VENV)
	$(VENV)/bin/pip install -r requirements.txt


test:
	ENV=.env.test make base


gunicorn:
	$(VENV)/bin/gunicorn $(WEB_APP) -c python:$(CONFIG)


start:
	$(VENV)/bin/python -m $(PROJECT)


webhook:
	USE_WEBHOOK=TRUE $(VENV)/bin/python -m $(PROJECT)


polling:
	@echo Not supported
	USE_WEBHOOK=FALSE $(VENV)/bin/python -m $(PROJECT)

tree:
	tree -I 'venv|__p*'

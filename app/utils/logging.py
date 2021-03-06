import logging




def setup():
	logging.basicConfig(
        level=logging.INFO,
        format=config.LOG_FORMAT,
        datefmt="%Y-%m-%d %H:%M:%S %z")

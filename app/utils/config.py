from time import sleep

from aiohttp import BasicAuth
from environs import Env

env = Env()
env_f = env("ENV", ".env")
env.read_env(env_f)

TG_BOT_TOKEN = env("TG_BOT_TOKEN", None)
SKIP_UPDATES = env.bool("SKIP_UPDATES", True)
USE_WEBHOOK = env.bool("USE_WEBHOOK", True)
CHECK_IP = env.bool("CHECK_IP", False)
SUPERUSER = env.int("SUPERUSER", 0)

PROXY_URL = env("PROXY_URL", "")
PROXY_LOGIN = env("PROXY_LOGIN", "")
PROXY_PASSWORD = env("PROXY_PASSWORD", "")
PROXY_AUTH = BasicAuth(login=PROXY_LOGIN, password=PROXY_PASSWORD)

LOG_FORMAT = env("LOG_FORMAT", None)
DEBUG = env.bool("DEBUG", True)

WH_HOST = env("WH_HOST", "https://example.com")
WH_PATH = env("WH_PATH", "/")
WH_URL = env("WH_URL", WH_HOST + WH_PATH)

LC_HOST = env.str("LC_HOST", "localhost")
LC_PORT = env.int("LC_PORT", 8080)
LC_BIND = env.str("LC_BIND", f"{LC_HOST}:{LC_PORT}")
APP_CONFIG = {"host": LC_HOST, "port": LC_PORT}

PGHOST = env("PGHOST", "localhost")
PGPORT = env.int("PGPORT", 5432)
PGUSER = env("PGUSER", "postgres")
PGPASSWORD = env("PGPASSWORD", "postgres")
PGDATABASE = env("PGDATABASE", "postgres")
PGCONFIG = {
    "host": PGHOST,
    "port": PGPORT,
    "user": PGUSER,
    "password": PGPASSWORD,
    "database": PGDATABASE,
}


# gunicorn config
bind = LC_BIND
worker_class = "aiohttp.GunicornWebWorker"
workers = 1
timeout = 60
keepalive = 2


def pre_fork(i, j):
    sleep(1.5)

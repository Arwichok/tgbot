from time import sleep

from environs import Env

env = Env()
ENV_FILE = env("ENV", ".env")
env.read_env(ENV_FILE)

# Telegram Bot
TG_API_SERVER = env("TG_API_SERVER", "https://api.telegram.org")
TG_BOT_TOKEN = env("TG_BOT_TOKEN", None)
TG_BOT_ID = TG_BOT_TOKEN.split(":")[0]
SKIP_UPDATES = env.bool("SKIP_UPDATES", True)
SUPERUSER = env.int("SUPERUSER", 0)

# Telegram Client
TG_API_ID = env.int("TG_API_ID")
TG_API_HASH = env("TG_API_HASH")

# Logging
LOG_FORMAT = env("LOG_FORMAT", None)
DEBUG = env.bool("DEBUG", False)

# Proxy
PROXY_URL = env("PROXY_URL", "")
PROXY_AUTH = {"login": env("PROXY_LOGIN", ""), "password": env("PROXY_PASSWORD", "")}

# Webhook
CHECK_IP = env.bool("CHECK_IP", False)
WH_HOST = env("WH_HOST", "example.com")
WH_PATH = env("WH_PATH", "/webhook")
WH_URL = f"https://{WH_HOST+WH_PATH}"

# Web app
WEB_APP = {"host": env.str("APP_HOST", "127.0.0.1"), "port": env.int("APP_PORT", 8080)}

# PostgreSQL
PGCONFIG = {
    "host": env("PGHOST", "127.0.0.1"),
    "port": env.int("PGPORT", 5432),
    "user": env("PGUSER", "postgres"),
    "password": env("PGPASSWORD", "postgres"),
    "database": env("PGDATABASE", "postgres"),
}

# Gunicorn
bind = "{host}:{port}".format(**WEB_APP)
worker_class = "aiohttp.GunicornWebWorker"
workers = env.int("WORKERS", 1)
timeout = 60
keepalive = 2


def pre_fork(i, j):
    sleep(1.5)

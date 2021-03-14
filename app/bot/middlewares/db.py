from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from asyncpg import Connection
from asyncpg.pool import Pool


class DBMiddleware(LifetimeControllerMiddleware):
    def __init__(self, pool: Pool):
        super().__init__()
        self.pool = pool
        self.skip_patterns = []  # ['updates']

    async def pre_process(self, obj, data, *args):
        db: Connection = await self.pool.acquire()
        data["db"] = db

    async def post_process(self, obj, data, *args):
        db: Connection = data.get("db")
        if db:
            await db.close()

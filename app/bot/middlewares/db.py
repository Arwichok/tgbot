from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware


class DBMiddleware(LifetimeControllerMiddleware):
    def __init__(self, pool):
        super().__init__()
        self.pool = pool
        self.skip_patterns = None  # ['updates']

    async def pre_process(self, obj, data, *args):
        db = await self.pool.acquire()
        data["db"] = db

    async def post_process(self, obj, data, *args):
        if db := data.get("db"):
            await db.close()

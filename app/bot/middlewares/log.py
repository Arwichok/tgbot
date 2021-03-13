import time

from aiogram.dispatcher.middlewares import BaseMiddleware

# from ...utils import funcs


class LogMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()

    async def on_pre_process_message(self, update, data: dict):
        data["start_time"] = time.time()

    async def on_post_process_message(self, update, data, result):
        pass
        # pt = funcs.delta_time(result.get("start_time", 0))

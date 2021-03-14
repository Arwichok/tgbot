from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.storage import BaseStorage


def init_storage() -> BaseStorage:
    return MemoryStorage()

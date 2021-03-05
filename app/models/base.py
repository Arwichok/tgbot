import logging

import asyncpg

from ..utils import config



async def init_db():
    return await asyncpg.create_pool(**config.PGCONFIG)


async def execute(pool, query, *args, **kwargs):
    async with pool.acquire() as conn:
        async with conn.transaction():
           await conn.execute(query, *args, **kwargs)




class Base():
    _pool = None

    EXECUTE = 'execute'
    FETCHVAL = 'fetchval'

    @classmethod
    def pool(cls):
        return cls._pool

    @classmethod
    def setup(cls, pool):
        cls._pool = pool


    @classmethod
    async def execute(cls, command, *args, **kwargs):
        return await cls._connect(cls.EXECUTE, command, *args, **kwargs)


    @classmethod
    async def fetchval(cls, command, *args, **kwargs):
        return await cls._connect(cls.FETCHVAL, command, *args, **kwargs)

    @classmethod
    async def _connect(cls, method_name, *args, **kwargs):
        async with cls._pool.acquire() as conn:
            if(method := {
                cls.FETCHVAL: conn.fetchval,
                cls.EXECUTE: conn.execute
            }.get(method_name)):
                return await method(*args, **kwargs)



async def on_startup(dp):
    pool = await asyncpg.create_pool(**config.PGCONFIG)
    logging.info("Database started")
    return pool


    Base.setup(pool)
    await Base.execute(setup_sql)
    await Base.execute("INSERT INTO users (id) VALUES($1)", 11)
    r = await Base.fetchval('select 1')
    logging.info(f"Database run: {r}")


async def on_shutdown(dp):
    pass




setup_sql = '''
CREATE TABLE IF NOT EXISTS users(
    id int PRIMARY KEY,
    started_at date,
    is_stoped bool,
    is_superuser bool DEFAULT false
)
'''

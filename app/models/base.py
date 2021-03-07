import asyncpg

from ..utils import config


async def init_db():
    return await asyncpg.create_pool(**config.PGCONFIG)


async def execute(pool, query, *args, **kwargs):
    async with pool.acquire() as conn:
        async with conn.transaction():
            await conn.execute(query, *args, **kwargs)


setup_sql = '''
CREATE TABLE IF NOT EXISTS users(
    id int PRIMARY KEY,
    started_at date,
    is_stoped bool,
    is_superuser bool DEFAULT false
)
'''

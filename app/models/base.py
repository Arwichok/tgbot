import logging

from asyncpg import Connection, create_pool
from asyncpg.pool import Pool

from ..utils import config
from . import user

logger = logging.getLogger(__name__)


async def init_db() -> Pool:
    try:
        pool: Pool = await create_pool(**config.PGCONFIG)
        await setup_models(pool)
        return pool
    except ConnectionRefusedError as e:
        logger.error(e)
        exit(0)


async def setup_models(pool: Pool):
    async with pool.acquire() as conn:
        async with conn.transaction():
            await user.setup(conn)


async def execute(pool: Pool, query: str, *args, **kwargs):
    async with pool.acquire() as conn:
        async with conn.transaction():
            await conn.execute(query, *args, **kwargs)

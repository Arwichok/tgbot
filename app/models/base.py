import logging

from asyncpg import Connection, create_pool
from asyncpg.pool import Pool

from ..utils import config
from . import user

logger = logging.getLogger(__name__)


async def init_db() -> Pool:
    try:
        pool: Pool = await create_pool(**config.PGCONFIG)
        await setup_model(pool)
        return pool
    except ConnectionRefusedError as e:
        logger.error(e)
        exit(0)


async def setup_model(pool: Pool):
    async with pool.acquire() as conn:
        async with conn.transaction():
            await setup_db(conn)
            await user.create_super_user(conn, config.SUPERUSER)


async def execute(pool: Pool, query: str, *args, **kwargs):
    async with pool.acquire() as conn:
        async with conn.transaction():
            await conn.execute(query, *args, **kwargs)


async def setup_db(db: Connection):
    sql = """
    CREATE TABLE IF NOT EXISTS users(
    id int PRIMARY KEY,
    created_at timestamp DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp DEFAULT CURRENT_TIMESTAMP,
    is_stoped bool DEFAULT false,
    is_superuser bool DEFAULT false
    )
    """
    await db.execute(sql)

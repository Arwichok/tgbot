import logging
import sys

from asyncpg import create_pool
from asyncpg.pool import Pool

from ..utils import config
from .user import setup_user

logger = logging.getLogger(__name__)


def init_pool() -> Pool:
    return create_pool(**config.PGCONFIG)


async def startup_db(pool: Pool):
    try:
        await pool
        async with pool.acquire() as conn:
            async with conn.transaction():
                await setup_user(conn)
    except ConnectionRefusedError as e:
        logger.error(f"Filed connection to Postgresql: {e}")
        sys.exit(1)

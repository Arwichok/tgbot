from dataclasses import dataclass
from datetime import datetime

from asyncpg import Connection

from ..utils import config


@dataclass
class User:
    id: int
    created_at: datetime
    updated_at: datetime
    is_stopped: bool
    is_superuser: bool


async def setup(db: Connection):
    await create_table(db)
    await create_super_user(db, config.SUPERUSER)


async def create_table(db: Connection):
    sql = """
    CREATE TABLE IF NOT EXISTS users(
    id int PRIMARY KEY,
    created_at timestamp DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp DEFAULT CURRENT_TIMESTAMP,
    is_stopped bool DEFAULT false,
    is_superuser bool DEFAULT false
    )
    """
    await db.execute(sql)


async def create_user(db: Connection, user_id: int):
    sql = """
    INSERT INTO users(id) VALUES($1)
    ON CONFLICT (id) DO UPDATE SET
    (updated_at, is_stopped) = (CURRENT_TIMESTAMP, false)
    """
    await db.execute(sql, user_id)


async def create_super_user(db: Connection, user_id: int, is_superuser=True):
    sql = """
    INSERT INTO users (id, is_superuser) VALUES ($1, $2)
    ON CONFLICT (id) DO UPDATE SET is_superuser=$2;
    """
    await db.execute(sql, user_id, is_superuser)


async def stopped_by_user(db: Connection, user_id: int):
    sql = """
    UPDATE users SET is_stopped=true WHERE id=$1
    """
    await db.execute(sql, user_id)


async def get(db: Connection, user_id: int) -> User:
    sql = '''
    SELECT * FROM users WHERE id=$1
    '''
    user_row = await db.fetchrow(sql, user_id)
    return User(**user_row)

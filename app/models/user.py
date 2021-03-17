from dataclasses import dataclass
from datetime import datetime

from asyncpg import Connection

from ..utils import config


@dataclass
class User:
    db: Connection
    id: int
    created_at: datetime
    updated_at: datetime
    start_conversation: bool
    do_not_disturb: bool
    is_superuser: bool = False

    @classmethod
    async def create(cls, db: Connection, user_id: int):
        sql = """
        INSERT INTO users (id) VALUES ($1)
        ON CONFLICT (id) DO NOTHING
        """
        await db.execute(sql, user_id)
        return await cls.get(db, user_id)

    @classmethod
    async def get(cls, db: Connection, user_id: int):
        sql = "SELECT * FROM users WHERE id=$1"
        row_user = await db.fetchrow(sql, user_id)
        return User(db, **row_user) if row_user else None

    @classmethod
    async def create_table(cls, db: Connection):
        sql = """
        CREATE TABLE IF NOT EXISTS users (
            id int PRIMARY KEY,
            created_at timestamptz DEFAULT CURRENT_TIMESTAMP,
            updated_at timestamptz DEFAULT CURRENT_TIMESTAMP,
            start_conversation bool DEFAULT false,
            do_not_disturb bool DEFAULT true,
            is_superuser bool DEFAULT false
        )
        """
        await db.execute(sql)

    @classmethod
    async def start_conversation(cls, db: Connection, user_id: int):
        sql = """
        INSERT INTO users (id, start_conversation, do_not_disturb)
        VALUES ($1, true, false) ON CONFLICT (id)
        DO UPDATE SET (start_conversation, do_not_disturb) = (true, false)
        """
        await db.execute(sql, user_id)

    @classmethod
    async def do_not_disturb(cls, db: Connection, user_id: int):
        sql = """
        INSERT INTO users (id, do_not_disturb) VALUES ($1, true)
        ON CONFLICT (id) DO UPDATE SET do_not_disturb=true
        """
        await db.execute(sql, user_id)

    @classmethod
    async def create_super(cls, db: Connection, user_id: int):
        sql = """
        INSERT INTO users (id, is_superuser) VALUES ($1, true)
        ON CONFLICT (id) DO UPDATE SET is_superuser=true
        """
        await db.execute(sql, user_id)


async def setup_user(db: Connection):
    await User.create_table(db)
    await User.create_super(db, config.SUPERUSER)


'''
async def create_table(db: Connection):
    sql = """
    CREATE TABLE IF NOT EXISTS users(
    id int PRIMARY KEY,
    created_at timestamp DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp DEFAULT CURRENT_TIMESTAMP,
    start_conversation bool DEFAULT false,
    do_not_disturb bool DEFAULT true,
    is_superuser bool DEFAULT false
    )
    """
    await db.execute(sql)


async def create(db: Connection, user_id: int):
    sql = """
    INSERT INTO users(id) VALUES($1)
    ON CONFLICT (id) DO UPDATE SET
    (updated_at, is_stopped) = (CURRENT_TIMESTAMP, false)
    """
    await db.execute(sql, user_id)
    return await get(db, user_id)


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
    sql = "SELECT * FROM users WHERE id=$1"
    user_row = await db.fetchrow(sql, user_id)
    return User(db=db, **user_row) if user_row else user_row
'''

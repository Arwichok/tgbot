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
    is_superuser: bool
    start: bool = False

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
            created_at timestamptz DEFAULT now(),
            updated_at timestamptz DEFAULT now(),
            is_superuser bool DEFAULT false,
            start bool DEFAULT false
        )
        """
        await db.execute(sql)

    @classmethod
    async def start(cls, db: Connection, user_id: int):
        sql = """
        INSERT INTO users (id, start) VALUES ($1, true)
        ON CONFLICT (id) DO UPDATE SET
            start=true,
            updated_at=now()
        """
        await db.execute(sql, user_id)

    @classmethod
    async def stop(cls, db: Connection, user_id: int):
        sql = """
        INSERT INTO users (id, start) VALUES ($1, false)
        ON CONFLICT (id) DO UPDATE SET
            start=false,
            updated_at=now()
        """
        await db.execute(sql, user_id)

    @classmethod
    async def create_super(cls, db: Connection, user_id: int):
        sql = """
        INSERT INTO users (id, is_superuser) VALUES ($1, true)
        ON CONFLICT (id) DO UPDATE SET
            is_superuser=true,
            updated_at=now()
        """
        await db.execute(sql, user_id)

    @classmethod
    async def restrict_super(cls, db: Connection, user_id: int):
        sql = """
        INSERT INTO users (id, is_superuser) VALUES ($1, false)
        ON CONFLICT (id) DO UPDATE SET
            is_superuser=false,
            updated_at=now()
        """
        await db.execute(sql, user_id)


async def setup_user(db: Connection):
    await User.create_table(db)
    await User.create_super(db, config.SUPERUSER)

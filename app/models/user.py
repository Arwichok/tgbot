from asyncpg import Connection


async def create_user(db: Connection, user_id: int):
    sql = """
    INSERT INTO users(id) VALUES($1)
    ON CONFLICT (id) DO UPDATE SET
    (updated_at, is_stoped) = (CURRENT_TIMESTAMP, false)
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
    UPDATE users SET is_stoped=true WHERE id=$1
    """
    await db.execute(sql, user_id)

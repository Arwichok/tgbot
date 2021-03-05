CREATE TABLE IF NOT EXISTS users(
    id int PRIMARY KEY,
    started_at date
    is_stoped bool,
    is_superuser bool SET DEFAULT false
)

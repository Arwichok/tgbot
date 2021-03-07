

class DBMiddleware():
    def __init__(self, db_pool):
        self._db_pool = db_pool

from .util import get_conn

class DatabaseOperation:
    def __init__(self, db_name):
        self.db_name = db_name

    def create(self):
        conn = get_conn(self.db_name)
        if conn:
            print("database %s created successfully.....\n" % self.db_name)

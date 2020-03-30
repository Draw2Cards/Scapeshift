import sqlite3


class DatabaseManager:
    def __init__(self):
        self.table = "cards"
        self.conn = None
        self.cursor = None
        self.__init = False

    def __del__(self):
        assert self.__init is False

    def init(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        if not self.is_table_exists(self.table):
            self.create_table(self.table)
        self.__init = True

    def is_table_exists(self, table):
        is_exists = False
        self.cursor("SELECT count(name) FROM sqlite_master WHERE type='table' AND name=':table'", {'table', table})
        if self.cursor.fetchone()[0] == 1:
            is_exists = True
        return is_exists

    def create_table(self, table):
        self.cursor.execute("""CREATE TABLE ':table' (
                    name text,
                    cmc integer,
                    mana_cost text,
                    type_line text,
                    import_date text
                    )""", {'table', table})
        self.conn.commit()

    def close(self):
        self.conn.close()
        self.__init = False

    def find(self, name):
        self.cursor.execute("SELECT * FROM cards WHERE name=':name'", {'name': name})
        row = self.cursor.fetchone()
        return row

    def insert(self, row):
        # TODO
        self.conn.commit()

    def find_outdated_cards(self):
        pass

    def update(self, rows):
        pass

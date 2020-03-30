import sqlite3


class DatabaseManager:
    def __init__(self):
        self.table = "cards"
        self.db_path = "cards.db"
        self.conn = None
        self.cursor = None
        self.__init = False

    def __del__(self):
        assert self.__init is False

    def init(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        if not self._is_table_exists():
            self._create_table()
        self.__init = True

    def _is_table_exists(self):
        is_exists = True
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='cards'")
        if not self.cursor.fetchone():
            is_exists = False
        return is_exists

    def _create_table(self):
        self.cursor.execute("""CREATE TABLE cards (
                    name text,
                    cmc real,
                    mana_cost text,
                    type_line text,
                    import_date text
                    )""")
        self.conn.commit()

    def close(self):
        self.conn.close()
        self.__init = False

    def find(self, name):
        self.cursor.execute("SELECT * FROM cards WHERE name='Valakut, the Molten Pinnacle'")
        row = self.cursor.fetchone()
        return row

    def insert(self, data):
        import_date = "test"
        self.cursor.execute("INSERT INTO cards VALUES (?, ?, ?, ?, ?)", (data["name"], data["cmc"], data["mana_cost"], data["type_line"], import_date))
        self.conn.commit()

    def find_outdated_cards(self):
        pass

    def update(self, rows):
        pass

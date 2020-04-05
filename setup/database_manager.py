import sqlite3
from datetime import date


class DatabaseManager:
    def __init__(self):
        self.db_path = "../cards.db"
        self.conn = None
        self.cursor = None
        self.__init = False

    def __del__(self):
        assert self.__init is False

    def init(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self._create_table()
        self.__init = True

    def _create_table(self):
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS cards (
            name text, 
            cmc real, 
            mana_cost text, 
            type_line text, 
            import_date text,
            UNIQUE(name))""")
        self.conn.commit()

    def close(self):
        self.conn.close()
        self.__init = False

    def find(self, name):
        self.cursor.execute("SELECT * FROM cards WHERE name=?", (name,))
        row = self.cursor.fetchone()
        return row

    def insert(self, data):
        self.cursor.execute("INSERT INTO cards VALUES (?, ?, ?, ?, ?)",
                            (data["name"], data["cmc"], data["mana_cost"], data["type_line"], date.today()))
        self.conn.commit()

    def find_outdated_cards(self):
        pass

    def update(self, rows):
        pass

    def pint_table(self):
        self.cursor.execute("SELECT * FROM cards")
        rows = self.cursor.fetchall()
        if not rows:
            print("Table is empty.")
        else:
            for row in rows:
                print(row)
            print("Count: {}".format(len(rows)))


if __name__ == "__main__":
    db_manager = DatabaseManager()
    db_manager.init()
    db_manager.pint_table()
    db_manager.close()

import sqlite3

class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)

    def disconnect(self):
        self.conn.close()

    def create_table(self, table_name):
        self.connect()
        self.conn.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ("
                          f"id INTEGER PRIMARY KEY AUTOINCREMENT,"
                          f"player1_name TEXT,"
                          f"player2_name TEXT,"
                          f"player1_score INTEGER,"
                          f"player2_score INTEGER,"
                          f"winner TEXT,"
                          f"datetime DATETIME DEFAULT CURRENT_TIMESTAMP)")
        self.disconnect()

    def insert_data(self, table_name, data):
        self.connect()
        self.conn.execute(f"INSERT INTO {table_name} (player1_name, player2_name, "
                          f"player1_score, player2_score, winner) "
                          f"VALUES (?, ?, ?, ?, ?)", data)
        self.conn.commit()
        self.disconnect()

    def get_all_data(self, table_name):
        self.connect()
        data = self.conn.execute(f"SELECT * FROM {table_name}")
        result = data.fetchall()
        self.disconnect()
        return result

    def get_last_data(self, table_name):
        self.connect()
        data = self.conn.execute(f"SELECT * FROM {table_name} ORDER BY datetime DESC LIMIT 1")
        result = data.fetchone()
        self.disconnect()
        return result

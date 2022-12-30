import sqlite3

class DBHandler:
    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        try:
            self.create_table()
        except:
            pass
    def create_table(self):
        self.conn.execute('''CREATE TABLE accounts
                (ACCOUNT           TEXT    NOT NULL,
                N_MESSAGES          INT     NOT NULL);''')
        self.conn.commit()
    def add_record(self, account, n_messages):
        self.conn.execute(f"""INSERT INTO ACCOUNTS VALUES('{account}', {n_messages});""")
        self.conn.commit()
    def get_record(self, account):
        cursor = self.conn.execute(f'SELECT * FROM accounts WHERE account="{account}";')
        return cursor.fetchone()
    def update_record(self, account, n_messages):
        self.conn.execute(f'UPDATE  ACCOUNTS SET N_MESSAGES={n_messages} WHERE account="{account}";')
        self.conn.commit()
        
import sqlite3


class DataSource:
    database = "file_backup.db"  # SQLite database file

    def __init__(self):
        self.connection = None
        self._connect()

    def _connect(self):
        try:
            self.connection = sqlite3.connect(self.database)
            print("Connected successfully to the database")
        except sqlite3.Error as err:
            raise ConnectionError(f"Connection error: {err}")

    def create_cursor(self):
        if not self.connection:
            raise ConnectionError("Connection not established. Call connect() first.")
        return self.connection.cursor()

    def execute(self, query, params=None):
        cursor = self.create_cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if query.strip().lower().startswith("select"):
                return cursor.fetchall()
            else:
                self.connection.commit()  # Commit for INSERT, UPDATE, DELETE, etc.
        except sqlite3.Error as err:
            raise Exception(f"Error executing query: {err}")

    def execute_many(self, query, params_list):
        cursor = self.create_cursor()
        try:
            cursor.executemany(query, params_list)
            self.connection.commit()
        except sqlite3.Error as err:
            raise Exception(f"Error executing query: {err}")

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            print("Connection Successfully Disconnected")

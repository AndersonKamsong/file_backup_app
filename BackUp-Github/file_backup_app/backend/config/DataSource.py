import configparser
from configparser import ConfigParser

import mysql.connector


class DataSource:
    host = "localhost"
    user = "root"
    password = "root"
    database = "file_backup"

    def __init__(self):
        self.connection = None
        self._connect()

    def _connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print("Connected successfully to the database")
        except mysql.connector.Error as err:
            raise ConnectionError(f"Connection error: {err}")

    def create_cursor(self):
        if not self.connection:
            raise ConnectionError(
                "Connection not established. Call connect() first.")
        return self.connection.cursor()

    def execute(self, query, params=None):
        cursor = self.create_cursor()
        try:
            cursor.execute(query, params)
            if not query.lower().startswith("select"):
                # Commit for INSERT, UPDATE, DELETE, etc.
                self.connection.commit()
            return cursor.fetchall()  # Fetch all rows by default
        except mysql.connector.Error as err:
            raise Exception(f"Error executing query: {err}")
        # finally:
            # cursor.close()

    def execute_many(self, query, params_list):
        # # Execute with multiple rows (using execute_many)
        # data = [('Alice Smith',), ('Bob Jones',)]
        # db.execute_many("INSERT INTO customers (name) VALUES (%s)", data)

        cursor = self.create_cursor()
        try:
            cursor.executemany(query, params_list)
            self.connection.commit()  # Commit changes after executing multiple rows
        except mysql.connector.Error as err:
            raise Exception(f"Error executing query: {err}")
        # finally:
        #     cursor.close()

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            print("Connection Successfully Disconnected")
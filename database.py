import sqlite3


class DataBase:
    def __init__(self, file):
        super().__init__()
        self.file_connect(file)
        print("База данных подключена")

    def file_connect(self, file):
        self.connection = sqlite3.connect(file)
        self.cursor = self.connection.cursor()

    def execute(self, com):
        self.cursor.execute(com)

    def select(self, frm, select="*", where=""):
        self.execute(f"SELECT {select} FROM {frm} {where}")

    def insert(self, table, columns, values):
        self.execute(f"INSERT INTO {table} ({columns}) VALUES ({values})")

    def update(self, table, col, value, where=""):
        self.execute(f"UPDATE {table} SET {col}={value} {where}")

    def delete(self, frm, where):
        self.execute(f"DELETE FROM {frm} WHERE {where}")
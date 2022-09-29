import sqlite3
from os import path
from datetime import datetime


class Database:
    def __init__(self, db_name):
        self.database = db_name
        self.connect = sqlite3.connect(self.database)
        self.db_connect()

    def db_connect(self):
        with self.connect as connection:
            self.cursor = connection.cursor()
    
    def check_if_exist(self):
        if not path.isfile(self.database):
            self.create_db()
        return True
        
    def create_db(self):
        self.cursor.execute(
             """CREATE TABLE IF NOT EXISTS book (id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL, mail TEXT NOT NULL, book_name TEXT, date TEXT)""")           

    def get_content(self, column = 'id', id = None):
        content = []
        if id:
            self.cursor.execute(
                 f"SELECT id, name, mail, book_name, date FROM book WHERE {column} IS ?", (id,)
            )
        else:
            self.cursor.execute("SELECT id, name, mail, book_name, date FROM book")
        
        for entry_id, name, mail, book_name, date in self.cursor.fetchall():
            content.append(
                {'id': entry_id, 'name' : name,
                'mail' : mail, 'book_name' : book_name,
                'date' : date}
                )
        return content

    def put_content(self, name, mail, book_name, date = datetime.now()):
        self.cursor.execute(
            "INSERT INTO book(name, mail, book_name, date) VALUES (?, ?, ?, ?)",
            (name, mail, book_name, date)
        )

    def delete_content(self, column = 'id', id = not None):
        self.cursor.execute(f"DELETE FROM book WHERE {column} IS ?", (id,))

    def __del__(self):
        del self.cursor
        self.connect.commit()
        self.connect.close()
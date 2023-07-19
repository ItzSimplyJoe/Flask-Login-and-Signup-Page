import sqlite3
import hashlib
from flask import g

DATABASE = 'static/database/database.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = Database()
    return db


class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE)
        self.cursor = self.conn.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)')
        self.conn.commit()

    def insert(self, username, password):
        self.cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, self.hashpassword(password)))
        self.conn.commit()

    def fetch(self, username):
        self.cursor.execute('SELECT * FROM users WHERE username=?', (username,))
        return self.cursor.fetchall()

    def login(self, username, password):
        self.cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, self.hashpassword(password)))
        return self.cursor.fetchall()

    def hashpassword(self, password):
        password = hashlib.sha256(password.encode()).hexdigest()
        return password

import sqlite3, os, pathlib
from werkzeug.security import generate_password_hash

DB_PATH = os.environ.get("DB_PATH", "demo.sqlite3")

pathlib.Path(DB_PATH).unlink(missing_ok=True)
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()
cur.executescript(
    '''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    );
    CREATE TABLE posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        body TEXT NOT NULL
    );
    '''
)
cur.executemany(
    "INSERT INTO users(username, password) VALUES (?, ?)",
    [
        ("alice", generate_password_hash("alice123")),
        ("bob", generate_password_hash("bob12345")),
    ],
)
cur.executemany(
    "INSERT INTO posts(title, body) VALUES (?, ?)",
    [
        ("Welcome", "This is a demo post."),
        ("Security Tips", "Never trust user input. Use parameterized queries."),
    ],
)
conn.commit()
conn.close()
print(f"Initialized secure SQLite DB at {DB_PATH}")

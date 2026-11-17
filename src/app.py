from flask import Flask, request, render_template, redirect, make_response, session
from markupsafe import escape
from werkzeug.security import check_password_hash
import os
import logging
import sqlite3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
)

DB_PATH = os.environ.get("DB_PATH", "demo.sqlite3")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.after_request
def set_security_headers(response):
    response.headers["Content-Security-Policy"] = "default-src 'self'; style-src 'self' 'unsafe-inline'"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/echo")
def echo():
    msg = escape(request.args.get("msg", ""))
    return f"<h1>Echo</h1><p>{msg}</p>"

@app.route("/search")
def search():
    q = request.args.get("q", "")
    conn = get_db()
    cur = conn.cursor()
    like_q = f"%{q}%"
    rows = cur.execute(
        "SELECT id, title, body FROM posts WHERE title LIKE ? OR body LIKE ?",
        (like_q, like_q),
    ).fetchall()
    return render_template("search.html", q=q, rows=rows, sql="[Parameterized query]")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        conn = get_db()
        cur = conn.cursor()
        row = cur.execute("SELECT id, username, password FROM users WHERE username = ?", (username,)).fetchone()
        if row and check_password_hash(row["password"], password):
            session["user_id"] = row["id"]
            logging.info("Successful login for '%s' from %s", username, request.remote_addr)
            return make_response(redirect("/profile"))
        logging.warning("Failed login for '%s' from %s", username, request.remote_addr)
        return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route("/profile")
def profile():
    if "user_id" not in session:
        return redirect("/login")
    conn = get_db()
    cur = conn.cursor()
    user = cur.execute("SELECT id, username FROM users WHERE id = ?", (session["user_id"],)).fetchone()
    return render_template("profile.html", user=user)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)

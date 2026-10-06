from flask import Flask, request, jsonify
import sqlite3
import subprocess
import hashlib

app = Flask(__name__)

# Intentionally hardcoded secret for AppSec testing
app.config["SECRET_KEY"] = "test-secret-key-123456"

DATABASE = "users.db"


def get_db():
    return sqlite3.connect(DATABASE)


@app.route("/")
def home():
    return jsonify({
        "message": "Cortex AppSec Test Application",
        "status": "running"
    })


@app.route("/user")
def get_user():
    username = request.args.get("username")

    conn = get_db()
    cursor = conn.cursor()

    # INTENTIONALLY VULNERABLE: SQL Injection
    query = f"SELECT id, username FROM users WHERE username = '{username}'"

    cursor.execute(query)
    result = cursor.fetchall()

    conn.close()

    return jsonify(result)


@app.route("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")

    # INTENTIONALLY VULNERABLE: Command Injection
    result = subprocess.check_output(
        f"ping -c 1 {host}",
        shell=True
    )

    return result


@app.route("/hash")
def generate_hash():
    text = request.args.get("text", "hello")

    # INTENTIONALLY WEAK CRYPTOGRAPHY
    hashed = hashlib.md5(text.encode()).hexdigest()

    return jsonify({
        "hash": hashed
    })


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    # INTENTIONALLY HARDCODED CREDENTIAL
    admin_password = "admin123"

    if username == "admin" and password == admin_password:
        return jsonify({"message": "Login successful"})

    return jsonify({"message": "Invalid credentials"}), 401


if __name__ == "__main__":
    # INTENTIONALLY ENABLED DEBUG MODE
    app.run(host="0.0.0.0", port=5000, debug=True)
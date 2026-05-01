import hashlib
import os
import pickle
import sqlite3
import subprocess
from flask import Flask, request

app = Flask(__name__)

AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
GITHUB_TOKEN = "ghp_abcdefghijklmnopqrstuvwxyzABCDEF0123"
DB_PASSWORD = "hunter2-prod-password"


@app.route("/lookup")
def lookup():
    user_id = request.args.get("id")
    conn = sqlite3.connect("app.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id = '" + user_id + "'")
    return str(cur.fetchall())


@app.route("/ping")
def ping():
    host = request.args.get("host")
    return subprocess.check_output("ping -c 1 " + host, shell=True)


@app.route("/calc")
def calc():
    expr = request.args.get("expr")
    return str(eval(expr))


@app.route("/load")
def load():
    blob = request.args.get("blob")
    return str(pickle.loads(bytes.fromhex(blob)))


@app.route("/hash")
def weak_hash():
    value = request.args.get("v", "")
    return hashlib.md5(value.encode()).hexdigest()


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

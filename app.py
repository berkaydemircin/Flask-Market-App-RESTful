import sqlite3
import os
from werkzeug.security import check_password_hash, generate_password_hash
from helper import login_required, displayError
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_session import Session

app = Flask(__name__)
app.debug = True

# FOR API
load_dotenv("sensitive.env")
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET")
jwt = JWTManager(app)

# FOR NORMAL USERS
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Establishing DB connection
def get_db_connection():
    conn = sqlite3.connect('swift_market.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row  # To return rows as dictionaries
    return conn
conn = get_db_connection()
cursor = conn.cursor()

if (__name__) == "__main__":
    app.run()


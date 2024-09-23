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

    
# BELOW ARE API RELATED ENDPOINTS

# To register a new vendor
@app.route('/api/vendors', methods=['POST'])
def api_register():
    data = request.get_json()

    required_fields = ['username', 'password', 'display_name', 'description', 'contact_info']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'missing field: {field}'}), 400

    # Data of newly registered vendor
    username = data['username']
    password = data['password']
    display_name = data['display_name']
    description = data['description']
    contact_info = data['contact_info']

    hash = generate_password_hash(password, method='pbkdf2', salt_length=16)

    try:
        cursor.execute("INSERT INTO vendors (name, hash, store_name, description, contact_info) VALUES (?, ?, ?, ?, ?)"
                       ,(username, hash, display_name, description, contact_info))
        conn.commit()
    except sqlite3.Error as e:
        print(e)
        return jsonify({'error': 'SQL error', 'details': str(e)}), 500
    
    return jsonify({'status': 'success'})

# To get a JWT (login)
@app.route('/api/token', methods=['POST'])
def api_token():
    data = request.get_json()

    required_fields = ['username', 'password']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'missing field: {field}'}), 400
        
    username = data['username']
    password = data['password']
    
    try:
        cursor.execute("SELECT hash, vendor_id FROM vendors WHERE name = ?", (username,))
    except sqlite3.Error as e:
        print(e)
        return jsonify({'error': 'SQL error', 'details': str(e)}), 500
    
    # Validate credentials, generate JWT for API clients
    row = cursor.fetchall()
    print(row)
    print(len(row))
    if len(row) != 1 or not check_password_hash(row[0]["hash"], password):
        return jsonify({'error': 'invalid credentials'})
    else:
        access_token = create_access_token(identity=username)
        return jsonify({'access_token': access_token})

@app.route('/api/vendors/<int:id>', methods=['GET'])
def api_vendors(id):
    try:
        cursor.execute("SELECT store_name, description, contact_info FROM vendors WHERE vendor_id = ?", (id,))
    except sqlite3.Error as e:
        return jsonify({'error': 'SQL error', 'details': str(e)}), 500
        
    vendorInfo = dict(cursor.fetchone())
    return jsonify(vendorInfo), 200

# To update vendor info
@app.route('/api/vendors/<int:id>/update', methods=['PUT'])
@jwt_required()
def api_vendors_update(id):
    vendor = get_jwt_identity()
    cursor.execute("SELECT vendor_id FROM vendors WHERE name = ?", (vendor,))
    row = cursor.fetchone()

    if row is None:
        return jsonify({'error': 'vendor not found'}), 404
    if id != row["vendor_id"]:
        return jsonify({'error': 'not authorized to edit other vendors'}), 403

    data = request.get_json()

    # Check if required fields are present
    required_fields = ['display_name', 'description', 'contact_info']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'missing field: {field}'}), 400
        
    display_name = data['display_name']
    description = data['description']
    contact_info = data['contact_info']

    # Updating vendor info
    try:
        cursor.execute("UPDATE vendors SET store_name = ? , description = ? , contact_info = ? WHERE vendor_id = ?"
                       ,(display_name, description, contact_info, id))
        conn.commit()
    except sqlite3.Error as e:
        return jsonify({'error': 'SQL error', 'details': str(e)}), 500

    return jsonify({'status': 'success'}), 200

if (__name__) == "__main__":
    app.run()
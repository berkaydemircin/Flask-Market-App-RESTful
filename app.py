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

# BELOW ARE NON API ENDPOINTS

@app.route("/")
@login_required
def index():
    cursor.execute("SELECT item_name, stock, price, vendors.store_name FROM items JOIN vendors ON items.vendor_id = vendors.vendor_id LIMIT 8")
    items = cursor.fetchall()
    return render_template("index.html", items=items)

# Register user
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username:
            return displayError("Must provide username", 400)
        elif not password:
            return displayError("Must provide password", 400)
        elif not password == request.form.get("confirmation"):
            return displayError("Passwords must match", 400)

        name = username
        passwordHash = generate_password_hash(password, method='pbkdf2', salt_length=16)

        try:
            cursor.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (name, passwordHash,))
            conn.commit()
            return redirect("/login")
        except ValueError:
            return displayError("User already registered", 400)

    else:
        return render_template("register.html")

# User logs in
@app.route("/login", methods=["GET", "POST"])
def login():

    session.clear()

    # POST route
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        # Ensure username was submitted
        if not username:
            return displayError("Must provide username", 403)

        # Ensure password was submitted
        elif not password:
            return displayError("Must provide password", 403)

        # Query database for username
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()

        # Ensure username exists and password is correct
        if not check_password_hash(row["hash"], password):
            return displayError("Invalid username and/or password", 403)

        # Remember user    
        session["user_id"] = row["user_id"]

        return redirect("/")
    
    # GET route
    else:
        return render_template("login.html")

# Items
@app.route("/items", methods=["GET", "POST"])
@login_required
def items():
    if request.method == "GET":
        cursor.execute("SELECT item_name, stock, price, vendors.store_name FROM items JOIN vendors ON items.vendor_id = vendors.vendor_id")
        items = cursor.fetchall()
        return render_template("items.html", items=items)
    else:
        name = request.form.get("name")
        cursor.execute("SELECT item_name, stock, price, vendors.store_name FROM items JOIN vendors ON items.vendor_id = vendors.vendor_id WHERE item_name LIKE ?"
                       , ("%" + name + "%",))
        items = cursor.fetchall()
        return render_template("items.html", items=items)

# Vendors
@app.route("/vendors", methods=["GET", "POST"])
@login_required
def vendors():
    if request.method == "GET":
        cursor.execute("SELECT store_name, description, contact_info FROM vendors")
        vendors = cursor.fetchall()
        return render_template("vendors.html", vendors=vendors)
    else:
        try:
            name = request.form.get("name")
            cursor.execute("SELECT vendor_id, store_name, description, contact_info FROM vendors WHERE store_name LIKE ?"
                        , ("%" + name + "%",))
            vendors = cursor.fetchall()
            cursor.execute("SELECT item_name, stock, price FROM items WHERE items.vendor_id IN (SELECT vendor_id FROM vendors WHERE store_name LIKE ?)"
                        , ("%" + name + "%",))
            items = cursor.fetchall()
            return render_template("vendors.html", vendors=vendors, items=items)
        except sqlite3.Error as e:
            return displayError(print(e.sqlite_errorname))

# User logs out
@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    flash("Succesfully logged out.")
    return redirect("/")

    
# BELOW ARE API RELATED ENDPOINTS

# To register a new vendor
@app.route('/api/vendors', methods=['POST'])
def api_vendors_create():
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
    row = cursor.fetchone()

    id = row["vendor_id"]
    if not check_password_hash(row["hash"], password):
        return jsonify({'error': 'invalid credentials'})
    else:
        access_token = create_access_token(identity=id)
        return jsonify({'access_token': access_token})

# To see a single vendors details
@app.route('/api/vendors/<int:id>', methods=['GET'])
def api_vendors_details(id):
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

    if id != vendor:
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

# To view all items of vendor
@app.route('/api/vendors/<int:id>/items', methods=['GET'])
@jwt_required()
def api_vendors_items(id):
    vendor = get_jwt_identity()

    if id != vendor:
        return jsonify({'error': 'not authorized to view other vendors stock'}), 403

    try:
        cursor.execute('SELECT * FROM items WHERE vendor_id = ?', (vendor,))
        items = cursor.fetchall()
    except sqlite3.Error as e:
        return jsonify({'error': 'SQL error', 'details': str(e)}), 500
    
    items_list = [
        {
            'item_id': item['item_id'],
            'item_name': item['item_name'],
            'vendor_id': item['vendor_id'],
            'stock': item['stock'],
            'price': item['price']
        } for item in items
    ]

    return jsonify({
        'vendor_id': vendor,
        'items': items_list
    })

# Create new items for the vendor
@app.route("/api/items", methods=["POST"])
@jwt_required()
def api_items():
    vendor = get_jwt_identity()

    data = request.get_json()

    # Check if required fields are present
    required_fields = ['item_name', 'stock', 'price']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'missing field: {field}'}), 400
        
    item_name = data['item_name']
    stock = data['stock']
    price = data['price']

    # Updating vendor info
    try:
        cursor.execute("INSERT INTO items ('item_name', 'vendor_id', 'stock', 'price') VALUES (?, ?, ?, ?)"
                       ,(item_name, vendor, stock, price))
        conn.commit()
    except sqlite3.Error as e:
        return jsonify({'error': 'SQL error', 'details': str(e)}), 500

    return jsonify({'status': 'success'}), 200

# To see a specific items details
@app.route('/api/items/<int:id>', methods=['GET'])
@jwt_required()
def api_item_details(id):

    try:
        cursor.execute('SELECT * FROM items WHERE item_id = ?', (id,))
        item = cursor.fetchone()
    except sqlite3.Error as e:
        return jsonify({'error': 'SQL error', 'details': str(e)}), 500
    
    # If ID doesnt exist
    if item is None:
        return jsonify({"error": "no such item with id exists"})

    return jsonify({
            'item_id': item["item_id"],
            'item_name': item["item_name"],
            'vendor_id': item["vendor_id"],
            'stock': item["stock"],
            'price': item["price"]
            })

# Delete an item
@app.route('/api/items/<int:id>/delete', methods=['DELETE'])
@jwt_required()
def api_item_delete(id):
    vendor = get_jwt_identity()
    cursor.execute("SELECT item_id FROM items WHERE items.vendor_id = ? AND item_id = ?", (vendor, id))
    row = cursor.fetchone()

    if row is None:
        return jsonify({'error': 'item not found, it may not belong to you'}), 404
    
    try:
        cursor.execute("DELETE FROM items WHERE item_id = ?", (id,))
        conn.commit()
    except sqlite3.Error as e:
        return jsonify({'error': 'SQL error', 'details': str(e)}), 500
    
    return jsonify({"status": "success"})

if (__name__) == "__main__":
    app.run()
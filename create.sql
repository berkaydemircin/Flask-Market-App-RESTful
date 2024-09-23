CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    hash TEXT NOT NULL,
    money NUMERIC NOT NULL DEFAULT 250.00
);

CREATE TABLE vendors (
    vendor_id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    hash TEXT NOT NULL,
    store_name TEXT NOT NULL,
    description TEXT,
    contact_info TEXT
);

CREATE TABLE items (
    item_id INTEGER PRIMARY KEY,
    item_name TEXT NOT NULL,
    vendor_id INTEGER,
    stock INTEGER NOT NULL CHECK (stock >= 0),
    price NUMERIC NOT NULL CHECK (price >= 0),
    FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id) ON DELETE CASCADE
);

/* This feature is not yet supported and might be scrapped
CREATE TABLE ratings (
    review_id INTEGER PRIMARY KEY,
    item_id INTEGER,
    user_id INTEGER,
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (item_id) REFERENCES Items(item_id) ON DELETE CASCADE,
);
*/
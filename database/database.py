import sqlite3

# ==========================================
# CONNECT DATABASE
# ==========================================

conn = sqlite3.connect("retailmind.db")
cursor = conn.cursor()

# ==========================================
# PRODUCTS TABLE
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    barcode TEXT UNIQUE,

    product_name TEXT NOT NULL,

    brand TEXT,

    category TEXT,

    unit TEXT,

    purchase_price REAL,

    selling_price REAL,

    stock INTEGER DEFAULT 0,

    min_stock INTEGER DEFAULT 10,

    supplier TEXT,

    market TEXT,

    gst REAL DEFAULT 0,

    hsn_code TEXT,

    expiry_date TEXT,

    rack_no TEXT,

    status TEXT DEFAULT 'Active'

)
""")

# ==========================================
# CUSTOMERS TABLE
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    customer_name TEXT,

    mobile TEXT,

    email TEXT,

    address TEXT,

    loyalty_points INTEGER DEFAULT 0,

    total_purchase REAL DEFAULT 0

)
""")

# ==========================================
# SUPPLIERS TABLE
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS suppliers (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    supplier_name TEXT,

    mobile TEXT,

    email TEXT,

    address TEXT,

    gst_number TEXT

)
""")

# ==========================================
# BILLS TABLE
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS bills (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    bill_no TEXT,

    customer_name TEXT,

    bill_date TEXT,

    total_amount REAL,

    payment_mode TEXT

)
""")

# ==========================================
# BILL ITEMS TABLE
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS bill_items (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    bill_no TEXT,

    product_name TEXT,

    quantity INTEGER,

    price REAL,

    total REAL

)
""")

# ==========================================
# USERS TABLE
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT UNIQUE,

    password TEXT,

    role TEXT

)
""")

# ==========================================
# SETTINGS TABLE
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS settings (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    shop_name TEXT,

    owner_name TEXT,

    mobile TEXT,

    email TEXT,

    address TEXT,

    gst_number TEXT

)
""")

conn.commit()
conn.close()

print("RetailMind Database Created Successfully")
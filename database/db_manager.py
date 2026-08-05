import sqlite3
import os
import pandas as pd
from typing import Dict, List, Tuple, Any, Optional

DB_FILE = "retailmind.db"

class DatabaseManager:
    """
    Enterprise Data Access Layer (DAL) for RetailMind AI.
    Handles thread-safe SQLite connections, normalized schema creation, 
    indexing, and parameterized safe SQL operations.
    """

    @staticmethod
    def get_connection() -> sqlite3.Connection:
        conn = sqlite3.connect(DB_FILE, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

    @classmethod
    def init_database(cls) -> None:
        with cls.get_connection() as conn:
            c = conn.cursor()

            # 1. Products Table
            c.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                barcode TEXT UNIQUE,
                product_name TEXT NOT NULL,
                name TEXT,
                brand TEXT,
                category TEXT NOT NULL,
                unit TEXT DEFAULT 'pcs',
                purchase_price REAL DEFAULT 0,
                selling_price REAL DEFAULT 0,
                price REAL DEFAULT 0,
                stock INTEGER DEFAULT 50,
                min_stock INTEGER DEFAULT 10,
                stock_status TEXT DEFAULT '🟢 Healthy',
                market TEXT DEFAULT 'Nashik Mandi',
                supplier TEXT DEFAULT 'Standard Supplier',
                gst REAL DEFAULT 5,
                hsn_code TEXT,
                expiry_date TEXT,
                rack_no TEXT,
                status TEXT DEFAULT 'Active'
            )
            """)

            # 2. Customers Table
            c.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                mobile TEXT UNIQUE,
                email TEXT,
                address TEXT,
                loyalty_points INTEGER DEFAULT 0,
                total_purchase REAL DEFAULT 0
            )
            """)

            # 3. Suppliers Table
            c.execute("""
            CREATE TABLE IF NOT EXISTS suppliers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                supplier_name TEXT NOT NULL,
                mobile TEXT,
                email TEXT,
                address TEXT,
                gst_number TEXT,
                category TEXT
            )
            """)

            # 4. Bills Table
            c.execute("""
            CREATE TABLE IF NOT EXISTS bills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bill_no TEXT UNIQUE NOT NULL,
                customer_name TEXT,
                mobile TEXT,
                bill_date TEXT NOT NULL,
                subtotal REAL DEFAULT 0,
                discount REAL DEFAULT 0,
                gst_amount REAL DEFAULT 0,
                total_amount REAL NOT NULL,
                payment_mode TEXT DEFAULT 'Cash'
            )
            """)

            # 5. Bill Items Table
            c.execute("""
            CREATE TABLE IF NOT EXISTS bill_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bill_no TEXT NOT NULL,
                product_name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL,
                gst_pct REAL DEFAULT 5,
                total REAL NOT NULL,
                FOREIGN KEY (bill_no) REFERENCES bills (bill_no)
            )
            """)

            # 6. Users Table
            c.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                role TEXT NOT NULL
            )
            """)

            # 7. Settings Table
            c.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                shop_name TEXT DEFAULT 'RetailMind Supermarket',
                owner_name TEXT DEFAULT 'Suraj V. Shewale',
                mobile TEXT DEFAULT '+91 9876543210',
                email TEXT DEFAULT 'contact@retailmind.ai',
                address TEXT DEFAULT 'Nashik, Maharashtra, India',
                gst_number TEXT DEFAULT '27AAAAA0000A1Z5'
            )
            """)

            # 8. Performance Indexes
            c.execute("CREATE INDEX IF NOT EXISTS idx_products_name ON products(product_name);")
            c.execute("CREATE INDEX IF NOT EXISTS idx_products_category ON products(category);")
            c.execute("CREATE INDEX IF NOT EXISTS idx_products_market ON products(market);")
            c.execute("CREATE INDEX IF NOT EXISTS idx_bills_date ON bills(bill_date);")
            c.execute("CREATE INDEX IF NOT EXISTS idx_customers_mobile ON customers(mobile);")

            conn.commit()

        # Seed data if empty
        cls._seed_initial_data()

    @classmethod
    def _seed_initial_data(cls) -> None:
        with cls.get_connection() as conn:
            c = conn.cursor()
            
            # Seed Products if empty
            c.execute("SELECT COUNT(*) FROM products")
            if c.fetchone()[0] == 0:
                products = [
                    ("RM-BAR-101", "Aashirvaad Shuddh Chakki Atta 5kg", "Aashirvaad Atta", "Aashirvaad", "Grocery & Staples", "kg", 205.0, 245.0, 245.0, 85, 15, "🟢 Healthy", "Nashik Mandi", "ITC Wholesalers", 5, "1101", "2026-12-31", "A-12"),
                    ("RM-BAR-102", "Fortune Sunlite Sunflower Oil 1L", "Fortune Oil", "Fortune", "Edible Oils", "litre", 122.0, 145.0, 145.0, 45, 10, "🟢 Healthy", "Pune Mandi", "Adani Wilmar Dist.", 5, "1512", "2026-11-15", "B-04"),
                    ("RM-BAR-103", "Tata Salt Vacuum Evaporated 1kg", "Tata Salt", "Tata", "Grocery & Staples", "kg", 21.5, 28.0, 28.0, 140, 20, "🟢 Healthy", "Nashik Mandi", "Tata Consumer Products", 5, "2501", "2027-05-20", "A-02"),
                    ("RM-BAR-104", "Amul Butter Pasteurised 500g", "Amul Butter", "Amul", "Dairy & Frozen", "pcs", 240.0, 275.0, 275.0, 8, 12, "🔴 Critical", "Malegaon Mandi", "Amul Dairy Corp", 5, "0405", "2026-08-28", "C-01"),
                    ("RM-BAR-105", "Sugar M-30 Premium Grade 1kg", "Sugar M-30", "Local Wholesale", "Grocery & Staples", "kg", 38.5, 44.0, 44.0, 220, 30, "🟢 Healthy", "Nashik Mandi", "Sahakar Sugar Mill", 5, "1701", "2027-01-10", "A-08"),
                    ("RM-BAR-106", "Nestle Everyday Dairy Whitener 1kg", "Nestle Milk Powder", "Nestle", "Dairy & Frozen", "kg", 385.0, 445.0, 445.0, 18, 10, "🟡 Low", "Pune Mandi", "Nestle India Supplies", 12, "0402", "2026-09-15", "C-03"),
                    ("RM-BAR-107", "Cadbury Dairy Milk Silk 150g", "Dairy Milk Silk", "Cadbury", "Confectionery", "pcs", 142.0, 175.0, 175.0, 60, 15, "🟢 Healthy", "Nashik Mandi", "Mondelez India", 18, "1806", "2026-10-30", "D-05")
                ]
                c.executemany("""
                INSERT INTO products (barcode, product_name, name, brand, category, unit, purchase_price, selling_price, price, stock, min_stock, stock_status, market, supplier, gst, hsn_code, expiry_date, rack_no)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, products)

            # Seed Customers if empty
            c.execute("SELECT COUNT(*) FROM customers")
            if c.fetchone()[0] == 0:
                customers = [
                    ("Rahul Sharma", "9876543210", "rahul@gmail.com", "College Road, Nashik", 120, 4500.0),
                    ("Priya Patil", "9823011223", "priya.patil@outlook.com", "MG Road, Pune", 250, 8900.0),
                    ("Amit Deshmukh", "9422055667", "amit.d@yahoo.com", "Panchavati, Nashik", 85, 3100.0)
                ]
                c.executemany("""
                INSERT INTO customers (customer_name, mobile, email, address, loyalty_points, total_purchase)
                VALUES (?, ?, ?, ?, ?, ?)
                """, customers)

            # Seed Suppliers if empty
            c.execute("SELECT COUNT(*) FROM suppliers")
            if c.fetchone()[0] == 0:
                suppliers = [
                    ("ITC Wholesalers Ltd", "9890123456", "supply@itc.in", "MIDC Ambad, Nashik", "27AAACI1681G1ZM", "Grocery & Staples"),
                    ("Adani Wilmar Distributorship", "9870987654", "sales@adaniwilmar.com", "Hadapsar, Pune", "27AAACA9876B1ZX", "Edible Oils"),
                    ("Amul Dairy Federation", "9822334455", "distributor@amul.coop", "Anand Nagar, Nashik", "27AAAFA1122C1ZY", "Dairy & Frozen")
                ]
                c.executemany("""
                INSERT INTO suppliers (supplier_name, mobile, email, address, gst_number, category)
                VALUES (?, ?, ?, ?, ?, ?)
                """, suppliers)

            # Seed Settings if empty
            c.execute("SELECT COUNT(*) FROM settings")
            if c.fetchone()[0] == 0:
                c.execute("""
                INSERT INTO settings (shop_name, owner_name, mobile, email, address, gst_number)
                VALUES ('RetailMind AI Supermarket', 'Suraj V. Shewale', '+91 9876543210', 'contact@retailmind.ai', 'Nashik, Maharashtra, India', '27AAAAA0000A1Z5')
                """)

            conn.commit()

    @classmethod
    def get_products_dataframe(cls) -> pd.DataFrame:
        with cls.get_connection() as conn:
            df = pd.read_sql_query("SELECT * FROM products ORDER BY id DESC", conn)
            if 'name' not in df.columns or df['name'].isnull().all():
                df['name'] = df['product_name']
            if 'price' not in df.columns or df['price'].isnull().all():
                df['price'] = df['selling_price']
            df['selling_price'] = pd.to_numeric(df['selling_price'], errors='coerce').fillna(0)
            df['purchase_price'] = pd.to_numeric(df['purchase_price'], errors='coerce').fillna(0)
            df['stock'] = pd.to_numeric(df['stock'], errors='coerce').fillna(0).astype(int)
            df['profit_margin'] = df['selling_price'] - df['purchase_price']
            df['margin_pct'] = (df['profit_margin'] / df['selling_price'].replace(0, 1)) * 100
            return df

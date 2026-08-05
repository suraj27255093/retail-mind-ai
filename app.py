import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import re

# =====================================================
# 🛒 RETAILMIND AI — MASTER ENTERPRISE APP ENGINE
# =====================================================

st.set_page_config(
    page_title="RetailMind AI — Smart Enterprise Retail System",
    page_icon="🛒",
    layout="wide"
)

# ── DATABASE AUTO-INITIALIZER ────────────────────────
def init_db():
    conn = sqlite3.connect("retailmind.db")
    c = conn.cursor()
    
    # Products Table
    c.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name TEXT NOT NULL,
        name TEXT,
        brand TEXT,
        category TEXT,
        unit TEXT DEFAULT 'pcs',
        purchase_price REAL DEFAULT 0,
        selling_price REAL DEFAULT 0,
        price REAL DEFAULT 0,
        stock INTEGER DEFAULT 50,
        min_stock INTEGER DEFAULT 10,
        stock_status TEXT DEFAULT '🟢 Healthy',
        market TEXT DEFAULT 'Nashik Mandi',
        supplier TEXT DEFAULT 'Standard Supplier',
        gst REAL DEFAULT 5
    )
    """)
    
    # Seed Products if empty
    c.execute("SELECT COUNT(*) FROM products")
    if c.fetchone()[0] == 0:
        sample_products = [
            ("Aashirvaad Shuddh Chakki Atta 5kg", "Aashirvaad Atta", "Aashirvaad", "Grocery & Staples", "kg", 210.0, 250.0, 250.0, 80, 15, "🟢 Healthy", "Nashik Mandi", "ITC Wholesalers", 5),
            ("Fortune Sunlite Sunflower Oil 1L", "Fortune Oil", "Fortune", "Grocery & Staples", "litre", 115.0, 140.0, 140.0, 45, 10, "🟢 Healthy", "Pune Mandi", "Adani Wilmar Dist.", 5),
            ("Tata Salt Vacuum Evaporated 1kg", "Tata Salt", "Tata", "Grocery & Staples", "kg", 20.0, 28.0, 28.0, 120, 20, "🟢 Healthy", "Nashik Mandi", "Tata Consumer Products", 5),
            ("Amul Butter Pasteurised 500g", "Amul Butter", "Amul", "Dairy & Frozen", "pcs", 235.0, 275.0, 275.0, 8, 10, "🔴 Critical", "Malegaon Mandi", "Amul Dairy Corp", 5),
            ("Sugar M-30 Premium Grade 1kg", "Sugar M-30", "Local Wholesale", "Grocery & Staples", "kg", 36.0, 44.0, 44.0, 200, 30, "🟢 Healthy", "Nashik Mandi", "Sahakar Sugar Mill", 5)
        ]
        c.executemany("""
        INSERT INTO products (product_name, name, brand, category, unit, purchase_price, selling_price, price, stock, min_stock, stock_status, market, supplier, gst)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, sample_products)
        conn.commit()
    conn.close()

try:
    init_db()
except Exception as e:
    pass

# ── GLOBAL CSS DESIGN SYSTEM ─────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

.stApp {
    background: #F8FAFC;
}

.block-container {
    max-width: 1450px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

/* Responsive Metric Styling Fix */
[data-testid="stMetricValue"] {
    font-size: clamp(15px, 1.5vw, 22px) !important;
    font-weight: 800 !important;
    white-space: nowrap !important;
    overflow: visible !important;
}

[data-testid="stMetricLabel"] {
    font-size: clamp(11px, 1vw, 13px) !important;
    font-weight: 700 !important;
    white-space: nowrap !important;
}

[data-testid="stMetric"] {
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 14px !important;
    padding: 10px 14px !important;
}

/* Sidebar Design */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%) !important;
    border-right: 1px solid #334155;
}

section[data-testid="stSidebar"] * {
    color: #F8FAFC !important;
}

/* Custom Hero Section */
.rm-hero {
    background: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #2563EB 100%);
    padding: 28px 32px;
    border-radius: 20px;
    color: white;
    margin-bottom: 25px;
    box-shadow: 0 10px 25px rgba(37,99,235,0.15);
}

.rm-hero h1 {
    color: #FFFFFF !important;
    font-size: 32px !important;
    font-weight: 800 !important;
    margin-bottom: 4px !important;
}

.rm-hero p {
    color: #93C5FD !important;
    font-size: 15px !important;
    margin: 0 !important;
}

/* Primary Button Styling */
.stButton > button, .stFormSubmitButton > button {
    border-radius: 12px !important;
    border: none !important;
    background: linear-gradient(135deg, #2563EB, #1D4ED8) !important;
    color: white !important;
    font-weight: 600 !important;
    padding: 0.6rem 1.2rem !important;
    transition: all 0.2s ease !important;
}

.stButton > button:hover, .stFormSubmitButton > button:hover {
    background: linear-gradient(135deg, #1D4ED8, #1E40AF) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 14px rgba(37,99,235,0.2) !important;
}

#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header[data-testid="stHeader"] { background: transparent; }
[data-testid="stSidebarNav"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ── AUTHENTICATION SESSION STATE ─────────────────────
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "username" not in st.session_state:
    st.session_state["username"] = "admin"

if "role" not in st.session_state:
    st.session_state["role"] = "Admin"

# ── LOGIN GATEWAY ───────────────────────────────────
if not st.session_state["logged_in"]:
    st.markdown("""
    <div style="text-align: center; margin-top: 25px; margin-bottom: 20px;">
        <div style="font-size: 64px;">🛒</div>
        <h1 style="font-weight: 900; color: #0F172A; margin-bottom: 4px; font-size: 42px;">RetailMind AI</h1>
        <p style="color: #64748B; font-size: 16px; margin-bottom: 10px;">Smart Enterprise Retail & Market Intelligence Portal</p>
        <div style="display: inline-block; background: linear-gradient(135deg, #2563EB, #1D4ED8); color: white; padding: 6px 18px; border-radius: 20px; font-size: 14px; font-weight: 800; box-shadow: 0 4px 12px rgba(37,99,235,0.25);">
            💻 Developed by Suraj V. Shewale
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col_l1, col_l2, col_l3 = st.columns([1, 1.2, 1])
    
    with col_l2:
        st.markdown("### ⚡ Quick Demo Login (One-Click)")
        d_col1, d_col2, d_col3 = st.columns(3)
        with d_col1:
            if st.button("👑 Admin Demo", use_container_width=True, key="demo_admin_btn"):
                st.session_state["logged_in"] = True
                st.session_state["username"] = "admin"
                st.session_state["role"] = "Admin"
                st.toast("Welcome Admin!", icon="👑")
                st.rerun()
        with d_col2:
            if st.button("👔 Manager Demo", use_container_width=True, key="demo_mgr_btn"):
                st.session_state["logged_in"] = True
                st.session_state["username"] = "manager"
                st.session_state["role"] = "Store Manager"
                st.toast("Welcome Manager!", icon="👔")
                st.rerun()
        with d_col3:
            if st.button("🧑‍💼 Staff Demo", use_container_width=True, key="demo_staff_btn"):
                st.session_state["logged_in"] = True
                st.session_state["username"] = "staff"
                st.session_state["role"] = "Staff Account"
                st.toast("Welcome Staff!", icon="🧑‍💼")
                st.rerun()

        st.divider()
        st.info("💡 **Manual Credentials:** Username: `admin` | Password: `admin123`")
        
        with st.form("login_form"):
            st.subheader("🔐 Secure Sign In")
            user_input = st.text_input("Username", placeholder="e.g. admin")
            pass_input = st.text_input("Password", type="password", placeholder="••••••••")
            role_input = st.selectbox("Role", ["Admin", "Store Manager", "Staff Account"])
            
            submit_login = st.form_submit_button("🚀 Sign In to RetailMind AI", use_container_width=True)
            
            if submit_login:
                if user_input.strip() == "admin" and pass_input.strip() == "admin123":
                    st.session_state["logged_in"] = True
                    st.session_state["username"] = user_input
                    st.session_state["role"] = role_input
                    st.success("✅ Login successful!")
                    st.rerun()
                elif user_input.strip() != "" and pass_input.strip() != "":
                    st.session_state["logged_in"] = True
                    st.session_state["username"] = user_input
                    st.session_state["role"] = role_input
                    st.success("✅ Login successful!")
                    st.rerun()
                else:
                    st.error("Please enter valid username and password.")
                    
    st.stop()

# ── ROUTER UTILITY ──────────────────────────────────
def run_page(module_filename):
    filepath = f"page_modules/{module_filename}"
    with open(filepath, "r", encoding="utf-8") as f:
        code = f.read()
    exec(code, globals())

# ── SIDEBAR NAVIGATION ──────────────────────────────
st.sidebar.markdown(f"""
<div style="text-align:center; padding:15px 5px 15px 5px;">
    <div style="font-size:38px;">🛒</div>
    <div style="font-size:20px; font-weight:800; color:#FFFFFF;">RetailMind AI</div>
    <div style="font-size:12px; color:#94A3B8; margin-top:2px;">Smart Retail Intelligence v2.0</div>
    <div style="margin-top:10px; padding:6px 12px; background:rgba(37,99,235,0.2); border-radius:20px; font-size:12px; font-weight:600; color:#93C5FD;">
        👤 {st.session_state['username']} ({st.session_state['role']})
    </div>
</div>
""", unsafe_allow_html=True)

if st.sidebar.button("🚪 Sign Out / Logout", use_container_width=True):
    st.session_state["logged_in"] = False
    st.rerun()

st.sidebar.divider()

menu = st.sidebar.radio(
    "Navigation Menu",
    [
        "🏠 Executive Dashboard",
        "🤖 AI Assistant",
        "📦 Inventory Manager",
        "🌾 Market Rates",
        "🏢 Suppliers Directory",
        "🧾 Billing & POS",
        "👥 Customers & CRM",
        "📈 Business Analytics",
        "⚙️ System Settings",
        "ℹ️ About & Developer"
    ]
)

st.sidebar.divider()
st.sidebar.markdown("""
<div style="padding:12px; background:rgba(255,255,255,0.06); border-radius:14px; font-size:12px; color:#94A3B8; border: 1px solid rgba(255,255,255,0.1);">
    🟢 <b>System Status:</b> Online<br>
    💾 <b>Database:</b> Connected<br>
    🤖 <b>AI Engine:</b> Active
    <hr style="margin:8px 0; border-color:rgba(255,255,255,0.1);">
    <div style="font-weight:700; color:#60A5FA; text-align:center;">💻 Developed by Suraj V. Shewale</div>
</div>
""", unsafe_allow_html=True)

# ── DYNAMIC PAGE ROUTER ─────────────────────────────
if menu == "🏠 Executive Dashboard":
    run_page("dashboard.py")
elif menu == "🤖 AI Assistant":
    run_page("ai_assistant.py")
elif menu == "📦 Inventory Manager":
    run_page("inventory.py")
elif menu == "🌾 Market Rates":
    run_page("market_rates.py")
elif menu == "🏢 Suppliers Directory":
    run_page("suppliers.py")
elif menu == "🧾 Billing & POS":
    run_page("billing.py")
elif menu == "👥 Customers & CRM":
    run_page("customers.py")
elif menu == "📈 Business Analytics":
    run_page("analytics.py")
elif menu == "⚙️ System Settings":
    run_page("settings.py")
elif menu == "ℹ️ About & Developer":
    run_page("about.py")

# ── MASTER FOOTER ───────────────────────────────────
st.write("")
st.markdown("""<div style="margin-top:40px; padding:12px; background:linear-gradient(135deg, #0F172A 0%, #1E293B 100%); border-radius:12px; text-align:center; color:#94A3B8; font-size:12px;">
    🛒 <b>RetailMind AI v2.0</b> &nbsp;|&nbsp; Developed with ❤️ by <b style="color:#60A5FA;">Suraj V. Shewale</b>
</div>""", unsafe_allow_html=True)

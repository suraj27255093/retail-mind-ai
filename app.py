import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import re
import importlib


# =====================================================
# 🎨 RETAILMIND AI — MASTER APP & AUTH SYSTEM
# =====================================================

st.set_page_config(
    page_title="RetailMind AI — Smart Retail System",
    page_icon="🛒",
    layout="wide"
)

# Inject Global Modern CSS Design System
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

/* Sidebar Styling */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%) !important;
    border-right: 1px solid #334155;
}

section[data-testid="stSidebar"] * {
    color: #F8FAFC !important;
}

section[data-testid="stSidebar"] .stRadio label {
    padding: 10px 14px !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
}

/* Login Hero Card */
.login-card {
    background: #FFFFFF;
    padding: 40px;
    border-radius: 24px;
    border: 1px solid #E2E8F0;
    box-shadow: 0 20px 40px rgba(15,23,42,0.08);
    max-width: 480px;
    margin: 40px auto;
    text-align: center;
}

.login-card h2 {
    font-weight: 800;
    color: #0F172A;
    margin-bottom: 8px;
}

/* Custom Hero Cards */
.rm-hero {
    background: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #2563EB 100%);
    padding: 30px 35px;
    border-radius: 22px;
    color: white;
    margin-bottom: 25px;
    box-shadow: 0 12px 30px rgba(37,99,235,0.18);
    border: 1px solid rgba(255,255,255,0.12);
}

.rm-hero h1 {
    color: #FFFFFF !important;
    font-size: 34px !important;
    font-weight: 800 !important;
    letter-spacing: -0.5px;
    margin-bottom: 6px !important;
}

.rm-hero p {
    color: #93C5FD !important;
    font-size: 16px !important;
    margin: 0 !important;
}

/* Metric Cards */
[data-testid="stMetric"] {
    background: #FFFFFF !important;
    padding: 20px 22px !important;
    border-radius: 18px !important;
    border: 1px solid #E2E8F0 !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.03) !important;
    transition: all 0.25s ease-in-out !important;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 10px 25px rgba(37,99,235,0.10) !important;
    border-color: #BFDBFE !important;
}

[data-testid="stMetricValue"] {
    font-weight: 800 !important;
    font-size: 28px !important;
    color: #0F172A !important;
}

[data-testid="stMetricLabel"] {
    font-weight: 600 !important;
    font-size: 13px !important;
    color: #64748B !important;
}

/* Buttons */
.stButton > button, .stFormSubmitButton > button {
    border-radius: 12px !important;
    border: none !important;
    background: linear-gradient(135deg, #2563EB, #1D4ED8) !important;
    color: white !important;
    font-weight: 600 !important;
    padding: 0.65rem 1.3rem !important;
    transition: all 0.2s ease !important;
}

.stButton > button:hover, .stFormSubmitButton > button:hover {
    background: linear-gradient(135deg, #1D4ED8, #1E40AF) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 18px rgba(37,99,235,0.25) !important;
}

/* Dataframe & Tables */
[data-testid="stDataFrame"] {
    border-radius: 16px !important;
    overflow: hidden !important;
    border: 1px solid #E2E8F0 !important;
}

#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header[data-testid="stHeader"] { background: transparent; }
[data-testid="stSidebarNav"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# Initialize Session Auth
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "username" not in st.session_state:
    st.session_state["username"] = "admin"

if "role" not in st.session_state:
    st.session_state["role"] = "Admin"

# =====================================================
# 🔐 AUTHENTICATION MANDATORY LOGIN GATEWAY
# =====================================================

if not st.session_state["logged_in"]:
    st.markdown("""
    <div style="text-align: center; margin-top: 30px;">
        <div style="font-size: 64px;">🛒</div>
        <h1 style="font-weight: 800; color: #0F172A; margin-bottom: 5px;">RetailMind AI</h1>
        <p style="color: #64748B; font-size: 16px;">Smart Enterprise Retail & Market Intelligence Portal</p>
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
            user_input = st.text_input("Username", value="admin")
            pass_input = st.text_input("Password", type="password", value="admin123")
            role_input = st.selectbox("Role", ["Admin", "Store Manager", "Staff Account"])
            
            remember_me = st.checkbox("Remember session", value=True)
            submit_login = st.form_submit_button("🚀 Sign In to RetailMind AI", use_container_width=True)
            
            if submit_login:
                if user_input.strip() == "admin" and pass_input.strip() == "admin123":
                    st.session_state["logged_in"] = True
                    st.session_state["username"] = user_input
                    st.session_state["role"] = role_input
                    st.success("✅ Login successful! Loading dashboard...")
                    st.rerun()
                elif user_input.strip() != "" and pass_input.strip() != "":
                    st.session_state["logged_in"] = True
                    st.session_state["username"] = user_input
                    st.session_state["role"] = role_input
                    st.success("✅ Login successful!")
                    st.rerun()
                else:
                    st.error("Please enter valid username and password.")
                    
    st.stop() # Stop execution here so no app page is shown until logged in!

# =====================================================
# DATABASE UTILITIES
# =====================================================

@st.cache_data(ttl=30)
def load_db_data():
    conn = sqlite3.connect("retailmind.db")
    products_df = pd.read_sql_query("SELECT * FROM products", conn)
    
    if 'selling_price' not in products_df.columns and 'price' in products_df.columns:
        products_df['selling_price'] = products_df['price']
    elif 'selling_price' in products_df.columns and 'price' not in products_df.columns:
        products_df['price'] = products_df['selling_price']
        
    if 'purchase_price' not in products_df.columns:
        products_df['purchase_price'] = products_df['selling_price'] * 0.85
        
    if 'stock' not in products_df.columns:
        products_df['stock'] = 50
        
    if 'min_stock' not in products_df.columns:
        products_df['min_stock'] = 10

    products_df['profit_margin'] = products_df['selling_price'] - products_df['purchase_price']
    products_df['margin_pct'] = (products_df['profit_margin'] / products_df['selling_price'].replace(0,1)) * 100

    conn.close()
    return products_df

df = load_db_data()

# =====================================================
# SIDEBAR NAVIGATION & LOGOUT
# =====================================================

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
        "⚙️ System Settings"
    ]
)

st.sidebar.divider()
st.sidebar.markdown("""
<div style="padding:10px; background:rgba(255,255,255,0.05); border-radius:12px; font-size:12px; color:#94A3B8;">
    🟢 <b>System Status:</b> Online<br>
    💾 <b>Database:</b> Connected<br>
    🤖 <b>AI Engine:</b> Active
</div>
""", unsafe_allow_html=True)

# =====================================================
# 1. 🏠 EXECUTIVE DASHBOARD
# =====================================================
if menu == "🏠 Executive Dashboard":
    st.markdown("""
    <div class="rm-hero">
        <h1>🛒 RetailMind AI — Executive Dashboard</h1>
        <p>Real-Time Overview of Grocery Business, Inventory Health, & Market Intelligence</p>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3, c4, c5 = st.columns(5)
    total_products = len(df)
    total_categories = df["category"].nunique()
    total_markets = df["market"].nunique()
    avg_price = df["selling_price"].mean()
    low_stock_count = len(df[df['stock'] <= df['min_stock']])
    
    with c1:
        st.metric("📦 Total Products", f"{total_products:,}")
    with c2:
        st.metric("📂 Categories", total_categories)
    with c3:
        st.metric("🏪 Markets", total_markets)
    with c4:
        st.metric("💰 Avg Selling Price", f"₹{avg_price:.2f}")
    with c5:
        st.metric("⚠️ Low Stock Items", low_stock_count, delta=f"{low_stock_count} Need Reorder" if low_stock_count>0 else "Healthy Stock", delta_color="inverse")
        
    st.write("")
    
    # Action Buttons Row
    st.markdown("**⚡ Quick Actions:**")
    ac1, ac2, ac3, ac4 = st.columns(4)
    with ac1:
        if st.button("📊 Refresh Catalog Stats", use_container_width=True):
            st.cache_data.clear()
            st.success("Refreshed!")
            st.rerun()
    with ac2:
        if st.button("🚨 View Low Stock Items", use_container_width=True):
            st.info(f"{low_stock_count} items need replenishment.")
    with ac3:
        if st.button("📥 Download Catalog CSV", use_container_width=True):
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("Download CSV", csv, "Catalog_Export.csv", "text/csv")
    with ac4:
        if st.button("🤖 Launch AI Assistant", use_container_width=True):
            st.info("Switching to AI Assistant...")
            
    st.write("")
    left_col, right_col = st.columns([1.5, 1])
    
    with left_col:
        st.subheader("📊 Category Stock & Price Distribution")
        cat_fig = px.bar(
            df.groupby("category").agg(AvgPrice=("selling_price","mean"), Count=("id","count")).reset_index(),
            x="category",
            y="AvgPrice",
            color="Count",
            labels={"AvgPrice": "Average Price (₹)", "Count": "Items Count"},
            title="Category Average Selling Price (₹) & Product Count",
            color_continuous_scale="Blues"
        )
        st.plotly_chart(cat_fig, use_container_width=True)
        
    with right_col:
        st.subheader("🏪 Market Sourcing Share")
        mkt_fig = px.pie(
            df,
            names="market",
            title="Products Sourced per Market Location",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        st.plotly_chart(mkt_fig, use_container_width=True)

    st.divider()
    st.subheader("📋 Top Catalog Highlights")
    st.dataframe(
        df[['id', 'product_name', 'brand', 'category', 'unit', 'purchase_price', 'selling_price', 'stock', 'market', 'supplier']].head(12),
        use_container_width=True,
        hide_index=True
    )

# =====================================================
# 2. 🤖 AI ASSISTANT
# =====================================================
elif menu == "🤖 AI Assistant":
    import page_modules.ai_assistant as ai_module
    importlib.reload(ai_module)

# =====================================================
# 3. 📦 INVENTORY MANAGER
# =====================================================
elif menu == "📦 Inventory Manager":
    import page_modules.inventory as inventory_module
    importlib.reload(inventory_module)

# =====================================================
# 4. 🌾 MARKET RATES
# =====================================================
elif menu == "🌾 Market Rates":
    import page_modules.market_rates as market_module
    importlib.reload(market_module)

# =====================================================
# 5. 🏢 SUPPLIERS DIRECTORY
# =====================================================
elif menu == "🏢 Suppliers Directory":
    import page_modules.suppliers as supplier_module
    importlib.reload(supplier_module)

# =====================================================
# 6. 🧾 BILLING & POS
# =====================================================
elif menu == "🧾 Billing & POS":
    import page_modules.billing as billing_module
    importlib.reload(billing_module)

# =====================================================
# 7. 👥 CUSTOMERS & CRM
# =====================================================
elif menu == "👥 Customers & CRM":
    import page_modules.customers as customer_module
    importlib.reload(customer_module)

# =====================================================
# 8. 📈 BUSINESS ANALYTICS
# =====================================================
elif menu == "📈 Business Analytics":
    import page_modules.analytics as analytics_module
    importlib.reload(analytics_module)

# =====================================================
# 9. 📄 REPORTS & EXPORT
# =====================================================
elif menu == "📄 Reports & Export":
    import page_modules.reports as reports_module
    importlib.reload(reports_module)

# =====================================================
# 10. ⚙️ SYSTEM SETTINGS
# =====================================================
elif menu == "⚙️ System Settings":
    import page_modules.settings as settings_module
    importlib.reload(settings_module)


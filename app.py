import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import re

# Enterprise Architecture & DAL Services
from database.db_manager import DatabaseManager
from services.auth_service import AuthService

# =====================================================
# 🛒 RETAILMIND AI — MASTER ENTERPRISE APP ENGINE
# =====================================================

st.set_page_config(
    page_title="RetailMind AI — Smart Enterprise Retail System",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Database Schema & Data Seeding safely on boot
try:
    DatabaseManager.init_database()
except Exception as e:
    pass

# Initialize Session Authentication & Theme Settings
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "username" not in st.session_state:
    st.session_state["username"] = "admin"

if "role" not in st.session_state:
    st.session_state["role"] = "Admin"

if "dark_mode" not in st.session_state:
    st.session_state["dark_mode"] = False

# ── GLOBAL MASTER CSS DESIGN SYSTEM ────────────────────
if st.session_state.get("dark_mode", False):
    st.markdown("""
    <style>
    .stApp { background-color: #0F172A !important; color: #F8FAFC !important; }
    [data-testid="stMetric"] { background: #1E293B !important; border-color: #334155 !important; }
    [data-testid="stMetricValue"] { color: #F8FAFC !important; }
    [data-testid="stMetricLabel"] { color: #94A3B8 !important; }
    [data-testid="stForm"] { background: #1E293B !important; border-color: #334155 !important; }
    header[data-testid="stHeader"] { background: transparent !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

* {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

.block-container {
    max-width: 1480px;
    padding-top: 1.2rem;
    padding-bottom: 3rem;
}

/* Master Metric Container Styling */
[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-left: 5px solid #2563EB !important;
    border-radius: 16px !important;
    padding: 14px 18px !important;
    box-shadow: 0 4px 14px rgba(15, 23, 42, 0.03) !important;
    transition: all 0.2s ease-in-out !important;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(37, 99, 235, 0.08) !important;
}

[data-testid="stMetricValue"] {
    font-size: clamp(16px, 1.6vw, 24px) !important;
    font-weight: 800 !important;
    white-space: nowrap !important;
    overflow: visible !important;
}

[data-testid="stMetricLabel"] {
    font-size: clamp(11px, 1vw, 13px) !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
}

/* Sidebar Custom Styling */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%) !important;
    border-right: 1px solid #334155 !important;
}

section[data-testid="stSidebar"] * {
    color: #F8FAFC !important;
}

section[data-testid="stSidebar"] .stRadio label {
    padding: 10px 16px !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    transition: all 0.2s ease !important;
}

section[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(255, 255, 255, 0.08) !important;
}

/* Hero Banners */
.rm-hero {
    background: linear-gradient(135deg, #0F172A 0%, #1E293B 45%, #2563EB 100%);
    padding: 32px 38px;
    border-radius: 24px;
    color: white;
    margin-bottom: 28px;
    box-shadow: 0 12px 30px rgba(37, 99, 235, 0.18);
    border: 1px solid rgba(255, 255, 255, 0.12);
}

.rm-hero h1 {
    color: #FFFFFF !important;
    font-size: 34px !important;
    font-weight: 900 !important;
    letter-spacing: -0.5px !important;
    margin-bottom: 6px !important;
}

.rm-hero p {
    color: #93C5FD !important;
    font-size: 16px !important;
    margin: 0 !important;
}

/* Button Design System */
.stButton > button, .stFormSubmitButton > button {
    border-radius: 12px !important;
    border: none !important;
    background: linear-gradient(135deg, #2563EB, #1D4ED8) !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    padding: 0.65rem 1.4rem !important;
    transition: all 0.2s ease-in-out !important;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2) !important;
}

.stButton > button:hover, .stFormSubmitButton > button:hover {
    background: linear-gradient(135deg, #1D4ED8, #1E40AF) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 20px rgba(37, 99, 235, 0.3) !important;
}

/* Dataframe & Tables Styling */
[data-testid="stDataFrame"] {
    border-radius: 18px !important;
    overflow: hidden !important;
    border: 1px solid #E2E8F0 !important;
}

#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header[data-testid="stHeader"] { background: transparent; }
[data-testid="stSidebarNav"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# Initialize Landing Page / Login Toggle State
if "show_login" not in st.session_state:
    st.session_state["show_login"] = False

# ── PUBLIC LANDING PAGE & LOGIN GATEWAY ───────────────
from page_modules.landing import render_public_landing

if not st.session_state["logged_in"]:
    if not st.session_state["show_login"]:
        # Render Pure Commercial Landing Page
        render_public_landing()
        
        # Central Single CTA Button
        c_l1, c_l2, c_l3 = st.columns([1, 1.2, 1])
        with c_l2:
            st.markdown("""
            <div style="text-align: center; margin-top: 10px; margin-bottom: 25px;">
                <p style="font-size: 16px; color: #64748B; font-weight: 600;">Ready to transform your retail business?</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🚀 Sign In / Enter RetailMind Portal", use_container_width=True, key="landing_signin_cta_btn"):
                st.session_state["show_login"] = True
                st.rerun()
        st.stop()
    else:
        # Render Dedicated Login Screen
        b_col1, b_col2 = st.columns([1, 4])
        with b_col1:
            if st.button("⬅️ Back to Home", key="back_to_landing_btn"):
                st.session_state["show_login"] = False
                st.rerun()
                
        st.markdown("""
        <div style="text-align: center; margin-top: 15px; margin-bottom: 20px;">
            <div style="font-size: 54px;">🛒</div>
            <h1 style="font-weight: 900; color: #0F172A; margin-bottom: 4px; font-size: 38px;">RetailMind AI Portal</h1>
            <p style="color: #64748B; font-size: 15px; margin-bottom: 10px;">Smart Enterprise Retail & Market Intelligence System</p>
        </div>
        """, unsafe_allow_html=True)

        col_l1, col_l2, col_l3 = st.columns([1, 1.2, 1])
        
        with col_l2:
            st.markdown("### ⚡ Quick Demo Login (One-Click)")
            d_col1, d_col2, d_col3 = st.columns(3)
            with d_col1:
                if st.button("👑 Admin", use_container_width=True, key="demo_admin_btn"):
                    user_info = AuthService.authenticate_user("admin", "admin123")
                    if user_info:
                        st.session_state["logged_in"] = True
                        st.session_state["username"] = user_info["username"]
                        st.session_state["role"] = user_info["role"]
                        st.toast("Welcome Admin!", icon="👑")
                        st.rerun()
            with d_col2:
                if st.button("👔 Manager", use_container_width=True, key="demo_mgr_btn"):
                    user_info = AuthService.authenticate_user("manager", "admin123")
                    if user_info:
                        st.session_state["logged_in"] = True
                        st.session_state["username"] = user_info["username"]
                        st.session_state["role"] = user_info["role"]
                        st.toast("Welcome Manager!", icon="👔")
                        st.rerun()
            with d_col3:
                if st.button("🧑‍💼 Staff", use_container_width=True, key="demo_staff_btn"):
                    user_info = AuthService.authenticate_user("staff", "admin123")
                    if user_info:
                        st.session_state["logged_in"] = True
                        st.session_state["username"] = user_info["username"]
                        st.session_state["role"] = user_info["role"]
                        st.toast("Welcome Staff!", icon="🧑‍💼")
                        st.rerun()

            st.divider()
            st.info("💡 **Manual Credentials:** Username: `admin` | Password: `admin123`")
            
            with st.form("login_form"):
                st.subheader("🔐 Secure Sign In")
                user_input = st.text_input("Username", placeholder="e.g. admin")
                pass_input = st.text_input("Password", type="password", placeholder="••••••••")
                
                submit_login = st.form_submit_button("🚀 Sign In to RetailMind AI", use_container_width=True)
                
                if submit_login:
                    user_info = AuthService.authenticate_user(user_input, pass_input)
                    if user_info:
                        st.session_state["logged_in"] = True
                        st.session_state["username"] = user_info["username"]
                        st.session_state["role"] = user_info["role"]
                        st.success("✅ Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid username or password. Please try again.")
                        
        st.stop()

# ── ROUTER UTILITY ──────────────────────────────────
def run_page(module_filename: str) -> None:
    filepath = f"page_modules/{module_filename}"
    with open(filepath, "r", encoding="utf-8") as f:
        code = f.read()
    exec_scope = {
        "st": st,
        "sqlite3": sqlite3,
        "pd": pd,
        "px": px,
        "go": go,
        "datetime": datetime,
        "json": json,
        "re": re,
        "DatabaseManager": DatabaseManager,
        "__file__": filepath,
        "__name__": "__main__"
    }
    exec(code, exec_scope)

# ── SIDEBAR NAVIGATION ──────────────────────────────
st.sidebar.markdown(f"""
<div style="text-align:center; padding:15px 5px 15px 5px;">
    <div style="font-size:38px;">🛒</div>
    <div style="font-size:20px; font-weight:800; color:#FFFFFF;">RetailMind AI</div>
    <div style="font-size:12px; color:#94A3B8; margin-top:2px;">Smart Retail Enterprise Platform v3.0</div>
    <div style="margin-top:10px; padding:6px 12px; background:rgba(37,99,235,0.2); border-radius:20px; font-size:12px; font-weight:600; color:#93C5FD;">
        👤 {st.session_state['username']} ({st.session_state['role']})
    </div>
</div>
""", unsafe_allow_html=True)

sb_col1, sb_col2 = st.sidebar.columns(2)
with sb_col1:
    if st.button("🚪 Sign Out", use_container_width=True):
        st.session_state["logged_in"] = False
        st.rerun()
with sb_col2:
    mode_label = "☀️ Light" if st.session_state.get("dark_mode", False) else "🌙 Dark"
    if st.button(mode_label, use_container_width=True, key="sidebar_theme_toggle"):
        st.session_state["dark_mode"] = not st.session_state.get("dark_mode", False)
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
    🟢 <b>System Status:</b> Operational<br>
    💾 <b>Database:</b> DAL Connected<br>
    🤖 <b>AI Engine:</b> NLP & ML Active
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
    🛒 <b>RetailMind AI v3.0 Enterprise Platform</b> &nbsp;|&nbsp; Developed with ❤️ by <b style="color:#60A5FA;">Suraj V. Shewale</b>
</div>""", unsafe_allow_html=True)

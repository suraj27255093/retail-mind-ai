import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import re

# Enterprise Architecture & DAL Services
from database.db_manager import DatabaseManager
from services.auth_service import AuthService

# =====================================================
# 🛒 RETAILMIND AI — MASTER ENTERPRISE APP ENGINE
# =====================================================

st.set_page_config(
    page_title="RetailMind AI | Retail & Mandi Price Intelligence",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Database Schema & Data Seeding safely on boot
try:
    DatabaseManager.init_database()
    from services.mandi_sync_service import MandiSyncEngine
    MandiSyncEngine.auto_sync_mandi_prices()
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
* {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    font-size: 15px;
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
    padding: 16px 20px !important;
    box-shadow: 0 4px 14px rgba(15, 23, 42, 0.03) !important;
    transition: all 0.2s ease-in-out !important;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(37, 99, 235, 0.08) !important;
}

[data-testid="stMetricValue"] {
    font-size: clamp(22px, 2vw, 30px) !important;
    font-weight: 800 !important;
    white-space: nowrap !important;
    overflow: visible !important;
}

[data-testid="stMetricLabel"] {
    font-size: 13px !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.4px !important;
    white-space: normal !important;
    word-break: break-word !important;
    overflow: visible !important;
    text-overflow: clip !important;
    line-height: 1.3 !important;
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
    font-size: 15px !important;
    transition: all 0.2s ease !important;
}

section[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(255, 255, 255, 0.08) !important;
}

/* Hero Banners */
.rm-hero {
    background: linear-gradient(135deg, #0F172A 0%, #1E293B 45%, #2563EB 100%);
    padding: 28px 34px;
    border-radius: 20px;
    color: white;
    margin-bottom: 24px;
    box-shadow: 0 10px 25px rgba(37, 99, 235, 0.15);
    border: 1px solid rgba(255, 255, 255, 0.12);
}

.rm-hero h1 {
    color: #FFFFFF !important;
    font-size: 28px !important;
    font-weight: 900 !important;
    letter-spacing: -0.5px !important;
    margin-bottom: 6px !important;
}
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

# ── SEO METADATA, OPENGRAPH & WCAG ZOOM FIX INJECTION ────
import streamlit.components.v1 as components

components.html("""
<script>
(function() {
    try {
        var doc = window.top.document || window.parent.document || document;
        
        // 1. Preconnect & DNS-Prefetch Resource Hints (Eliminates Render-Blocking Bottlenecks)
        setLink('dns-prefetch', 'https://fonts.googleapis.com');
        setLink('dns-prefetch', 'https://fonts.gstatic.com');
        setLink('preconnect', 'https://fonts.googleapis.com');
        setLink('preconnect', 'https://fonts.gstatic.com');
        
        // 2. Title Tag (52 chars)
        doc.title = "RetailMind AI | Retail & Mandi Price Intelligence";
        
        // 2. Viewport Zoom Fix (WCAG 1.4.4)
        var vp = doc.querySelector('meta[name="viewport"]');
        if (vp) {
            vp.setAttribute('content', 'width=device-width, initial-scale=1.0, user-scalable=yes');
        }
        
        // 3. Helper to set Meta
        function setMeta(name, val, isProp) {
            var attr = isProp ? 'property' : 'name';
            var el = doc.querySelector('meta[' + attr + '="' + name + '"]');
            if (!el) {
                el = doc.createElement('meta');
                el.setAttribute(attr, name);
                doc.head.appendChild(el);
            }
            el.setAttribute('content', val);
        }
        
        // 4. Helper to set Link
        function setLink(rel, href) {
            var el = doc.querySelector('link[rel="' + rel + '"]');
            if (!el) {
                el = doc.createElement('link');
                el.setAttribute('rel', rel);
                doc.head.appendChild(el);
            }
            el.setAttribute('href', href);
        }
        
        // Essential Meta (148 chars - Optimal) & Canonical URL
        setMeta('google-site-verification', 'googlebd6698be2dd95070');
        setMeta('description', 'RetailMind AI helps Indian grocers and supermarkets track APMC mandi prices, forecast inventory stock, and manage instant billing in one platform.');
        setLink('canonical', 'https://retailmind-ai-by-suraj.streamlit.app/');
        
        // OpenGraph Social Share Meta
        setMeta('og:title', 'RetailMind AI | Retail & Mandi Price Intelligence', true);
        setMeta('og:description', 'Track APMC mandi prices, forecast stock, and manage instant retail billing in one platform.', true);
        setMeta('og:url', 'https://retailmind-ai-by-suraj.streamlit.app/', true);
        setMeta('og:type', 'website', true);
        setMeta('og:image', 'https://images.unsplash.com/photo-1578916171728-46686eac8d58?q=80&w=1200&auto=format&fit=crop', true);
        
        // Twitter Card Meta
        setMeta('twitter:card', 'summary_large_image');
        setMeta('twitter:title', 'RetailMind AI | Retail & Mandi Price Intelligence');
        setMeta('twitter:description', 'Track APMC mandi prices, forecast stock, and manage instant retail billing in one platform.');
        setMeta('twitter:image', 'https://images.unsplash.com/photo-1578916171728-46686eac8d58?q=80&w=1200&auto=format&fit=crop');
        
        // JSON-LD Schema Insertion
        var existingJsonLd = doc.querySelector('script[id="jsonld-retailmind"]');
        if (!existingJsonLd) {
            var script = doc.createElement('script');
            script.id = 'jsonld-retailmind';
            script.type = 'application/ld+json';
            script.text = JSON.stringify({
                "@context": "https://schema.org",
                "@type": "SoftwareApplication",
                "name": "RetailMind AI",
                "applicationCategory": "BusinessApplication",
                "operatingSystem": "Web, Cloud, Windows, Android, iOS",
                "offers": {
                    "@type": "Offer",
                    "price": "0.00",
                    "priceCurrency": "INR"
                },
                "description": "RetailMind AI is an AI-powered retail management platform for grocery stores, supermarkets, and distributors featuring live Agmarknet APMC wholesale Mandi intelligence.",
                "author": {
                    "@type": "Person",
                    "name": "Suraj V. Shewale"
                }
            });
            doc.head.appendChild(script);
        }
    } catch(e) {}
})();
</script>
""", height=0, width=0)

# Initialize Landing Page / Login Toggle State
if "show_login" not in st.session_state:
    st.session_state["show_login"] = False

# ── PUBLIC LANDING PAGE & LOGIN GATEWAY ───────────────
from page_modules.landing import render_public_landing

if not st.session_state["logged_in"]:
    if not st.session_state["show_login"]:
        # ── TOP-RIGHT NAVIGATION HEADER BAR (GOOGLE STYLE) ─────
        top_brand, top_actions = st.columns([1.6, 2.8])

        with top_brand:
            st.markdown("""
            <div style="display: flex; align-items: center; gap: 10px; padding: 4px 0; margin-bottom: 12px;">
                <span style="font-size: 30px;">🛒</span>
                <span style="font-weight: 900; font-size: 22px; color: #0F172A; letter-spacing: -0.5px;">RetailMind AI</span>
                <span style="background: rgba(37,99,235,0.12); color: #2563EB; padding: 3px 10px; border-radius: 12px; font-size: 11px; font-weight: 800;">v3.0</span>
            </div>
            """, unsafe_allow_html=True)

        with top_actions:
            h1, h2, h3 = st.columns([1, 1, 1.4])
            with h1:
                if st.button("📩 Contact Us", use_container_width=True, key="top_header_contact_btn"):
                    st.session_state["show_contact_modal"] = not st.session_state.get("show_contact_modal", False)
            with h2:
                if st.button("🔐 Login", use_container_width=True, key="top_header_login_btn"):
                    st.session_state["show_login"] = True
                    st.rerun()
            with h3:
                if st.button("🚀 Enter Portal", use_container_width=True, type="primary", key="top_header_portal_btn"):
                    st.session_state["logged_in"] = True
                    st.session_state["username"] = "admin"
                    st.session_state["role"] = "Admin"
                    st.toast("Welcome to RetailMind AI Portal!", icon="🚀")
                    st.rerun()

        # Contact Us Modal / Drawer
        if st.session_state.get("show_contact_modal", False):
            st.info("💼 **Enterprise Support & Live Demo Onboarding**\n\n💬 **WhatsApp / Call:** +91 8261941723\n\n📧 **Direct Email:** surajshewale2725@gmail.com")

        # Render Commercial Landing Page
        render_public_landing()
        st.write("")
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
            st.markdown("""
            <div style="background: #FFFFFF; padding: 24px; border-radius: 18px; border: 1px solid #E2E8F0; box-shadow: 0 4px 20px rgba(0,0,0,0.05);">
                <h3 style="margin-top: 0; font-size: 18px; color: #0F172A; text-align: center;">⚡ Quick Demo Login</h3>
                <p style="font-size: 12px; color: #64748B; text-align: center; margin-bottom: 14px;">Select a role below for 1-click evaluation & testing</p>
            </div>
            """, unsafe_allow_html=True)
            
            d_col1, d_col2, d_col3 = st.columns(3)
            with d_col1:
                if st.button("👑 Admin (Demo)", use_container_width=True, key="demo_admin_btn"):
                    admin_p = os.environ.get("ADMIN_PASSWORD", "admin123")
                    user_info = AuthService.authenticate_user("admin", admin_p)
                    if user_info:
                        st.session_state["logged_in"] = True
                        st.session_state["username"] = user_info["username"]
                        st.session_state["role"] = user_info["role"]
                        st.toast("Welcome Admin!", icon="👑")
                        st.rerun()
            with d_col2:
                if st.button("👔 Manager (Demo)", use_container_width=True, key="demo_mgr_btn"):
                    admin_p = os.environ.get("ADMIN_PASSWORD", "admin123")
                    user_info = AuthService.authenticate_user("manager", admin_p)
                    if user_info:
                        st.session_state["logged_in"] = True
                        st.session_state["username"] = user_info["username"]
                        st.session_state["role"] = user_info["role"]
                        st.toast("Welcome Manager!", icon="👔")
                        st.rerun()
            with d_col3:
                if st.button("🧑‍💼 Staff (Demo)", use_container_width=True, key="demo_staff_btn"):
                    admin_p = os.environ.get("ADMIN_PASSWORD", "admin123")
                    user_info = AuthService.authenticate_user("staff", admin_p)
                    if user_info:
                        st.session_state["logged_in"] = True
                        st.session_state["username"] = user_info["username"]
                        st.session_state["role"] = user_info["role"]
                        st.toast("Welcome Staff!", icon="🧑‍💼")
                        st.rerun()

            st.divider()
            
            with st.form("login_form"):
                st.subheader("🔐 Store Owner Sign In")
                user_input = st.text_input("Username / Shop ID", placeholder="e.g. admin or your username")
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

def run_page(module_filename: str) -> None:
    filepath = f"page_modules/{module_filename}"
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            code = f.read()
        exec_scope = {
            "st": st,
            "sqlite3": sqlite3,
            "pd": pd,
            "px": px,
            "go": go,
            "datetime": datetime,
            "timedelta": timedelta,
            "json": json,
            "re": re,
            "DatabaseManager": DatabaseManager,
            "__file__": filepath,
            "__name__": "__main__"
        }
        exec(code, exec_scope)
    except Exception as err:
        # Internal logging for developer investigation
        import logging
        logging.error(f"Error executing module '{module_filename}': {err}", exc_info=True)
        st.error("⚠️ Something went wrong while loading this page. Please try again.")

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

nav_options = [
    "🏠 Dashboard",
    "📦 Products & Inventory",
    "📊 Market Rates",
    "🛒 Sales / POS Billing",
    "👥 Customers",
    "🚚 Suppliers",
    "📈 Analytics",
    "📄 Reports",
    "🤖 AI Assistant",
    "⚙️ Settings",
    "ℹ️ About Developer"
]

if "nav_menu" not in st.session_state:
    st.session_state["nav_menu"] = "🏠 Dashboard"

if "redirect_page" in st.session_state and st.session_state["redirect_page"]:
    target = st.session_state.pop("redirect_page")
    if target in nav_options:
        st.session_state["nav_menu"] = target

menu = st.sidebar.radio(
    "Navigation Menu",
    nav_options,
    key="nav_menu"
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
if menu == "🏠 Dashboard":
    run_page("dashboard.py")
elif menu == "📦 Products & Inventory":
    run_page("inventory.py")
elif menu == "📊 Market Rates":
    run_page("market_rates.py")
elif menu == "🛒 Sales / POS Billing":
    run_page("billing.py")
elif menu == "👥 Customers":
    run_page("customers.py")
elif menu == "🚚 Suppliers":
    run_page("suppliers.py")
elif menu == "📈 Analytics":
    run_page("analytics.py")
elif menu == "📄 Reports":
    run_page("reports.py")
elif menu == "🤖 AI Assistant":
    run_page("ai_assistant.py")
elif menu == "⚙️ Settings":
    run_page("settings.py")
elif menu == "ℹ️ About Developer":
    run_page("about.py")

# ── MASTER FOOTER ───────────────────────────────────
st.write("")
st.markdown("""<div style="margin-top:40px; padding:12px; background:linear-gradient(135deg, #0F172A 0%, #1E293B 100%); border-radius:12px; text-align:center; color:#94A3B8; font-size:12px;">
    🛒 <b>RetailMind AI v3.0 Enterprise Platform</b> &nbsp;|&nbsp; Developed with ❤️ by <b style="color:#60A5FA;">Suraj V. Shewale</b>
</div>""", unsafe_allow_html=True)

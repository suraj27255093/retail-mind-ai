import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# =========================================================
# 🏠 EXECUTIVE DASHBOARD — ENTERPRISE SAAS CONTROL CENTER
# =========================================================

@st.cache_data(ttl=15)
def load_products():
    conn = sqlite3.connect("retailmind.db")
    df = pd.read_sql_query("SELECT * FROM products", conn)
    conn.close()

    if "selling_price" in df.columns and ("price" not in df.columns or df["price"].isnull().all()):
        df["price"] = df["selling_price"]
    elif "price" in df.columns and ("selling_price" not in df.columns or df["selling_price"].isnull().all()):
        df["selling_price"] = df["price"]

    df["price"] = pd.to_numeric(df["price"], errors="coerce").fillna(0)
    df["selling_price"] = pd.to_numeric(df["selling_price"], errors="coerce").fillna(0)
    df["purchase_price"] = pd.to_numeric(df.get("purchase_price", df["selling_price"] * 0.85), errors="coerce").fillna(0)
    df["stock"] = pd.to_numeric(df.get("stock", 50), errors="coerce").fillna(50)
    df["stock_value"] = df["selling_price"] * df["stock"]
    df["cost_valuation"] = df["purchase_price"] * df["stock"]
    df["profit_margin"] = df["selling_price"] - df["purchase_price"]
    df["margin_pct"] = (df["profit_margin"] / df["selling_price"].replace(0, 1)) * 100
    return df

df = load_products()

if df.empty:
    st.warning("⚠️ No products found in database.")
    st.stop()

# ── 1. ULTRA-SLEEK HERO BANNER ───────────
st.markdown("""
<div style="background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 50%, #2563EB 100%); padding: 28px 32px; border-radius: 24px; color: white; margin-bottom: 24px; box-shadow: 0 15px 35px -10px rgba(37,99,235,0.22); border: 1px solid rgba(255,255,255,0.15);">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px;">
        <div>
            <h1 style="font-size: 28px; font-weight: 900; letter-spacing: -0.5px; margin: 0 0 6px 0; color: #FFFFFF;">
                🛒 RetailMind AI — Store & Mandi Manager
            </h1>
            <p style="font-size: 14.5px; color: #CBD5E1; margin: 0; font-weight: 500;">
                Live Mandi Rates • 10-Second POS Billing • Inventory Alerts & Profit Optimizer
            </p>
        </div>
        <div style="display: flex; gap: 8px; flex-wrap: wrap;">
            <span style="background: rgba(16,185,129,0.2); border: 1px solid #10B981; padding: 5px 14px; border-radius: 20px; font-size: 12px; font-weight: 700; color: #6EE7B7;">
                🟢 4 Govt Portals Live
            </span>
            <span style="background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); padding: 5px 14px; border-radius: 20px; font-size: 12px; font-weight: 700; color: #F1F5F9;">
                🤖 AI Active
            </span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── 2. EXECUTIVE KPI CARDS ─────────────────────────────
total_products = len(df)
total_categories = df["category"].nunique()
total_markets = df["market"].nunique()
total_cost_val = df["cost_valuation"].sum()
total_retail_val = df["stock_value"].sum()
total_profit_pool = df["profit_margin"].sum()
avg_margin_pct = df["margin_pct"].mean()
low_stock_count = len(df[df["stock"] < 15])

kc1, kc2, kc3, kc4 = st.columns(4)

with kc1:
    st.metric(
        label="📦 Total Items",
        value=f"{total_products:,} SKUs",
        delta=f"{total_categories} Categories"
    )

with kc2:
    st.metric(
        label="💰 Stock Cost Value",
        value=f"₹{total_cost_val:,.0f}",
        delta=f"MRP: ₹{total_retail_val:,.0f}"
    )

with kc3:
    st.metric(
        label="🔥 Total Profit Pool",
        value=f"₹{total_profit_pool:,.0f}",
        delta=f"Avg {avg_margin_pct:.1f}% Margin"
    )

with kc4:
    st.metric(
        label="🌾 Mandi Source Hubs",
        value=f"{total_markets} APMC Hubs",
        delta="Priority 1 Govt Data"
    )

st.write("")

# ── 3. PROJECT CORE FEATURE MODULE CARDS (HAMARE PROJECT KE MAIN OPTIONS) ──────────
st.markdown("<div style='font-size: 20px; font-weight: 900; color: #0F172A; margin-top: 10px; margin-bottom: 16px;'>🌟 RetailMind AI — Core Feature Options (प्रोजेक्ट के मुख्य ऑप्शंस)</div>", unsafe_allow_html=True)

fc_col1, fc_col2, fc_col3 = st.columns(3)

with fc_col1:
    st.markdown("""
    <div style="background: #FFFFFF; border: 1px solid #E2E8F0; padding: 22px; border-radius: 20px; margin-bottom: 20px; border-top: 5px solid #2563EB; box-shadow: 0 8px 20px rgba(15,23,42,0.04);">
        <div style="font-size: 32px; margin-bottom: 8px;">🌾</div>
        <div style="font-weight: 900; font-size: 18px; color: #0F172A; margin-bottom: 6px;">1. APMC Mandi Wholesale Rates</div>
        <div style="font-size: 13.5px; color: #64748B; line-height: 1.5; margin-bottom: 14px;">Live wholesale purchase rates for Sugar, Rice, Atta, Oil from official Govt portals (fcainfoweb, msamb, enam).</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🌾 Open Mandi Rates", use_container_width=True, key="card_btn_mandi"):
        st.session_state["redirect_page"] = "🌾 Market Rates"
        st.rerun()

    st.write("")
    st.markdown("""
    <div style="background: #FFFFFF; border: 1px solid #E2E8F0; padding: 22px; border-radius: 20px; margin-bottom: 20px; border-top: 5px solid #8B5CF6; box-shadow: 0 8px 20px rgba(15,23,42,0.04);">
        <div style="font-size: 32px; margin-bottom: 8px;">🤖</div>
        <div style="font-weight: 900; font-size: 18px; color: #0F172A; margin-bottom: 6px;">2. Hinglish AI Query Assistant</div>
        <div style="font-size: 13.5px; color: #64748B; line-height: 1.5; margin-bottom: 14px;">Ask any retail query like <i>"Sugar rate Malegaon mein"</i> or <i>"Rice stock status"</i> for instant AI insights.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🤖 Open AI Assistant", use_container_width=True, key="card_btn_ai"):
        st.session_state["redirect_page"] = "🤖 AI Assistant"
        st.rerun()

with fc_col2:
    st.markdown("""
    <div style="background: #FFFFFF; border: 1px solid #E2E8F0; padding: 22px; border-radius: 20px; margin-bottom: 20px; border-top: 5px solid #10B981; box-shadow: 0 8px 20px rgba(15,23,42,0.04);">
        <div style="font-size: 32px; margin-bottom: 8px;">🧾</div>
        <div style="font-weight: 900; font-size: 18px; color: #0F172A; margin-bottom: 6px;">3. Ultra-Fast POS Billing</div>
        <div style="font-size: 13.5px; color: #64748B; line-height: 1.5; margin-bottom: 14px;">10-Second barcode billing, fast quantity preset buttons, GST auto-calc, and 1-click WhatsApp customer receipts.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🧾 Open POS Billing", use_container_width=True, key="card_btn_pos"):
        st.session_state["redirect_page"] = "🧾 Billing & POS"
        st.rerun()

    st.write("")
    st.markdown("""
    <div style="background: #FFFFFF; border: 1px solid #E2E8F0; padding: 22px; border-radius: 20px; margin-bottom: 20px; border-top: 5px solid #F59E0B; box-shadow: 0 8px 20px rgba(15,23,42,0.04);">
        <div style="font-size: 32px; margin-bottom: 8px;">📦</div>
        <div style="font-weight: 900; font-size: 18px; color: #0F172A; margin-bottom: 6px;">4. Inventory & Stock Radar</div>
        <div style="font-size: 13.5px; color: #64748B; line-height: 1.5; margin-bottom: 14px;">Track active SKU catalog, automatic low stock reorder alerts, stockout risk radar, and 1-click stock refills.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("📦 Open Inventory", use_container_width=True, key="card_btn_stock"):
        st.session_state["redirect_page"] = "📦 Inventory Manager"
        st.rerun()

with fc_col3:
    st.markdown("""
    <div style="background: #FFFFFF; border: 1px solid #E2E8F0; padding: 22px; border-radius: 20px; margin-bottom: 20px; border-top: 5px solid #EC4899; box-shadow: 0 8px 20px rgba(15,23,42,0.04);">
        <div style="font-size: 32px; margin-bottom: 8px;">👥</div>
        <div style="font-weight: 900; font-size: 18px; color: #0F172A; margin-bottom: 6px;">5. Customer CRM & Khata Ledger</div>
        <div style="font-size: 13.5px; color: #64748B; line-height: 1.5; margin-bottom: 14px;">Track customer purchase history, manage credit khata accounts, and auto-reward customer loyalty points.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("👥 Open Customer CRM", use_container_width=True, key="card_btn_crm"):
        st.session_state["redirect_page"] = "👥 Customers & CRM"
        st.rerun()

    st.write("")
    st.markdown("""
    <div style="background: #FFFFFF; border: 1px solid #E2E8F0; padding: 22px; border-radius: 20px; margin-bottom: 20px; border-top: 5px solid #0284C7; box-shadow: 0 8px 20px rgba(15,23,42,0.04);">
        <div style="font-size: 32px; margin-bottom: 8px;">🚚</div>
        <div style="font-weight: 900; font-size: 18px; color: #0F172A; margin-bottom: 6px;">6. Mandi Supplier Directory</div>
        <div style="font-size: 13.5px; color: #64748B; line-height: 1.5; margin-bottom: 14px;">Wholesale mandi supplier directory across Nashik, Pune, Malegaon & Mumbai Vashi APMC markets.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🚚 Open Suppliers", use_container_width=True, key="card_btn_supplier"):
        st.session_state["redirect_page"] = "🏢 Suppliers Directory"
        st.rerun()
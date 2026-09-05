import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# =========================================================
# 🏠 ULTRA-SIMPLE KIRANA SHOPKEEPER DASHBOARD
# =========================================================

@st.cache_data(ttl=15)
def load_dashboard_data():
    conn = sqlite3.connect("retailmind.db")
    df = pd.read_sql_query("SELECT * FROM products", conn)
    try:
        bills_df = pd.read_sql_query("SELECT * FROM bills", conn)
    except Exception:
        bills_df = pd.DataFrame()
    conn.close()

    if "selling_price" in df.columns and ("price" not in df.columns or df["price"].isnull().all()):
        df["price"] = df["selling_price"]
    elif "price" in df.columns and ("selling_price" not in df.columns or df["selling_price"].isnull().all()):
        df["selling_price"] = df["price"]

    df["selling_price"] = pd.to_numeric(df["selling_price"], errors="coerce").fillna(0)
    df["purchase_price"] = pd.to_numeric(df.get("purchase_price", df["selling_price"] * 0.85), errors="coerce").fillna(0)
    df["stock"] = pd.to_numeric(df.get("stock", 50), errors="coerce").fillna(50)
    df["min_stock"] = pd.to_numeric(df.get("min_stock", 10), errors="coerce").fillna(10)
    return df, bills_df

df, bills_df = load_dashboard_data()

# ── 1. GREETING BANNER ──────────────────────────────────
user_disp = st.session_state.get("username", "Store Owner").capitalize()
st.markdown(f"""
<div style="background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 50%, #2563EB 100%); padding: 22px 28px; border-radius: 18px; color: white; margin-bottom: 20px;">
    <h1 style="font-size: 26px; font-weight: 900; margin: 0 0 4px 0; color: #FFFFFF;">
        Namaste, {user_disp} 👋 (नमस्ते)
    </h1>
    <p style="font-size: 15px; color: #CBD5E1; margin: 0;">
        Welcome to your Kirana Store Control Panel
    </p>
</div>
""", unsafe_allow_html=True)

# ── 2. LARGE ACTION BUTTONS (WHAT TO DO) ─────────────────
st.subheader("⚡ What would you like to do?")

qa1, qa2, qa3, qa4 = st.columns(4)

with qa1:
    if st.button("🛒 New Bill\n(नया बिल बनाएं)", use_container_width=True, type="primary", key="qa_new_bill"):
        st.session_state["redirect_page"] = "🛒 Billing"
        st.rerun()

with qa2:
    if st.button("📦 Products\n(सामान लिस्ट)", use_container_width=True, key="qa_add_prod"):
        st.session_state["redirect_page"] = "📦 Products"
        st.rerun()

with qa3:
    if st.button("📊 Market Rates\n(मंडी भाव)", use_container_width=True, key="qa_mkt_rates"):
        st.session_state["redirect_page"] = "📊 Market Rates"
        st.rerun()

with qa4:
    if st.button("📋 Stock\n(स्टॉक चेक)", use_container_width=True, key="qa_stock"):
        st.session_state["redirect_page"] = "📋 Stock"
        st.rerun()

st.write("")
st.divider()

# ── 3. TODAY'S STORE SUMMARY (COMPACT & SIMPLE) ───────────
today_str = datetime.now().strftime("%Y-%m-%d")
if not bills_df.empty and "created_at" in bills_df.columns:
    today_bills = bills_df[bills_df["created_at"].str.startswith(today_str, na=False)]
    todays_sales = today_bills["grand_total"].sum() if "grand_total" in today_bills.columns else 0.0
    todays_orders = len(today_bills)
else:
    saved_b = st.session_state.get("saved_bills", [])
    todays_sales = sum(b.get("grand_total", 0) for b in saved_b)
    todays_orders = len(saved_b)

low_stock_count = len(df[df["stock"] <= df["min_stock"]]) if not df.empty else 0

st.subheader("📊 Today's Store Summary")

s1, s2, s3 = st.columns(3)
with s1:
    st.metric("💵 Today's Sales (आज की बिक्री)", f"₹{todays_sales:,.2f}")
with s2:
    st.metric("🧾 Today's Bills (आज के बिल)", f"{todays_orders} Bills")
with s3:
    st.metric("⚠️ Low Stock Alert (कम स्टॉक)", f"{low_stock_count} Products", delta=f"{low_stock_count} Need Refill" if low_stock_count > 0 else "All Healthy", delta_color="inverse")

st.write("")
st.divider()

# ── 4. LOW STOCK & MARKET RATES (CLEAN 2-COLUMN VIEW) ─────
col_low, col_rates = st.columns(2)

with col_low:
    st.subheader("⚠️ Low Stock Alert (कम स्टॉक वाले सामान)")
    if not df.empty:
        low_df = df[df["stock"] <= df["min_stock"]].sort_values("stock")
        if low_df.empty:
            st.success("✅ All products have sufficient stock!")
        else:
            disp_low = low_df[["product_name", "stock", "min_stock"]].copy()
            disp_low.columns = ["Product", "Current Stock", "Min Stock"]
            st.dataframe(disp_low, use_container_width=True, hide_index=True, height=200)

with col_rates:
    st.subheader("🌾 Latest Market Rates (आज के मंडी भाव)")
    if not df.empty:
        mkt_summary = df[["product_name", "market", "purchase_price"]].head(5).copy()
        mkt_summary.columns = ["Product", "Mandi Market", "Wholesale Rate"]
        mkt_summary["Wholesale Rate"] = mkt_summary["Wholesale Rate"].map("₹{:.2f}".format)
        st.dataframe(mkt_summary, use_container_width=True, hide_index=True, height=200)
        if st.button("📊 View All Market Rates", key="dash_view_rates", use_container_width=True):
            st.session_state["redirect_page"] = "📊 Market Rates"
            st.rerun()

import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# =========================================================
# 🏠 KIRANA DASHBOARD — EASY STORE CONTROL CENTER
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

# ── 1. CLEAN HERO BANNER ─────────────────────────────────
user_disp = st.session_state.get("username", "Store Owner").capitalize()
st.markdown(f"""
<div style="background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 50%, #2563EB 100%); padding: 24px 28px; border-radius: 20px; color: white; margin-bottom: 22px; box-shadow: 0 10px 25px -5px rgba(37,99,235,0.18);">
    <h1 style="font-size: 26px; font-weight: 900; margin: 0 0 6px 0; color: #FFFFFF;">
        Welcome, {user_disp} 👋
    </h1>
    <p style="font-size: 14.5px; color: #CBD5E1; margin: 0; font-weight: 500;">
        Here's what's happening in your store today.
    </p>
</div>
""", unsafe_allow_html=True)

# ── 2. TOP 4 KEY METRICS ─────────────────────────────────
today_str = datetime.now().strftime("%Y-%m-%d")
if not bills_df.empty and "created_at" in bills_df.columns:
    today_bills = bills_df[bills_df["created_at"].str.startswith(today_str, na=False)]
    todays_sales = today_bills["grand_total"].sum() if "grand_total" in today_bills.columns else 0.0
    todays_orders = len(today_bills)
else:
    # Use saved bills in session state if DB table empty
    saved_b = st.session_state.get("saved_bills", [])
    todays_sales = sum(b.get("grand_total", 0) for b in saved_b)
    todays_orders = len(saved_b)

total_products = len(df) if not df.empty else 0
low_stock_count = len(df[df["stock"] <= df["min_stock"]]) if not df.empty else 0

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("💵 Today's Sales", f"₹{todays_sales:,.2f}")
with m2:
    st.metric("📦 Total Products", f"{total_products:,} SKUs")
with m3:
    st.metric("⚠️ Low Stock", f"{low_stock_count} Items", delta=f"{low_stock_count} Need Reorder" if low_stock_count > 0 else "All Healthy", delta_color="inverse")
with m4:
    st.metric("🧾 Today's Orders", f"{todays_orders} Bills")

st.write("")

# ── 3. QUICK ACTIONS ─────────────────────────────────────
st.subheader("⚡ Quick Actions (त्वरित कार्य)")
qa1, qa2, qa3, qa4 = st.columns(4)

with qa1:
    if st.button("🛒 New Bill", use_container_width=True, type="primary", key="qa_new_bill"):
        st.session_state["redirect_page"] = "🛒 Sales / POS Billing"
        st.rerun()
with qa2:
    if st.button("➕ Add Product", use_container_width=True, key="qa_add_prod"):
        st.session_state["redirect_page"] = "📦 Products & Inventory"
        st.rerun()
with qa3:
    if st.button("📊 Market Rates", use_container_width=True, key="qa_mkt_rates"):
        st.session_state["redirect_page"] = "📊 Market Rates"
        st.rerun()
with qa4:
    if st.button("🤖 Ask AI", use_container_width=True, key="qa_ask_ai"):
        st.session_state["redirect_page"] = "🤖 AI Assistant"
        st.rerun()

st.write("")
st.divider()

# ── 4. LOW STOCK ALERTS & TODAY'S MARKET RATES ────────────
c_left, c_right = st.columns([1.2, 1])

with c_left:
    st.subheader("⚠️ Low Stock Alerts (कम स्टॉक की जानकारी)")
    if not df.empty:
        low_df = df[df["stock"] <= df["min_stock"]].sort_values("stock")
        if low_df.empty:
            st.success("🎉 All product stock levels are healthy! No items need immediate reordering.")
        else:
            disp_low = low_df[["product_name", "category", "stock", "min_stock", "market"]].copy()
            disp_low.columns = ["Product Name", "Category", "Current Stock", "Min Limit", "Mandi Market"]
            st.dataframe(disp_low, use_container_width=True, hide_index=True)
            if st.button("⚡ Refill Low Stock (+10 units)", key="dash_quick_refill"):
                conn = sqlite3.connect("retailmind.db")
                conn.execute("UPDATE products SET stock = stock + 10 WHERE stock <= min_stock")
                conn.commit()
                conn.close()
                st.cache_data.clear()
                st.success("✅ Stock refilled successfully!")
                st.rerun()

with c_right:
    st.subheader("🌾 Today's Mandi Market Rates")
    if not df.empty:
        mkt_summary = df.groupby(["category", "market"])["purchase_price"].mean().reset_index().head(8)
        mkt_summary.columns = ["Commodity", "Market Yard", "Wholesale Rate (₹)"]
        mkt_summary["Wholesale Rate (₹)"] = mkt_summary["Wholesale Rate (₹)"].map("₹{:.2f}".format)
        st.dataframe(mkt_summary, use_container_width=True, hide_index=True)
        if st.button("📊 View All Market Rates", key="dash_view_rates"):
            st.session_state["redirect_page"] = "📊 Market Rates"
            st.rerun()

st.write("")
st.divider()

# ── 5. RECENT SALES ACTIVITY ──────────────────────────────
st.subheader("🧾 Recent Sales Transactions")
saved_bills = st.session_state.get("saved_bills", [])
if saved_bills:
    recent_df = pd.DataFrame(saved_bills).tail(5)[["bill_no", "customer_name", "items_count", "grand_total", "payment_method"]]
    recent_df.columns = ["Bill No", "Customer", "Items", "Total Amount (₹)", "Payment Mode"]
    recent_df["Total Amount (₹)"] = recent_df["Total Amount (₹)"].map("₹{:.2f}".format)
    st.dataframe(recent_df, use_container_width=True, hide_index=True)
else:
    st.info("No bills generated in this session yet. Click '🛒 New Bill' above to create your first sale bill!")
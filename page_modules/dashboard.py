import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# =========================================================
# 🏠 KIRANA DASHBOARD — MASTER STORE CONTROL CENTER
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
    df["stock_value"] = df["selling_price"] * df["stock"]
    return df, bills_df

df, bills_df = load_dashboard_data()

# ── 1. PAGE HEADER / WELCOME BANNER ─────────────────────
user_disp = st.session_state.get("username", "Store Owner").capitalize()
st.markdown(f"""
<div style="background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 50%, #2563EB 100%); padding: 18px 24px; border-radius: 16px; color: white; margin-bottom: 16px; box-shadow: 0 6px 18px -4px rgba(37,99,235,0.18);">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
        <div>
            <h1 style="font-size: 24px; font-weight: 900; margin: 0 0 4px 0; color: #FFFFFF;">
                Good Morning, {user_disp} 👋
            </h1>
            <p style="font-size: 13.5px; color: #CBD5E1; margin: 0; font-weight: 500;">
                Here's what's happening in your store today.
            </p>
        </div>
        <div style="font-size: 12px; background: rgba(255,255,255,0.12); padding: 5px 14px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.2);">
            📅 {datetime.now().strftime("%A, %d %B %Y")}
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── 2. TOP KPI CARDS ─────────────────────────────────────
today_str = datetime.now().strftime("%Y-%m-%d")
if not bills_df.empty and "created_at" in bills_df.columns:
    today_bills = bills_df[bills_df["created_at"].str.startswith(today_str, na=False)]
    todays_sales = today_bills["grand_total"].sum() if "grand_total" in today_bills.columns else 0.0
    todays_orders = len(today_bills)
else:
    saved_b = st.session_state.get("saved_bills", [])
    todays_sales = sum(b.get("grand_total", 0) for b in saved_b)
    todays_orders = len(saved_b)

total_products = len(df) if not df.empty else 0
low_stock_count = len(df[df["stock"] <= df["min_stock"]]) if not df.empty else 0

k1, k2, k3, k4 = st.columns(4)
with k1:
    st.metric("💰 Today's Sales", f"₹{todays_sales:,.2f}")
with k2:
    st.metric("📦 Total Products", f"{total_products:,} SKUs")
with k3:
    st.metric("⚠️ Low Stock", f"{low_stock_count} Items", delta=f"{low_stock_count} Need Reorder" if low_stock_count > 0 else "All Healthy", delta_color="inverse")
with k4:
    st.metric("🛒 Today's Orders", f"{todays_orders} Bills")

# ── 3. QUICK ACTIONS (COMPACT DIRECTLY BELOW KPIs) ──────
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

# ── 4. MAIN DASHBOARD GRID (2-COLUMN BALANCED VIEWPORT) ────
col_left, col_right = st.columns([1.1, 1])

with col_left:
    st.subheader("⚠️ Low Stock Alerts")
    if not df.empty:
        low_df = df[df["stock"] <= df["min_stock"]].sort_values("stock")
        if low_df.empty:
            st.success("✅ All products are sufficiently stocked.")
        else:
            disp_low = low_df[["product_name", "stock", "min_stock", "market"]].copy()
            disp_low.columns = ["Product", "Current Stock", "Min Limit", "Mandi Market"]
            st.dataframe(disp_low, use_container_width=True, hide_index=True, height=210)
            if st.button("⚡ Restock Low Items (+10 units)", key="dash_quick_refill", use_container_width=True):
                conn = sqlite3.connect("retailmind.db")
                conn.execute("UPDATE products SET stock = stock + 10 WHERE stock <= min_stock")
                conn.commit()
                conn.close()
                st.cache_data.clear()
                st.success("✅ Low stock items restocked successfully!")
                st.rerun()

with col_right:
    st.subheader("📊 Today's Market Rates")
    if not df.empty:
        mkt_summary = df[["product_name", "market", "purchase_price", "last_updated_date"]].head(5).copy()
        mkt_summary.columns = ["Product", "Market", "Wholesale Rate", "Last Updated"]
        mkt_summary["Wholesale Rate"] = mkt_summary["Wholesale Rate"].map("₹{:.2f}".format)
        st.dataframe(mkt_summary, use_container_width=True, hide_index=True, height=210)
        if st.button("📊 View All Market Rates", key="dash_view_rates", use_container_width=True):
            st.session_state["redirect_page"] = "📊 Market Rates"
            st.rerun()

st.write("")

# ── 5. RECENT SALES SECTION ──────────────────────────────
st.subheader("🧾 Recent Sales")
saved_bills = st.session_state.get("saved_bills", [])
if saved_bills:
    recent_df = pd.DataFrame(saved_bills).tail(6)[["bill_no", "customer_name", "items_count", "grand_total", "created_at"]]
    recent_df.columns = ["Bill No.", "Customer", "Items", "Amount", "Time"]
    recent_df["Amount"] = recent_df["Amount"].map("₹{:.2f}".format)
    
    r_col1, r_col2 = st.columns([4, 1])
    with r_col1:
        st.dataframe(recent_df, use_container_width=True, hide_index=True)
    with r_col2:
        st.write("")
        if st.button("📋 View All Sales", use_container_width=True, key="dash_view_all_sales"):
            st.session_state["redirect_page"] = "🛒 Sales / POS Billing"
            st.rerun()
else:
    st.info("No sales recorded today.")

st.write("")

# ── 6. INVENTORY OVERVIEW & 7. BUSINESS INSIGHT ──────────
io_col, bi_col = st.columns([1.3, 1])

with io_col:
    st.subheader("📦 Inventory Overview")
    if not df.empty:
        total_items_cnt = len(df)
        low_stock_cnt = len(df[df["stock"] <= df["min_stock"]])
        out_stock_cnt = len(df[df["stock"] == 0])
        total_inv_val = df["stock_value"].sum()

        i1, i2, i3, i4 = st.columns(4)
        with i1:
            st.metric("Total Items", f"{total_items_cnt}")
        with i2:
            st.metric("Low Stock", f"{low_stock_cnt}")
        with i3:
            st.metric("Out of Stock", f"{out_stock_cnt}")
        with i4:
            st.metric("Stock Value", f"₹{total_inv_val/1000:,.1f}k" if total_inv_val >= 100000 else f"₹{total_inv_val:,.0f}")

with bi_col:
    st.subheader("💡 Business Insight")
    if not df.empty:
        top_cat = df.groupby("category")["stock_value"].sum().idxmax()
        top_cat_val = df.groupby("category")["stock_value"].sum().max()
        
        st.info(f"""
        • **Low Stock Alert:** {low_stock_count} products are running low in stock and need reordering.
        • **Category Valuation:** **{top_cat}** category has the highest stock value at **₹{top_cat_val:,.0f}**.
        • **Sales Summary:** Today's recorded store sales stand at **₹{todays_sales:,.2f}**.
        """)

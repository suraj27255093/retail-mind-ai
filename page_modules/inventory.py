import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# =========================================================
# INVENTORY PAGE — loaded as module from app.py
# =========================================================

from database.db_manager import DatabaseManager
from services.ml_forecasting import MLForecastingEngine

@st.cache_data(ttl=30)
def load_inventory():
    df = DatabaseManager.get_products_dataframe()
    df["stock_status"] = df.apply(lambda r: "🔴 Critical" if r["stock"] <= r["min_stock"] else ("🟡 Low" if r["stock"] <= r["min_stock"] * 1.5 else "🟢 Healthy"), axis=1)
    return df

df = load_inventory()

# Hero Header
st.markdown("""
<div class="rm-hero">
    <h1>📦 RetailMind AI — Smart Inventory Management</h1>
    <p>Monitor products, track stock health, refill alerts & update catalog prices in real-time</p>
</div>
""", unsafe_allow_html=True)

# KPI Metrics
low_stock_c = len(df[df['stock'] <= df['min_stock']])
total_stock_val = (df['selling_price'] * df['stock']).sum()
avg_stock = df['stock'].mean()
critical_items = len(df[df['stock_status'] == "🔴 Critical"])

c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    st.metric("📦 Total Products", len(df))
with c2:
    st.metric("📂 Categories", df["category"].nunique())
with c3:
    st.metric("⚠️ Low Stock Alerts", low_stock_c, delta=f"{low_stock_c} Need Reorder" if low_stock_c > 0 else "All Healthy", delta_color="inverse")
with c4:
    st.metric("💰 Total Stock Value", f"₹{total_stock_val:,.0f}")
with c5:
    st.metric("📊 Avg Stock Level", f"{avg_stock:.0f} units")

st.write("")

# 🔮 ML DEMAND & EXPIRY PREDICTION RADAR
ml_insights = MLForecastingEngine.analyze_inventory_health(df)
with st.expander("🔮 ML Demand Forecasting & Stock Expiry Radar (v3.0 Engine)", expanded=True):
    st.markdown("""
    <div style="background:linear-gradient(135deg, #0F172A 0%, #1E293B 100%); padding:18px; border-radius:16px; color:white; margin-bottom:15px;">
        <h4 style="margin:0 0 4px 0; color:#60A5FA;">⚡ Machine Learning Inventory Radar</h4>
        <p style="font-size:12px; color:#94A3B8; margin:0;">AI calculating Reorder Points ROP = (Daily Demand × Lead Time) + Safety Stock</p>
    </div>
    """, unsafe_allow_html=True)
    
    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1:
        st.markdown("**🚨 High Risk Stockouts Next 7 Days:**")
        if ml_insights["stockout_risk"]:
            for item in ml_insights["stockout_risk"]:
                st.error(f"• **{item['product']}**: Est. {item['est_days']} days left (Suggested ROP: {item['suggested_reorder']} units)")
        else:
            st.success("No immediate stockout risks detected.")

    with m_col2:
        st.markdown("**⏰ Expiry Watchlist (Next 45 Days):**")
        if ml_insights["expiry_watchlist"]:
            for item in ml_insights["expiry_watchlist"]:
                st.warning(f"• **{item['product']}**: Expiring {item['expiry_date']} ({item['days_remaining']} days left)")
        else:
            st.info("No items near expiration.")

    with m_col3:
        st.markdown("**📈 Demand Surge Radar:**")
        if ml_insights["demand_surges"]:
            for item in ml_insights["demand_surges"]:
                st.success(f"• **{item['product']}**: +{item['predicted_surge_pct']}% expected ({item['reason']})")

st.write("")

# Action Buttons
st.markdown("**⚡ Quick Inventory Controls:**")
b_col1, b_col2, b_col3, b_col4, b_col5 = st.columns(5)

filter_low = False
with b_col1:
    filter_low = st.checkbox("🚨 Low Stock Only", value=False, key="inv_low_stock_chk")
with b_col2:
    if st.button("⚡ Refill All Low Stock (+10)", use_container_width=True, key="inv_refill"):
        conn = sqlite3.connect("retailmind.db")
        conn.execute("UPDATE products SET stock = stock + 10 WHERE stock <= min_stock")
        conn.commit()
        conn.close()
        st.cache_data.clear()
        st.success("✅ Refilled all low stock items by +10 units!")
        st.rerun()
with b_col3:
    if st.button("🔔 Send Reorder Alerts", use_container_width=True, key="inv_alerts"):
        st.info(f"📩 Reorder alert dispatched for {low_stock_c} critical items to suppliers!")
with b_col4:
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Export Inventory CSV", csv, "Inventory_Report.csv", "text/csv", use_container_width=True, key="inv_export")
with b_col5:
    if st.button("🔄 Refresh Inventory", use_container_width=True, key="inv_refresh"):
        st.cache_data.clear()
        st.rerun()

st.write("")

# Tabs
t1, t2, t3 = st.tabs(["📦 Stock Table & Filters", "📊 Stock Health Charts", "➕ Add New Product"])

with t1:
    search_k = st.text_input("🔍 Search inventory", placeholder="Search by product name, category, brand, or market...")
    col_cat, col_mkt, col_status = st.columns(3)
    with col_cat:
        sel_cat = st.multiselect("Filter Category", df["category"].unique().tolist(), default=[])
    with col_mkt:
        sel_mkt = st.multiselect("Filter Market", df["market"].unique().tolist(), default=[])
    with col_status:
        sel_status = st.multiselect("Stock Status", ["🟢 Healthy", "🟡 Low", "🔴 Critical"], default=[])

    f_df = df.copy()
    if filter_low:
        f_df = f_df[f_df['stock'] <= f_df['min_stock']]
    if search_k:
        mask = (
            f_df['product_name'].str.contains(search_k, case=False, na=False) |
            f_df['category'].str.contains(search_k, case=False, na=False) |
            f_df.get('brand', pd.Series([""] * len(f_df))).str.contains(search_k, case=False, na=False)
        )
        f_df = f_df[mask]
    if sel_cat:
        f_df = f_df[f_df["category"].isin(sel_cat)]
    if sel_mkt:
        f_df = f_df[f_df["market"].isin(sel_mkt)]
    if sel_status:
        f_df = f_df[f_df["stock_status"].isin(sel_status)]

    st.markdown(f"**Showing {len(f_df)} of {len(df)} products**")
    display_cols = ['id', 'product_name', 'brand', 'category', 'unit', 'purchase_price', 'selling_price', 'profit_margin', 'stock', 'min_stock', 'stock_status', 'market', 'supplier']
    display_cols = [c for c in display_cols if c in f_df.columns]
    st.dataframe(f_df[display_cols], use_container_width=True, hide_index=True)

with t2:
    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        st.subheader("📊 Stock Levels by Category")
        cat_stock = df.groupby("category")["stock"].sum().reset_index()
        fig_s1 = px.bar(cat_stock, x="category", y="stock", color="stock",
                        title="Total Stock Units per Category",
                        color_continuous_scale="Blues")
        fig_s1.update_layout(paper_bgcolor="#FFFFFF")
        st.plotly_chart(fig_s1, use_container_width=True)

    with chart_col2:
        st.subheader("🚦 Stock Status Distribution")
        status_count = df["stock_status"].value_counts().reset_index()
        status_count.columns = ["Status", "Count"]
        color_map = {"🟢 Healthy": "#22C55E", "🟡 Low": "#F59E0B", "🔴 Critical": "#EF4444"}
        fig_s2 = px.pie(status_count, names="Status", values="Count",
                        title="Inventory Health Overview",
                        color="Status", color_discrete_map=color_map, hole=0.4)
        st.plotly_chart(fig_s2, use_container_width=True)

    st.subheader("⚠️ Critical Stock Items — Needs Immediate Reorder")
    crit_df = df[df["stock_status"] == "🔴 Critical"].sort_values("stock")
    if crit_df.empty:
        st.success("🎉 All inventory levels are healthy! No critical stock issues.")
    else:
        fig_s3 = px.bar(crit_df.head(15), x="product_name", y="stock",
                        color="stock", color_continuous_scale="Reds_r",
                        title=f"🚨 {len(crit_df)} Critical Stock Items (Units Remaining)")
        fig_s3.update_layout(paper_bgcolor="#FFFFFF")
        st.plotly_chart(fig_s3, use_container_width=True)

with t3:
    with st.form("new_p_form"):
        st.subheader("➕ Add New Product to Inventory")
        col_a, col_b = st.columns(2)
        with col_a:
            p_name = st.text_input("Product Name*")
            p_brand = st.text_input("Brand Name")
            p_cat = st.selectbox("Category*", df["category"].unique().tolist() + ["Other"])
            p_unit = st.selectbox("Unit", ["kg", "g", "litre", "ml", "pcs", "dozen", "bag"])
        with col_b:
            p_cost = st.number_input("Purchase Price (₹)*", min_value=0.0, value=100.0)
            p_sell = st.number_input("Selling Price (₹)*", min_value=0.0, value=120.0)
            p_stock = st.number_input("Initial Stock Units*", min_value=0, value=50)
            p_min_stock = st.number_input("Minimum Stock Alert Level", min_value=0, value=10)
            p_mkt = st.selectbox("Sourcing Market", df["market"].unique().tolist())

        sub = st.form_submit_button("💾 Save Product to Catalog", use_container_width=True)
        if sub and p_name:
            conn = sqlite3.connect("retailmind.db")
            conn.execute(
                "INSERT INTO products (product_name, brand, category, unit, purchase_price, selling_price, stock, min_stock, market) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (p_name, p_brand, p_cat, p_unit, p_cost, p_sell, p_stock, p_min_stock, p_mkt)
            )
            conn.commit()
            conn.close()
            st.cache_data.clear()
            st.success(f"✅ Product '{p_name}' added successfully!")
            st.rerun()
        elif sub and not p_name:
            st.error("Product Name is required!")
import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# =========================================================
# PAGE CONFIG & STYLING
# =========================================================




# =========================================================
# DATABASE LOAD
# =========================================================

@st.cache_data(ttl=60)
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
    return df

df = load_products()

if df.empty:
    st.warning("No products found in database.")
    st.stop()

# =========================================================
# HERO HEADER
# =========================================================

st.markdown("""
<div class="rm-hero">
    <h1>🛒 RetailMind AI — Executive Control Center</h1>
    <p>Real-Time Retail Analytics • Mandi Rate Benchmark • Inventory Health & AI Sales Insights</p>
</div>
""", unsafe_allow_html=True)

# =========================================================
# TOP METRICS
# =========================================================

total_products = len(df)
total_categories = df["category"].nunique()
total_markets = df["market"].nunique()
avg_price = df["selling_price"].mean()

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("📦 Total Active SKU Catalog", f"{total_products:,}")

with c2:
    st.metric("📂 Retail Categories", f"{total_categories}")

with c3:
    st.metric("🏪 Benchmark Mandi Markets", f"{total_markets}")

with c4:
    st.metric("💰 Avg Selling Rate", f"₹{avg_price:,.2f}")

st.write("")

# =========================================================
# VISUAL CHARTS
# =========================================================

l_col, r_col = st.columns([1.6, 1])

with l_col:
    st.subheader("📊 Category Average Selling Prices (₹)")
    cat_df = df.groupby("category")["selling_price"].mean().reset_index()
    fig1 = px.bar(
        cat_df, x="category", y="selling_price", color="selling_price",
        title="Category Benchmark Price Comparison",
        color_continuous_scale="Viridis"
    )
    fig1.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(248,250,252,0.6)",
        font=dict(family="Inter", color="#0F172A"),
        margin=dict(l=20, r=20, t=40, b=20)
    )
    st.plotly_chart(fig1, use_container_width=True)

with r_col:
    st.subheader("🏪 Product Sourcing Breakdown")
    fig2 = px.pie(
        df, names="market",
        title="Market Sourcing Distribution",
        hole=0.45,
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    fig2.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#0F172A"),
        margin=dict(l=20, r=20, t=40, b=20)
    )
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# =========================================================
# RECENT PRODUCTS TABLE
# =========================================================

st.subheader("📋 Top Stock Catalog Highlights")
display_cols = ['id', 'product_name', 'brand', 'category', 'unit', 'purchase_price', 'selling_price', 'market', 'supplier']
display_cols = [col for col in display_cols if col in df.columns]
st.dataframe(df[display_cols].head(10), use_container_width=True, hide_index=True)
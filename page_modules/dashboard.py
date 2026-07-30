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
    <h1>🛒 RetailMind AI — Executive Dashboard</h1>
    <p>AI Powered Retail & Market Intelligence Dashboard</p>
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
    st.metric("📦 Total Products", f"{total_products:,}")

with c2:
    st.metric("📂 Categories", total_categories)

with c3:
    st.metric("🏪 Markets", total_markets)

with c4:
    st.metric("💰 Avg Selling Price", f"₹{avg_price:,.2f}")

st.write("")

# =========================================================
# VISUAL CHARTS
# =========================================================

l_col, r_col = st.columns([1.5, 1])

with l_col:
    st.subheader("📊 Category Average Selling Prices")
    cat_df = df.groupby("category")["selling_price"].mean().reset_index()
    fig1 = px.bar(cat_df, x="category", y="selling_price", color="selling_price", title="Category Avg Price (₹)", color_continuous_scale="Blues")
    st.plotly_chart(fig1, use_container_width=True)

with r_col:
    st.subheader("🏪 Products per Market")
    fig2 = px.pie(df, names="market", title="Market Distribution", hole=0.4)
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# =========================================================
# RECENT PRODUCTS TABLE
# =========================================================

st.subheader("📋 Product Catalog Highlights")
st.dataframe(df[['id', 'product_name', 'brand', 'category', 'unit', 'purchase_price', 'selling_price', 'market', 'supplier']].head(10), use_container_width=True, hide_index=True)
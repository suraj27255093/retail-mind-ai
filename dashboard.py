import streamlit as st
import sqlite3
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="RetailMind AI Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------- DATABASE ----------------


def load_products():
    conn = sqlite3.connect("retailmind.db")
    df = pd.read_sql_query("SELECT * FROM products", conn)
    conn.close()
    return df

df = load_products()

# ---------------- TITLE ----------------

st.title("📊 RetailMind AI Dashboard")
st.caption("AI Powered Retail & Market Intelligence System")

st.divider()

# ---------------- METRICS ----------------

total_products = len(df)
total_categories = df["category"].nunique()
total_markets = df["market"].nunique()
average_selling_price = int(df["selling_price"].mean())

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📦 Products", total_products)

with col2:
    st.metric("📂 Categories", total_categories)

with col3:
    st.metric("🏪 Markets", total_markets)

with col4:
    st.metric("💰 Avg Selling_price", f"₹{average_selling_price}")

st.divider()

# ---------------- SEARCH ----------------

st.subheader("🔍 Search Products")

search = st.text_input(
    "Search by Product Name",
    placeholder="Example : Basmati Rice"
)

filtered_df = df.copy()

if search:
    filtered_df = filtered_df[
        filtered_df["product_name"].str.contains(
            search,
            case=False,
            na=False
        )
    ]

# ---------------- FILTERS ----------------

left, right = st.columns(2)

with left:

    category = st.selectbox(
        "📂 Select Category",
        ["All"] + sorted(df["category"].unique().tolist())
    )

with right:

    market = st.selectbox(
        "🏪 Select Market",
        ["All"] + sorted(df["market"].unique().tolist())
    )

if category != "All":
    filtered_df = filtered_df[
        filtered_df["category"] == category
    ]

if market != "All":
    filtered_df = filtered_df[
        filtered_df["market"] == market
    ]

st.success(f"Showing {len(filtered_df)} Products")

# =====================================================
# PRODUCT INSIGHTS
# =====================================================

st.divider()
st.subheader("📌 Product Insights")

if not filtered_df.empty:

    highest = filtered_df.loc[filtered_df["selling_price"].idxmax()]
    lowest = filtered_df.loc[filtered_df["selling_price"].idxmin()]

    c1, c2 = st.columns(2)

    with c1:
        st.success("🔥 Highest Selling_price Product")

        st.write("**Product:**", highest["product_name"])
        st.write("**Category:**", highest["category"])
        st.write("**Market:**", highest["market"])
        st.write("**Selling_price:** ₹", highest["selling_price"])

    with c2:
        st.info("💸 Lowest Selling_price Product")

        st.write("**Product:**", lowest["product_name"])
        st.write("**Category:**", lowest["category"])
        st.write("**Market:**", lowest["market"])
        st.write("**Selling_price:** ₹", lowest["selling_price"])

# =====================================================
# TOP 5 COSTLIEST PRODUCTS
# =====================================================

st.divider()

st.subheader("🏆 Top 5 Costliest Products")

top5 = filtered_df.sort_values(
    by="selling_price",
    ascending=False
).head(5)

st.dataframe(
    top5,
    use_container_width=True
)

# =====================================================
# TOP 5 CHEAPEST PRODUCTS
# =====================================================

st.subheader("💰 Top 5 Cheapest Products")

cheap5 = filtered_df.sort_values(
    by="selling_price"
).head(5)

st.dataframe(
    cheap5,
    use_container_width=True
)

# =====================================================
# CATEGORY SUMMARY
# =====================================================

st.divider()

st.subheader("📊 Category Summary")

category_summary = filtered_df.groupby(
    "category"
)["selling_price"].agg(
    ["count", "min", "max", "mean"]
)

category_summary.columns = [
    "Products",
    "Lowest",
    "Highest",
    "Average"
]

st.dataframe(
    category_summary,
    use_container_width=True
)

# =====================================================
# MARKET SUMMARY
# =====================================================

st.divider()

st.subheader("🏪 Market Wise Summary")

market_summary = filtered_df.groupby(
    "market"
)["selling_price"].agg(
    ["count", "min", "max", "mean"]
)

market_summary.columns = [
    "Products",
    "Lowest",
    "Highest",
    "Average"
]

st.dataframe(
    market_summary,
    use_container_width=True
)

# =====================================================
# CATEGORY CHART
# =====================================================

st.divider()

st.subheader("📈 Products by Category")

cat_chart = filtered_df.groupby(
    "category"
).size()

st.bar_chart(cat_chart)

# =====================================================
# MARKET CHART
# =====================================================

st.subheader("🏪 Products by Market")

market_chart = filtered_df.groupby(
    "market"
).size()

st.bar_chart(market_chart)

# =====================================================
# COMPLETE DATABASE
# =====================================================

st.divider()

st.subheader("📋 Complete Product Database")

st.dataframe(
    filtered_df,
    use_container_width=True,
    height=500
)
# ==========================================================
# SELLING_PRICE ANALYTICS
# ==========================================================

st.divider()
st.subheader("💹 Selling_price Analytics")

col1, col2 = st.columns(2)

with col1:

    highest_selling_price = filtered_df["selling_price"].max()
    lowest_selling_price = filtered_df["selling_price"].min()
    avg_selling_price = filtered_df["selling_price"].mean()

    st.metric("Highest Selling_price", f"₹ {highest_selling_price}")
    st.metric("Lowest Selling_price", f"₹ {lowest_selling_price}")
    st.metric("Average Selling_price", f"₹ {avg_selling_price:.2f}")

with col2:

    total_stock = len(filtered_df)

    expensive = filtered_df[filtered_df["selling_price"] > avg_selling_price]

    cheap = filtered_df[filtered_df["selling_price"] <= avg_selling_price]

    st.metric("Total Products", total_stock)
    st.metric("Above Average", len(expensive))
    st.metric("Below Average", len(cheap))

# ==========================================================
# MARKET COMPARISON
# ==========================================================

st.divider()

st.subheader("🏪 Market Comparison")

comparison = filtered_df.pivot_table(
    values="selling_price",
    index="market",
    columns="category",
    aggfunc="mean"
)

st.dataframe(comparison, use_container_width=True)

# ==========================================================
# SELLING_PRICE RANKING
# ==========================================================

st.divider()

st.subheader("🥇 Selling_price Ranking")

ranking = filtered_df.sort_values(
    "selling_price",
    ascending=False
)

ranking.insert(
    0,
    "Rank",
    range(1, len(ranking)+1)
)

st.dataframe(
    ranking,
    use_container_width=True
)

# ==========================================================
# MARKET LEADERBOARD
# ==========================================================

st.divider()

st.subheader("🏆 Top Markets")

leader = filtered_df.groupby("market")["selling_price"].mean()

leader = leader.sort_values(ascending=False)

st.bar_chart(leader)

# ==========================================================
# CATEGORY LEADERBOARD
# ==========================================================

st.subheader("📦 Top Categories")

leader2 = filtered_df.groupby("category")["selling_price"].mean()

leader2 = leader2.sort_values(ascending=False)

st.bar_chart(leader2)

# ==========================================================
# AI ALERTS
# ==========================================================

st.divider()

st.subheader("🤖 AI Market Alerts")

highest = filtered_df.loc[filtered_df["selling_price"].idxmax()]
lowest = filtered_df.loc[filtered_df["selling_price"].idxmin()]

st.success(
    f"🔥 Highest selling_priced product is **{highest['product_name']}** "
    f"in **{highest['market']}** at **₹{highest['selling_price']}**."
)

st.info(
    f"💸 Lowest selling_priced product is **{lowest['product_name']}** "
    f"in **{lowest['market']}** at **₹{lowest['selling_price']}**."
)

if highest["selling_price"] > avg_selling_price * 1.5:
    st.warning(
        "⚠ Selling_price is much higher than average. Check before purchasing."
    )

if lowest["selling_price"] < avg_selling_price * 0.7:
    st.success(
        "✅ Great buying opportunity detected."
    )

# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.caption("RetailMind AI Pro Version 2.0")

# ==========================================================
# SELLING_PRICE RANGE FILTER
# ==========================================================

st.divider()
st.subheader("💰 Selling_price Filter")

min_selling_price = int(filtered_df["selling_price"].min())
max_selling_price = int(filtered_df["selling_price"].max())

selling_price_range = st.slider(
    "Select Selling_price Range",
    min_value=min_selling_price,
    max_value=max_selling_price,
    value=(min_selling_price, max_selling_price)
)

filtered_df = filtered_df[
    (filtered_df["selling_price"] >= selling_price_range[0]) &
    (filtered_df["selling_price"] <= selling_price_range[1])
]

st.success(f"Filtered Products : {len(filtered_df)}")

# ==========================================================
# TOP 10 EXPENSIVE PRODUCTS
# ==========================================================

st.divider()
st.subheader("🔥 Top 10 Most Expensive Products")

expensive = filtered_df.sort_values(
    "selling_price",
    ascending=False
).head(10)

st.dataframe(expensive, use_container_width=True)

# ==========================================================
# TOP 10 CHEAPEST PRODUCTS
# ==========================================================

st.subheader("💸 Top 10 Cheapest Products")

cheap = filtered_df.sort_values(
    "selling_price"
).head(10)

st.dataframe(cheap, use_container_width=True)

# ==========================================================
# MARKET SELLING_PRICE TABLE
# ==========================================================

st.divider()

st.subheader("🏪 Market Selling_price Comparison")

comparison = filtered_df.pivot_table(
    index="market",
    columns="category",
    values="selling_price",
    aggfunc="mean"
)

st.dataframe(comparison, use_container_width=True)

# ==========================================================
# CATEGORY PIE CHART
# ==========================================================

st.divider()

st.subheader("🥧 Category Distribution")

category_count = filtered_df.groupby("category").size()

st.pyplot(category_count.plot.pie(
    autopct="%1.1f%%",
    ylabel=""
).figure)

# ==========================================================
# MARKET PIE CHART
# ==========================================================

st.subheader("🥧 Market Distribution")

market_count = filtered_df.groupby("market").size()

st.pyplot(market_count.plot.pie(
    autopct="%1.1f%%",
    ylabel=""
).figure)

# ==========================================================
# LIVE PRODUCT TABLE
# ==========================================================

st.divider()

st.subheader("📋 Live Product Table")

st.dataframe(
    filtered_df,
    use_container_width=True,
    height=600
)
# ==========================================================
# TODAY'S MARKET INSIGHTS
# ==========================================================

st.divider()
st.subheader("📢 Today's Market Insights")

highest_market = (
    filtered_df.groupby("market")["selling_price"]
    .mean()
    .sort_values(ascending=False)
)

lowest_market = (
    filtered_df.groupby("market")["selling_price"]
    .mean()
    .sort_values()
)

col1, col2 = st.columns(2)

with col1:
    st.success("🏆 Highest Average Selling_price Market")
    st.write(f"**{highest_market.index[0]}**")
    st.write(f"Average Selling_price : ₹ {highest_market.iloc[0]:.2f}")

with col2:
    st.info("💰 Cheapest Market")
    st.write(f"**{lowest_market.index[0]}**")
    st.write(f"Average Selling_price : ₹ {lowest_market.iloc[0]:.2f}")

# ==========================================================
# CATEGORY LEADERBOARD
# ==========================================================

st.divider()
st.subheader("🥇 Category Leaderboard")

leaderboard = (
    filtered_df.groupby("category")["selling_price"]
    .agg(["count", "mean", "min", "max"])
    .reset_index()
)

leaderboard.columns = [
    "Category",
    "Products",
    "Average Selling_price",
    "Lowest Selling_price",
    "Highest Selling_price"
]

leaderboard = leaderboard.sort_values(
    by="Average Selling_price",
    ascending=False
)

st.dataframe(leaderboard, use_container_width=True)

# ==========================================================
# AI SHOPPING SUGGESTIONS
# ==========================================================

st.divider()
st.subheader("🤖 AI Shopping Suggestions")

avg_selling_price = filtered_df["selling_price"].mean()

cheap_products = filtered_df[
    filtered_df["selling_price"] < avg_selling_price
]

expensive_products = filtered_df[
    filtered_df["selling_price"] > avg_selling_price
]

st.success(
    f"✅ {len(cheap_products)} products are below average selling_price."
)

st.warning(
    f"⚠ {len(expensive_products)} products are above average selling_price."
)

# ==========================================================
# QUICK STATS
# ==========================================================

st.divider()
st.subheader("⚡ Quick Statistics")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Total Products", len(filtered_df))

with c2:
    st.metric("Categories", filtered_df["category"].nunique())

with c3:
    st.metric("Markets", filtered_df["market"].nunique())

with c4:
    st.metric(
        "Average Selling_price",
        f"₹ {filtered_df['selling_price'].mean():.2f}"
    )

# ==========================================================
# RECENT PRODUCTS
# ==========================================================

st.divider()
st.subheader("🆕 Recently Added Products")

recent = filtered_df.tail(10)

st.dataframe(recent, use_container_width=True)

# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.caption("🚀 RetailMind AI Pro | Version 2.0")

# ==========================================================
# DASHBOARD FINAL WIDGETS
# ==========================================================

from datetime import datetime

st.divider()
st.subheader("🕒 Dashboard Information")

col1, col2, col3 = st.columns(3)

with col1:
    st.info(f"📅 Date : {datetime.now().strftime('%d-%m-%Y')}")

with col2:
    st.info(f"⏰ Time : {datetime.now().strftime('%H:%M:%S')}")

with col3:
    hour = datetime.now().hour
    if 9 <= hour <= 18:
        st.success("🟢 Market Status : OPEN")
    else:
        st.error("🔴 Market Status : CLOSED")

# ==========================================================
# QUICK ACTIONS
# ==========================================================

st.divider()
st.subheader("⚡ Quick Actions")

c1, c2, c3 = st.columns(3)

with c1:
    if st.button("🔄 Refresh Dashboard"):
        st.cache_data.clear()
        st.rerun()

with c2:
    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Download CSV",
        csv,
        "RetailMind_Data.csv",
        "text/csv"
    )

with c3:
    st.metric("Database Rows", len(filtered_df))

# ==========================================================
# CATEGORY COUNT
# ==========================================================

st.divider()
st.subheader("📦 Category Product Count")

category_count = (
    filtered_df.groupby("category")
    .size()
    .reset_index(name="Products")
)

st.dataframe(category_count, use_container_width=True)

# ==========================================================
# MARKET COUNT
# ==========================================================

st.subheader("🏪 Market Product Count")

market_count = (
    filtered_df.groupby("market")
    .size()
    .reset_index(name="Products")
)

st.dataframe(market_count, use_container_width=True)

# ==========================================================
# SELLING_PRICE ALERTS
# ==========================================================

st.divider()
st.subheader("🚨 Selling_price Alerts")

avg = filtered_df["selling_price"].mean()

high = filtered_df[filtered_df["selling_price"] > avg * 1.30]

low = filtered_df[filtered_df["selling_price"] < avg * 0.70]

if len(high) > 0:
    st.warning(f"⚠ {len(high)} products are selling_priced much higher than average.")

if len(low) > 0:
    st.success(f"✅ {len(low)} products are available at very low selling_prices.")

# ==========================================================
# DASHBOARD SUMMARY
# ==========================================================

st.divider()
st.subheader("📊 Dashboard Summary")

summary = {
    "Total Products": len(filtered_df),
    "Categories": filtered_df["category"].nunique(),
    "Markets": filtered_df["market"].nunique(),
    "Highest Selling_price": filtered_df["selling_price"].max(),
    "Lowest Selling_price": filtered_df["selling_price"].min(),
    "Average Selling_price": round(filtered_df["selling_price"].mean(), 2)
}

st.json(summary)

# ==========================================================
# FOOTER
# ==========================================================

st.divider()
st.caption("🛒 RetailMind AI | Built using Python • Streamlit • SQLite")

# ==========================================================
# MARKET PERFORMANCE
# ==========================================================

st.divider()
st.subheader("🏪 Market Performance")

market_stats = filtered_df.groupby("market").agg({
    "selling_price": ["mean", "max", "min", "count"]
})

market_stats.columns = [
    "Average Selling_price",
    "Highest Selling_price",
    "Lowest Selling_price",
    "Products"
]

st.dataframe(market_stats, use_container_width=True)

# ==========================================================
# CATEGORY PERFORMANCE
# ==========================================================

st.divider()
st.subheader("📦 Category Performance")

category_stats = filtered_df.groupby("category").agg({
    "selling_price": ["mean", "max", "min", "count"]
})

category_stats.columns = [
    "Average Selling_price",
    "Highest Selling_price",
    "Lowest Selling_price",
    "Products"
]

st.dataframe(category_stats, use_container_width=True)

# ==========================================================
# TOP 5 PREMIUM PRODUCTS
# ==========================================================

st.divider()
st.subheader("💎 Premium Products")

premium = filtered_df.nlargest(5, "selling_price")

for _, row in premium.iterrows():
    st.success(
        f"🏆 {row['product_name']} | ₹{row['selling_price']} | {row['market']}"
    )

# ==========================================================
# TOP 5 BUDGET PRODUCTS
# ==========================================================

st.subheader("💸 Budget Products")

budget = filtered_df.nsmallest(5, "selling_price")

for _, row in budget.iterrows():
    st.info(
        f"✅ {row['product_name']} | ₹{row['selling_price']} | {row['market']}"
    )

# ==========================================================
# DATABASE HEALTH
# ==========================================================

st.divider()
st.subheader("🗄️ Database Health")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Rows", len(filtered_df))

with c2:
    st.metric("Columns", len(filtered_df.columns))

with c3:
    st.metric("Missing Values", filtered_df.isnull().sum().sum())

# ==========================================================
# SYSTEM STATUS
# ==========================================================

st.divider()
st.subheader("🖥️ System Status")

st.success("🟢 Database Connected")
st.success("🟢 Dashboard Running")
st.success("🟢 AI Module Ready")
st.success("🟢 Analytics Loaded")

# ==========================================================
# DEVELOPER INFO
# ==========================================================

st.divider()

with st.expander("ℹ️ About RetailMind AI"):
    st.write("""
    ### RetailMind AI

    AI Powered Retail & Market Intelligence System

    Features:
    - 📊 Dashboard
    - 📦 Inventory
    - 🌾 Market Rates
    - 📈 Analytics
    - 🤖 AI Assistant
    - 🏪 Suppliers
    - 📄 Reports

    Version : 2.0
    """)

    # ==========================================================
# PRODUCT RECOMMENDATION PANEL
# ==========================================================

st.divider()
st.subheader("⭐ Best Buying Recommendations")

recommend = filtered_df.sort_values("selling_price").head(5)

for i, row in recommend.iterrows():

    st.success(
        f"""
✅ **{row['product_name']}**

📂 Category : {row['category']}

🏪 Market : {row['market']}

💰 Selling_price : ₹ {row['selling_price']}
"""
    )

# ==========================================================
# MOST EXPENSIVE CATEGORY
# ==========================================================

st.divider()
st.subheader("💎 Premium Category")

premium = filtered_df.groupby("category")["selling_price"].mean()

premium = premium.sort_values(ascending=False)

st.dataframe(
    premium.reset_index().rename(
        columns={"selling_price":"Average Selling_price"}
    ),
    use_container_width=True
)

# ==========================================================
# MARKET RANKING
# ==========================================================

st.divider()

st.subheader("🏆 Best Markets Ranking")

market_rank = filtered_df.groupby("market")["selling_price"].mean()

market_rank = market_rank.sort_values()

market_rank = market_rank.reset_index()

market_rank.columns = [
    "Market",
    "Average Selling_price"
]

market_rank.insert(
    0,
    "Rank",
    range(1,len(market_rank)+1)
)

st.dataframe(
    market_rank,
    use_container_width=True
)

# ==========================================================
# DATABASE INFORMATION
# ==========================================================

st.divider()

st.subheader("🗄 Database Information")

st.write(f"Database Name : retailmind.db")

st.write(f"Total Records : {len(filtered_df)}")

st.write(f"Total Columns : {len(filtered_df.columns)}")

st.write(f"Categories : {filtered_df['category'].nunique()}")

st.write(f"Markets : {filtered_df['market'].nunique()}")

# ==========================================================
# PROJECT INFORMATION
# ==========================================================

st.divider()

with st.expander("📘 Project Information"):

    st.markdown("""
### RetailMind AI

AI Powered Grocery Store &
Market Intelligence System

Modules Included

- Dashboard
- Inventory
- Market Rates
- Suppliers
- Analytics
- AI Assistant

Technology

- Python
- Streamlit
- SQLite
- Pandas

Version

2.0 Professional
""")

# ==========================================================
# THANK YOU
# ==========================================================

st.divider()

st.success("🎉 Dashboard Loaded Successfully")

st.caption("© 2026 RetailMind AI | Developed by Suraj Shewale")
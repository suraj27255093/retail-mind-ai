import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json

# =========================================================
# REPORTS PAGE — loaded as module from app.py
# =========================================================

@st.cache_data(ttl=60)
def load_report_data():
    conn = sqlite3.connect("retailmind.db")
    df = pd.read_sql_query("SELECT * FROM products", conn)
    try:
        sup_df = pd.read_sql_query("SELECT * FROM suppliers", conn)
    except Exception:
        sup_df = pd.DataFrame()
    conn.close()

    if "selling_price" in df.columns and ("price" not in df.columns or df["price"].isnull().all()):
        df["price"] = df["selling_price"]
    elif "price" in df.columns and ("selling_price" not in df.columns or df["selling_price"].isnull().all()):
        df["selling_price"] = df["price"]
    df["selling_price"] = pd.to_numeric(df["selling_price"], errors="coerce").fillna(0)
    if "purchase_price" not in df.columns:
        df["purchase_price"] = df["selling_price"] * 0.85
    df["purchase_price"] = pd.to_numeric(df["purchase_price"], errors="coerce").fillna(0)
    df["profit_margin"] = df["selling_price"] - df["purchase_price"]
    df["margin_pct"] = (df["profit_margin"] / df["selling_price"].replace(0, 1)) * 100
    if "stock" not in df.columns:
        df["stock"] = 50
    df["stock"] = pd.to_numeric(df["stock"], errors="coerce").fillna(50)
    df["stock_value"] = df["selling_price"] * df["stock"]
    return df, sup_df

df, sup_df = load_report_data()

# Hero Header
st.markdown("""
<div class="rm-hero">
    <h1>📄 RetailMind AI — Business Reports & Data Export Center</h1>
    <p>Generate financial summaries, analytics reports, inventory audits & CSV/JSON exports</p>
</div>
""", unsafe_allow_html=True)

# Summary KPIs
total_revenue = df["stock_value"].sum()
total_margin = df["profit_margin"].sum()
avg_margin_pct = df["margin_pct"].mean()
total_products = len(df)

c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    st.metric("📦 Total Products", f"{total_products:,}")
with c2:
    st.metric("💰 Total Stock Value", f"₹{total_revenue:,.0f}")
with c3:
    st.metric("🔥 Total Profit Pool", f"₹{total_margin:,.0f}")
with c4:
    st.metric("📈 Avg Margin %", f"{avg_margin_pct:.1f}%")
with c5:
    st.metric("📂 Product Categories", df["category"].nunique())

st.write("")

# Report Generation Section
st.subheader("📊 Executive Financial Summary Report")

rep_data = {
    "Metric": [
        "Total Products in Catalog",
        "Product Categories",
        "Active Markets",
        "Average Selling Price",
        "Average Purchase Price",
        "Average Profit Margin",
        "Average Margin Percentage",
        "Total Inventory Stock Value",
        "Highest Priced Product",
        "Lowest Priced Product",
        "Most Profitable Product",
    ],
    "Value": [
        f"{total_products:,} items",
        f"{df['category'].nunique()} categories",
        f"{df['market'].nunique()} markets",
        f"₹{df['selling_price'].mean():.2f}",
        f"₹{df['purchase_price'].mean():.2f}",
        f"₹{df['profit_margin'].mean():.2f}",
        f"{avg_margin_pct:.1f}%",
        f"₹{total_revenue:,.2f}",
        f"{df.loc[df['selling_price'].idxmax(), 'product_name']} (₹{df['selling_price'].max():.2f})",
        f"{df.loc[df['selling_price'].idxmin(), 'product_name']} (₹{df['selling_price'].min():.2f})",
        f"{df.loc[df['profit_margin'].idxmax(), 'product_name']} (₹{df['profit_margin'].max():.2f})",
    ],
    "Status": [
        "✅ Healthy", "✅ Diversified", "✅ Multi-Source", "📊 Tracked",
        "📊 Tracked", "🔥 Profitable", "📈 Good Margins", "💰 Valued",
        "🏆 Premium", "💸 Budget Entry", "🥇 Top Performer"
    ]
}
rep_df = pd.DataFrame(rep_data)
st.dataframe(rep_df, use_container_width=True, hide_index=True)

st.write("")
st.divider()

# Export Section
st.subheader("📥 Data Export Center")
export_col1, export_col2, export_col3 = st.columns(3)

with export_col1:
    st.markdown("""
    <div style="background:#EFF6FF; padding:18px; border-radius:14px; border:1px solid #BFDBFE; margin-bottom:12px;">
        <div style="font-size:16px; font-weight:700; color:#1D4ED8;">📦 Full Product Catalog</div>
        <div style="font-size:13px; color:#64748B; margin-top:4px;">All products with pricing, stock & supplier data</div>
    </div>
    """, unsafe_allow_html=True)
    csv_data = df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇ Download Catalog CSV", csv_data, f"RetailMind_Catalog_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv", use_container_width=True, key="rpt_dl_catalog")

with export_col2:
    st.markdown("""
    <div style="background:#F0FDF4; padding:18px; border-radius:14px; border:1px solid #BBF7D0; margin-bottom:12px;">
        <div style="font-size:16px; font-weight:700; color:#16A34A;">📊 Analytics Summary</div>
        <div style="font-size:13px; color:#64748B; margin-top:4px;">Category-wise avg price, margin & performance</div>
    </div>
    """, unsafe_allow_html=True)
    analytics_csv = df.groupby("category").agg(
        AvgSelling=("selling_price", "mean"),
        AvgPurchase=("purchase_price", "mean"),
        AvgMargin=("profit_margin", "mean"),
        AvgMarginPct=("margin_pct", "mean"),
        TotalProducts=("id", "count"),
        TotalStockValue=("stock_value", "sum")
    ).reset_index().to_csv().encode("utf-8")
    st.download_button("⬇ Download Analytics CSV", analytics_csv, f"Analytics_Summary_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv", use_container_width=True, key="rpt_dl_analytics")

with export_col3:
    st.markdown("""
    <div style="background:#FFF7ED; padding:18px; border-radius:14px; border:1px solid #FED7AA; margin-bottom:12px;">
        <div style="font-size:16px; font-weight:700; color:#C2410C;">🔧 System Config JSON</div>
        <div style="font-size:13px; color:#64748B; margin-top:4px;">System diagnostics, DB stats & config export</div>
    </div>
    """, unsafe_allow_html=True)
    sys_config = {
        "app_name": "RetailMind AI",
        "version": "2.0",
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "database": "retailmind.db",
        "total_products": total_products,
        "total_categories": df["category"].nunique(),
        "total_markets": df["market"].nunique(),
        "avg_selling_price": round(df["selling_price"].mean(), 2),
        "avg_profit_margin_pct": round(avg_margin_pct, 2),
        "total_stock_value": round(total_revenue, 2),
        "status": "Healthy"
    }
    st.download_button("⬇ Download System JSON", json.dumps(sys_config, indent=4).encode("utf-8"),
                       "RetailMind_Config.json", "application/json", use_container_width=True, key="rpt_dl_config")

st.write("")
st.divider()

# Profit Analysis Charts
st.subheader("📈 Visual Business Performance Reports")

chart_r1, chart_r2 = st.columns(2)

with chart_r1:
    cat_summary = df.groupby("category").agg(
        Revenue=("stock_value", "sum"),
        Margin=("profit_margin", "sum"),
        Products=("id", "count")
    ).reset_index()
    fig_rev = px.bar(
        cat_summary, x="category",
        y=["Revenue", "Margin"],
        barmode="group",
        title="💰 Revenue vs Profit by Category (₹)",
        color_discrete_map={"Revenue": "#2563EB", "Margin": "#10B981"}
    )
    fig_rev.update_layout(paper_bgcolor="#FFFFFF")
    st.plotly_chart(fig_rev, use_container_width=True)

with chart_r2:
    mkt_summary = df.groupby("market").agg(
        AvgMarginPct=("margin_pct", "mean"),
        Products=("id", "count"),
        TotalRevenue=("stock_value", "sum")
    ).reset_index()
    fig_mkt = px.scatter(
        mkt_summary, x="AvgMarginPct", y="TotalRevenue",
        size="Products", color="market",
        title="🏪 Market Profitability Matrix",
        labels={"AvgMarginPct": "Avg Margin %", "TotalRevenue": "Total Revenue (₹)"},
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_mkt.update_layout(paper_bgcolor="#FFFFFF")
    st.plotly_chart(fig_mkt, use_container_width=True)

# Top products table
st.write("")
st.subheader("🏆 Top 15 Products — Revenue & Margin Leaders")
top_products = df.nlargest(15, "stock_value")[
    ["product_name", "brand", "category", "selling_price", "purchase_price", "profit_margin", "margin_pct", "stock", "stock_value", "market"]
]
st.dataframe(
    top_products.style.format({
        "selling_price": "₹{:.2f}",
        "purchase_price": "₹{:.2f}",
        "profit_margin": "₹{:.2f}",
        "margin_pct": "{:.1f}%",
        "stock_value": "₹{:.0f}"
    }),
    use_container_width=True,
    hide_index=True
)
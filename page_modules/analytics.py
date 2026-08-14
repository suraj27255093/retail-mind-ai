import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =========================================================
# ANALYTICS PAGE — loaded as module from app.py
# =========================================================

# Database Load
def load_analytics_data():
    conn = sqlite3.connect("retailmind.db")
    df = pd.read_sql_query("SELECT * FROM products", conn)
    conn.close()
    if df.empty:
        return df
    if "selling_price" in df.columns and ("price" not in df.columns or df["price"].isnull().all()):
        df["price"] = df["selling_price"]
    elif "price" in df.columns and ("selling_price" not in df.columns or df["selling_price"].isnull().all()):
        df["selling_price"] = df["price"]
    df["price"] = pd.to_numeric(df["price"], errors="coerce").fillna(0)
    df["selling_price"] = pd.to_numeric(df["selling_price"], errors="coerce").fillna(0)
    if "purchase_price" not in df.columns:
        df["purchase_price"] = df["selling_price"] * 0.85
    df["purchase_price"] = pd.to_numeric(df["purchase_price"], errors="coerce").fillna(0)
    df["profit_margin"] = df["selling_price"] - df["purchase_price"]
    df["margin_pct"] = (df["profit_margin"] / df["selling_price"].replace(0, 1)) * 100
    if "stock" not in df.columns:
        df["stock"] = 50
    return df

df = load_analytics_data()

# Hero Header
st.markdown("""
<div class="rm-hero">
    <h1>📈 RetailMind AI — Business Analytics & Profit Intelligence</h1>
    <p>Smart Pricing Spread, Margin Analysis, & Retail Performance Forecasting</p>
</div>
""", unsafe_allow_html=True)

if df.empty:
    st.warning("No data found in database.")
    st.stop()

# KPI Metrics
highest = df.loc[df["selling_price"].idxmax()] if df["selling_price"].max() > 0 else df.iloc[0]
lowest = df.loc[df["selling_price"].idxmin()] if df["selling_price"].max() > 0 else df.iloc[0]
average = df["selling_price"].mean()
total_margin = df["profit_margin"].sum()
total_revenue_potential = df["selling_price"].sum()
avg_margin_pct = df["margin_pct"].mean()

c1, c2, c3, c4, c5, c6 = st.columns(6)
with c1:
    st.metric("💰 Highest Price", f"₹{highest['selling_price']:,.2f}")
with c2:
    st.metric("📉 Lowest Price", f"₹{lowest['selling_price']:,.2f}")
with c3:
    st.metric("📊 Average Price", f"₹{average:,.2f}")
with c4:
    st.metric("🔥 Total Margin Pool", f"₹{total_margin:,.0f}")
with c5:
    st.metric("📈 Avg Margin %", f"{avg_margin_pct:.1f}%")
with c6:
    st.metric("💵 Revenue Potential", f"₹{total_revenue_potential:,.0f}")

st.write("")

# Action Buttons
st.markdown("**⚡ Interactive Analytics Controls:**")
ab1, ab2, ab3, ab4, ab5 = st.columns(5)

with ab1:
    if st.button("🔮 Simulate 10% Price Surge", use_container_width=True, key="an_btn_surge"):
        sim_margin = total_margin * 1.10
        st.success(f"📈 10% Surge → Total Profit: **₹{sim_margin:,.2f}** (+₹{total_margin*0.10:,.2f})")

with ab2:
    if st.button("🏆 Top 5 Margin Items", use_container_width=True, key="an_btn_top5"):
        top5 = df.nlargest(5, "profit_margin")["product_name"].tolist()
        st.info(f"🔥 Top Margin Items: {', '.join(top5)}")

with ab3:
    if st.button("⚠️ Margin Below 10%", use_container_width=True, key="an_btn_lowmargin"):
        low_m = df[df["margin_pct"] < 10]
        st.warning(f"⚠️ {len(low_m)} products have margin below 10%! Consider repricing.")

with ab4:
    an_csv = df.groupby("category")[["purchase_price", "selling_price", "profit_margin"]].mean().to_csv().encode('utf-8')
    st.download_button("📥 Export Analytics CSV", an_csv, "Business_Analytics.csv", "text/csv", use_container_width=True, key="an_btn_export")

with ab5:
    if st.button("🔄 Recalculate Metrics", use_container_width=True, key="an_btn_recalc"):
        st.cache_data.clear()
        st.rerun()

st.write("")

# Charts Row 1
a1, a2 = st.columns(2)
with a1:
    st.subheader("💰 Price vs Cost Scatter Analysis")
    fig1 = px.scatter(
        df, x="purchase_price", y="selling_price", color="category",
        size="stock", hover_name="product_name",
        title="Selling Price vs Cost Price (Bubble = Stock Level)",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig1.update_layout(plot_bgcolor="#F8FAFC", paper_bgcolor="#FFFFFF")
    st.plotly_chart(fig1, use_container_width=True)

with a2:
    st.subheader("📊 Profit Margin by Category")
    cat_m = df.groupby("category").agg(
        AvgMargin=("profit_margin", "mean"),
        AvgMarginPct=("margin_pct", "mean"),
        ProductCount=("id", "count")
    ).reset_index()
    fig2 = px.bar(
        cat_m, x="category", y="AvgMargin",
        color="AvgMarginPct", text="ProductCount",
        title="Avg Profit Margin per Category (₹)",
        color_continuous_scale="Greens",
        labels={"AvgMargin": "Avg Margin (₹)", "AvgMarginPct": "Margin %"}
    )
    fig2.update_traces(texttemplate="%{text} items", textposition="outside")
    fig2.update_layout(plot_bgcolor="#F8FAFC", paper_bgcolor="#FFFFFF")
    st.plotly_chart(fig2, use_container_width=True)

# Charts Row 2
st.write("")
b1, b2 = st.columns(2)

with b1:
    st.subheader("🌐 Market-wise Revenue Analysis")
    mkt_rev = df.groupby("market").agg(
        TotalRevenue=("selling_price", "sum"),
        AvgPrice=("selling_price", "mean"),
        Products=("id", "count")
    ).reset_index()
    fig3 = px.bar(
        mkt_rev, x="market", y="TotalRevenue",
        color="AvgPrice", text="Products",
        title="Total Revenue Potential by Market (₹)",
        color_continuous_scale="Blues",
        labels={"TotalRevenue": "Revenue (₹)"}
    )
    fig3.update_traces(texttemplate="%{text} items", textposition="outside")
    fig3.update_layout(plot_bgcolor="#F8FAFC", paper_bgcolor="#FFFFFF")
    st.plotly_chart(fig3, use_container_width=True)

with b2:
    st.subheader("📦 Stock Value Distribution")
    if "stock" in df.columns:
        df["stock_value"] = df["selling_price"] * df["stock"]
        sv = df.groupby("category")["stock_value"].sum().reset_index()
        fig4 = px.pie(
            sv, names="category", values="stock_value",
            title="Inventory Stock Value by Category (₹)",
            hole=0.45,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig4, use_container_width=True)

# Trend Chart
st.write("")
st.subheader("📉 Price Range Heatmap — Category × Market")
heat_df = df.pivot_table(
    index="category", columns="market",
    values="selling_price", aggfunc="mean"
).fillna(0)

fig5 = go.Figure(data=go.Heatmap(
    z=heat_df.values,
    x=heat_df.columns.tolist(),
    y=heat_df.index.tolist(),
    colorscale="Blues",
    text=[[f"₹{v:.0f}" for v in row] for row in heat_df.values],
    texttemplate="%{text}",
    showscale=True
))
fig5.update_layout(
    title="Average Selling Price Heatmap (Category vs Market)",
    paper_bgcolor="#FFFFFF"
)
st.plotly_chart(fig5, use_container_width=True)

st.divider()
st.subheader("🔥 Top High Margin Products Table")

col_sort = st.selectbox("Sort by:", ["profit_margin", "margin_pct", "selling_price", "stock"], index=0, key="an_sort_select")
top_n = st.slider("Show top N products:", 5, 30, 10, key="an_topn_slider")

top_df = df.sort_values(col_sort, ascending=False).head(top_n)
display_cols = ['product_name', 'brand', 'category', 'purchase_price', 'selling_price', 'profit_margin', 'margin_pct', 'stock', 'market']
display_cols = [c for c in display_cols if c in top_df.columns]

st.dataframe(
    top_df[display_cols].style.format({
        "purchase_price": "₹{:.2f}",
        "selling_price": "₹{:.2f}",
        "profit_margin": "₹{:.2f}",
        "margin_pct": "{:.1f}%"
    }),
    use_container_width=True,
    hide_index=True
)
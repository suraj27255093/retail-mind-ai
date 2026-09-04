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

# ── 3. EXECUTIVE QUICK ACTION HUB ───────────────────────
st.markdown("<div style='font-size: 15px; font-weight: 800; color: #0F172A; margin-bottom: 10px;'>⚡ Quick Action Hub</div>", unsafe_allow_html=True)
q1, q2, q3, q4, q5 = st.columns(5)

with q1:
    if st.button("🌾 Mandi Rates", use_container_width=True, key="dash_qa_mandi"):
        st.session_state["redirect_page"] = "🌾 Market Rates"
        st.rerun()

with q2:
    if st.button("🧾 Fast Billing", use_container_width=True, key="dash_qa_pos"):
        st.session_state["redirect_page"] = "🧾 Billing & POS"
        st.rerun()

with q3:
    if st.button("🤖 Ask AI", use_container_width=True, key="dash_qa_ai"):
        st.session_state["redirect_page"] = "🤖 AI Assistant"
        st.rerun()

with q4:
    if st.button("🚨 Low Stock", use_container_width=True, key="dash_qa_stock"):
        st.session_state["redirect_page"] = "📦 Inventory Manager"
        st.rerun()

with q5:
    if st.button("📈 Profit Report", use_container_width=True, key="dash_qa_analytics"):
        st.session_state["redirect_page"] = "📈 Business Analytics"
        st.rerun()

st.write("")
st.divider()

# ── 4. MODERN COLOR-HARMONIZED VISUAL CHARTS ──────────
st.markdown("<div style='font-size: 18px; font-weight: 900; color: #0F172A; margin-bottom: 16px;'>📊 Strategic Business Performance Analytics</div>", unsafe_allow_html=True)
chart_col1, chart_col2 = st.columns([1.6, 1])

with chart_col1:
    cat_summary = df.groupby("category").agg(
        AvgSelling=("selling_price", "mean"),
        AvgPurchase=("purchase_price", "mean"),
        AvgMargin=("profit_margin", "mean"),
        ProductCount=("id", "count")
    ).reset_index().sort_values("AvgSelling", ascending=False)

    fig1 = go.Figure()
    fig1.add_trace(go.Bar(
        x=cat_summary["category"],
        y=cat_summary["AvgSelling"],
        name="Selling Price (₹)",
        marker_color="#2563EB",
        text=[f"₹{v:.1f}" for v in cat_summary["AvgSelling"]],
        textposition="auto"
    ))
    fig1.add_trace(go.Bar(
        x=cat_summary["category"],
        y=cat_summary["AvgPurchase"],
        name="Wholesale Purchase Rate (₹)",
        marker_color="#64748B",
        text=[f"₹{v:.1f}" for v in cat_summary["AvgPurchase"]],
        textposition="auto"
    ))
    fig1.add_trace(go.Bar(
        x=cat_summary["category"],
        y=cat_summary["AvgMargin"],
        name="Profit Margin (₹)",
        marker_color="#10B981",
        text=[f"₹{v:.1f}" for v in cat_summary["AvgMargin"]],
        textposition="auto"
    ))

    fig1.update_layout(
        title="<b>Category Price & Profit Margin Comparison (₹)</b>",
        barmode="group",
        bargap=0.2,
        bargroupgap=0.08,
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#F8FAFC",
        font=dict(family="Inter", size=12, color="#0F172A"),
        margin=dict(l=20, r=20, t=45, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        yaxis=dict(gridcolor="#E2E8F0", title="Amount (₹)"),
        xaxis=dict(gridcolor="#E2E8F0", title="Category")
    )
    st.plotly_chart(fig1, use_container_width=True)

with chart_col2:
    mkt_summary = df.groupby("market")["id"].count().reset_index()
    mkt_summary.columns = ["market", "count"]

    fig2 = px.pie(
        mkt_summary,
        values="count",
        names="market",
        title="<b>Market Sourcing Distribution</b>",
        hole=0.55,
        color_discrete_sequence=["#2563EB", "#10B981", "#8B5CF6", "#F59E0B"]
    )
    fig2.update_traces(
        textposition="inside",
        textinfo="percent+label",
        hoverinfo="label+value+percent",
        marker=dict(line=dict(color='#FFFFFF', width=2))
    )
    fig2.update_layout(
        paper_bgcolor="#FFFFFF",
        font=dict(family="Inter", size=12, color="#0F172A"),
        margin=dict(l=20, r=20, t=45, b=20),
        showlegend=False
    )
    st.plotly_chart(fig2, use_container_width=True)

st.write("")

# ── 5. TOP CATALOG HIGHLIGHTS & RISK WATCHLIST ─────────
st.markdown("<div style='font-size: 18px; font-weight: 900; color: #0F172A; margin-bottom: 14px;'>📋 Executive Catalog & Profit Leaderboard</div>", unsafe_allow_html=True)

table_col1, table_col2 = st.columns([2, 1])

with table_col1:
    st.subheader("🥇 Top Profit Margin Champions")
    top_margin_df = df.nlargest(7, "profit_margin")[
        ["product_name", "category", "selling_price", "purchase_price", "profit_margin", "margin_pct", "market"]
    ]
    st.dataframe(
        top_margin_df.style.format({
            "selling_price": "₹{:.2f}",
            "purchase_price": "₹{:.2f}",
            "profit_margin": "₹{:.2f}",
            "margin_pct": "{:.1f}%"
        }),
        use_container_width=True,
        hide_index=True
    )

with table_col2:
    st.subheader("🚨 Inventory Stock Watchlist")
    stock_watch = df[["product_name", "stock", "category"]].sort_values("stock", ascending=True).head(7)
    st.dataframe(
        stock_watch,
        use_container_width=True,
        hide_index=True
    )
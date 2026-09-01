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

# ── 1. VYAPAR STYLE HERO BANNER ────────────────────────
st.markdown("""
<div style="background: linear-gradient(135deg, #0F172A 0%, #1E88E5 50%, #1565C0 100%); padding: 34px 34px 28px 34px; border-radius: 26px; color: white; margin-bottom: 24px; box-shadow: 0 16px 40px -10px rgba(30,136,229,0.25); border: 1px solid rgba(255,255,255,0.18);">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px;">
        <div>
            <div style="display: inline-flex; align-items: center; gap: 8px; background: rgba(255,255,255,0.14); border: 1px solid rgba(255,255,255,0.25); backdrop-filter: blur(10px); padding: 5px 18px; border-radius: 20px; font-size: 12.5px; font-weight: 800; color: #E0E7FF; margin-bottom: 10px; letter-spacing: 0.5px;">
                ⚡ VYAPAR BUSINESS CONTROL CENTER
            </div>
            <h1 style="font-size: 32px; font-weight: 900; letter-spacing: -0.8px; margin: 0 0 6px 0; color: #FFFFFF; line-height: 1.2;">
                RetailMind AI — Vyapar Business & Mandi OS
            </h1>
            <p style="font-size: 15px; color: #CBD5E1; margin: 0; font-weight: 500;">
                Easy Retail Accounting • APMC Govt Mandi Benchmarks • Instant Billing & Stock Ledger
            </p>
        </div>
        <div style="display: flex; gap: 10px; flex-wrap: wrap;">
            <span style="background: rgba(16,185,129,0.25); border: 1px solid #10B981; padding: 6px 16px; border-radius: 20px; font-size: 12px; font-weight: 700; color: #6EE7B7;">
                🟢 4 Govt Mandi Feeds Active
            </span>
            <span style="background: rgba(255,255,255,0.12); border: 1px solid rgba(255,255,255,0.2); padding: 6px 16px; border-radius: 20px; font-size: 12px; font-weight: 700; color: #F1F5F9;">
                📱 Vyapar Simple Mode
            </span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── 2. VYAPAR LEDGER SUMMARY CARDS ──────────────────────
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
        label="💰 Total Sales & Stock Value (स्टॉक मूल्य)",
        value=f"₹{total_retail_val:,.2f}",
        delta=f"{total_products} Active SKUs"
    )

with kc2:
    st.metric(
        label="📥 Total Purchase Cost (खरीद लागत)",
        value=f"₹{total_cost_val:,.2f}",
        delta="APMC Mandi Base"
    )

with kc3:
    st.metric(
        label="🔥 Net Profit Pool (कुल लाभ)",
        value=f"₹{total_profit_pool:,.2f}",
        delta=f"Avg {avg_margin_pct:.1f}% Margin"
    )

with kc4:
    st.metric(
        label="🌾 Mandi Sourcing Hubs (मंडी बाजार)",
        value=f"{total_markets} APMC Hubs",
        delta="Nashik, Pune, Malegaon"
    )

st.write("")

# ── 3. VYAPAR QUICK ACTION BAR ─────────────────────────
st.markdown("<div style='font-size: 16px; font-weight: 800; color: #0F172A; margin-bottom: 12px;'>⚡ Vyapar Quick Action Bar</div>", unsafe_allow_html=True)
q1, q2, q3, q4, q5 = st.columns(5)

with q1:
    if st.button("➕ Add Sale (POS Billing)", use_container_width=True, key="dash_qa_pos"):
        st.info("💡 Open **🧾 Billing & POS** in sidebar for fast billing checkout!")

with q2:
    if st.button("📥 Purchase Mandi Rates", use_container_width=True, key="dash_qa_mandi"):
        st.info("💡 Open **🌾 Market Rates** in sidebar for APMC wholesale prices!")

with q3:
    if st.button("🤖 AI Assistant Search", use_container_width=True, key="dash_qa_ai"):
        st.info("💡 Open **🤖 AI Assistant** in sidebar for Hinglish queries!")

with q4:
    if st.button("📦 Stock Radar & Alerts", use_container_width=True, key="dash_qa_stock"):
        st.warning(f"🚨 **{low_stock_count} Items** have stock below safety reorder threshold!")

with q5:
    if st.button("📈 Profit Reports", use_container_width=True, key="dash_qa_analytics"):
        st.info("💡 Open **📈 Business Analytics** for category margin reports!")

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
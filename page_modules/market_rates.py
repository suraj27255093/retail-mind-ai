import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# =========================================================
# MARKET RATES PAGE — loaded as module from app.py
# =========================================================

from database.db_manager import DatabaseManager
from services.mandi_sync_service import MandiSyncEngine

# Auto-sync daily market rates on boot if not updated today
if "mandi_auto_synced" not in st.session_state:
    try:
        sync_res = MandiSyncEngine.auto_sync_mandi_prices()
        st.session_state["mandi_auto_synced"] = sync_res
    except Exception:
        pass

@st.cache_data(ttl=15)
def load_market_data():
    return DatabaseManager.get_products_dataframe()

df = load_market_data()

# Hero Header
st.markdown("""
<div class="rm-hero">
    <h1>🌾 RetailMind AI — Automated Market Rates & Mandi Intelligence</h1>
    <p>Live Daily Mandi Wholesale Price Feed • Nashik, Malegaon & Pune APMC Benchmark</p>
</div>
""", unsafe_allow_html=True)

today_date = datetime.now().strftime("%d %B %Y")
st.success(f"🟢 **Automated Daily Sync Active:** Mandi wholesale rates auto-updated for today (**{today_date}**) via APMC Live Market Engine (No manual entry required!).")

# KPI Cards
markets = df["market"].unique()
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("📦 Products Tracked", len(df))
with c2:
    st.metric("🏪 Active Markets", df["market"].nunique())
with c3:
    best_mkt = df.groupby("market")["selling_price"].mean().idxmin()
    cheapest_val = df.groupby("market")["selling_price"].mean().min()
    st.metric("🥇 Cheapest Market", best_mkt, delta=f"Avg ₹{cheapest_val:.2f}/item")
with c4:
    st.metric("📊 Avg Market Rate", f"₹{df['selling_price'].mean():.2f}")

st.write("")

# Action Buttons
st.markdown("**⚡ Market Intelligence Actions:**")
mb1, mb2, mb3, mb4, mb5 = st.columns(5)

with mb1:
    if st.button("🏆 Lowest Price Market", use_container_width=True, key="mkt_lowest"):
        st.success(f"🥇 **{best_mkt} Market** is the cheapest overall (Avg ₹{cheapest_val:.2f}/item)!")

with mb2:
    if st.button("📊 Market Comparison", use_container_width=True, key="mkt_compare"):
        mkt_avgs = df.groupby("market")["selling_price"].mean()
        msg = " | ".join([f"**{m}:** ₹{v:.2f}" for m, v in mkt_avgs.items()])
        st.info(f"⚖️ Market Average Rates: {msg}")

with mb3:
    if st.button("🔍 Price Arbitrage Finder", use_container_width=True, key="mkt_arbitrage"):
        piv = df.pivot_table(index="product_name", columns="market", values="selling_price", aggfunc="mean")
        piv = piv.dropna()
        if not piv.empty:
            piv["price_spread"] = piv.max(axis=1) - piv.min(axis=1)
            top_arb = piv.nlargest(3, "price_spread")
            st.info(f"💡 Top arbitrage opportunities: {', '.join(top_arb.index.tolist())} — buy low, sell high across markets!")

with mb4:
    mkt_csv = df.groupby(["market", "category"])["selling_price"].agg(["mean", "min", "max"]).to_csv().encode('utf-8')
    st.download_button("📥 Export Market Benchmark", mkt_csv, "Market_Benchmark.csv", "text/csv", use_container_width=True, key="mkt_export")

with mb5:
    if st.button("🔄 Auto-Sync Mandi Feed", use_container_width=True, key="mkt_refresh"):
        res = MandiSyncEngine.auto_sync_mandi_prices()
        st.cache_data.clear()
        st.success(f"✅ Market rates re-synced! Updated {res['items_updated']} catalog items.")
        st.rerun()

st.write("")

# Chart Tabs
tab_m1, tab_m2, tab_m3 = st.tabs(["📊 Price Distribution", "🔥 Market Comparison", "📋 Rate Table"])

with tab_m1:
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        fig1 = px.box(
            df, x="market", y="selling_price", color="category",
            title="Wholesale Price Variance Across Sourcing Markets (₹)",
            labels={"selling_price": "Price (₹)"}
        )
        fig1.update_layout(paper_bgcolor="#FFFFFF")
        st.plotly_chart(fig1, use_container_width=True)

    with col_m2:
        mkt_cat = df.groupby(["market", "category"])["selling_price"].mean().reset_index()
        fig2 = px.bar(
            mkt_cat, x="category", y="selling_price", color="market",
            barmode="group", title="Category Avg Price by Market (₹)",
            labels={"selling_price": "Avg Price (₹)"},
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig2.update_layout(paper_bgcolor="#FFFFFF")
        st.plotly_chart(fig2, use_container_width=True)

with tab_m2:
    market_summary = df.groupby("market").agg(
        AvgPrice=("selling_price", "mean"),
        MinPrice=("selling_price", "min"),
        MaxPrice=("selling_price", "max"),
        TotalProducts=("id", "count"),
        AvgPurchasePrice=("purchase_price", "mean")
    ).reset_index()

    fig3 = px.bar(
        market_summary, x="market",
        y=["AvgPrice", "AvgPurchasePrice"],
        barmode="group",
        title="🛒 Selling Price vs Purchase Price by Market (₹)",
        labels={"value": "Price (₹)"},
        color_discrete_map={"AvgPrice": "#2563EB", "AvgPurchasePrice": "#10B981"}
    )
    fig3.update_layout(paper_bgcolor="#FFFFFF")
    st.plotly_chart(fig3, use_container_width=True)

    col_sum1, col_sum2 = st.columns(2)
    for i, row in market_summary.iterrows():
        col = col_sum1 if i % 2 == 0 else col_sum2
        with col:
            st.markdown(f"""
            <div style="background:#FFFFFF; padding:16px; border-radius:14px; border:1px solid #E2E8F0; margin-bottom:12px;">
                <div style="font-size:20px; font-weight:800; color:#0F172A;">🏪 {row['market']}</div>
                <div style="color:#64748B; font-size:13px; margin-top:6px;">
                    📦 <b>{int(row['TotalProducts'])}</b> Products &nbsp;|&nbsp;
                    💰 Avg: <b>₹{row['AvgPrice']:.2f}</b><br>
                    📉 Min: <b>₹{row['MinPrice']:.2f}</b> &nbsp;|&nbsp;
                    📈 Max: <b>₹{row['MaxPrice']:.2f}</b>
                </div>
            </div>
            """, unsafe_allow_html=True)

with tab_m3:
    search_mkt = st.text_input("🔍 Search products", placeholder="Search by name, category...", key="mkt_search_inp")
    sel_market_filter = st.multiselect("Filter by Market", df["market"].unique().tolist(), default=[], key="mkt_filter_multi")

    view_df = df.copy()
    if search_mkt:
        view_df = view_df[view_df['product_name'].str.contains(search_mkt, case=False, na=False) |
                          view_df['category'].str.contains(search_mkt, case=False, na=False)]
    if sel_market_filter:
        view_df = view_df[view_df["market"].isin(sel_market_filter)]

    display_cols = ['product_name', 'brand', 'category', 'unit', 'purchase_price', 'selling_price', 'market', 'supplier']
    display_cols = [c for c in display_cols if c in view_df.columns]
    st.dataframe(view_df[display_cols].sort_values("selling_price"), use_container_width=True, hide_index=True)

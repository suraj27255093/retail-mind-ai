import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import re

# =====================================================
# PAGE STYLING
# =====================================================



# =====================================================
# DATABASE HELPER
# =====================================================

from database.db_manager import DatabaseManager
from services.ai_engine import AIEngine

@st.cache_data(ttl=30)
def get_products_data():
    return DatabaseManager.get_products_dataframe()

df = get_products_data()

# =====================================================
# HEADER
# =====================================================

st.markdown("""
<div class="rm-hero">
    <h1>🤖 RetailMind AI Assistant <span style="font-size:14px; background:rgba(255,255,255,0.2); padding:4px 12px; border-radius:20px;">v2.0 NLP Engine Active</span></h1>
    <p>Conversational Retail Intelligence • Hinglish/English NLU • Stock Alerts • Margin Analytics</p>
</div>
""", unsafe_allow_html=True)

if df.empty:
    st.warning("⚠️ No products found in retailmind.db. Please run database seeding.")
    st.stop()

# =====================================================
# TOP KPIs
# =====================================================

col1, col2, col3, col4, col5 = st.columns(5)
low_stock_count = len(df[df['stock'] <= df['min_stock']])
avg_margin = df['margin_pct'].mean()

with col1: st.metric("📦 Total Items", f"{len(df):,}")
with col2: st.metric("📂 Categories", df["category"].nunique())
with col3: st.metric("🏪 Markets", df["market"].nunique())
with col4: st.metric("💰 Avg Margin", f"{avg_margin:.1f}%")
with col5: st.metric("⚠️ Low Stock Alerts", low_stock_count,
                      delta=f"{low_stock_count} Items Needed" if low_stock_count > 0 else "Healthy Stock",
                      delta_color="inverse")

st.write("")

# =====================================================
# SMART NLP INTEL ENGINE
# =====================================================

def process_ai_query(user_query, df):
    """
    Priority-based NLP query processor.
    PRIORITY 0 (highest): Product + Market combo  → e.g. "sugar rate Malegaon"
    1: Low stock / reorder alerts
    2: Profit / margin queries
    3: Cheapest / sasta
    4: Expensive / mehanga
    5: Market-only query (no product)
    6: Category-only query
    7: Product-only query (no market)
    8: Budget filter
    9: Default executive summary
    """
    q = user_query.lower().strip()

    # ---- Keywords defined INSIDE function ----
    # This avoids Streamlit module-import cache causing stale data
    PRODUCT_KEYWORDS = [
        # Grains
        "rice", "chawal", "atta", "wheat", "gehun", "maida", "suji", "rawa",
        # Pulses
        "dal", "daal", "chana", "moong", "masoor", "urad", "toor", "arhar", "rajma",
        # Sugar & Sweeteners
        "sugar", "chini", "cheeni", "shakkar", "gur", "jaggery", "honey", "shehad",
        # Oil & Ghee
        "oil", "tel", "ghee", "vanaspati", "sunflower", "mustard", "soya",
        # Spices
        "masala", "haldi", "turmeric", "mirchi", "namak", "salt", "jeera", "cumin", "dhania", "pepper",
        # Tea & Coffee
        "tea", "chai", "coffee",
        # Dairy
        "milk", "doodh", "paneer", "curd", "dahi", "butter", "makhan", "cheese",
        # Snacks
        "biscuit", "chips", "namkeen", "wafer", "snack",
        # Instant Food
        "noodles", "maggi", "soup",
        # Drinks
        "juice", "soda", "water", "paani",
        # Sweets
        "chocolate", "candy", "toffee",
        # Personal Care
        "soap", "shampoo", "toothpaste", "cream",
        # Specific varieties
        "kolam", "basmati", "sona masoori", "ponni",
    ]

    KW_MAP = {
        "chawal": "rice", "gehun": "wheat",
        "cheeni": "sugar", "chini": "sugar", "shakkar": "sugar",
        "daal": "dal", "tel": "oil", "makhan": "butter",
        "doodh": "milk", "shehad": "honey", "paani": "water",
    }

    # --- Detect market ---
    matched_market = next((mk for mk in df['market'].unique() if mk.lower() in q), None)

    # --- Detect product keyword ---
    found_product_kw = next((kw for kw in PRODUCT_KEYWORDS if kw in q), None)

    # =========================================================
    # PRIORITY 0: Product + Market COMBO (Strict Filtering)
    # "sugar ka rate malegaon mai" / "kolam chawal nashik mein"
    # =========================================================
    if found_product_kw and matched_market:
        search_kw = KW_MAP.get(found_product_kw, found_product_kw)

        # STRICT FILTERING: Match ONLY the specific product and specific market
        combo_df = df[
            (df['market'].str.lower().str.contains(matched_market.lower())) &
            (
                df['product_name'].str.contains(search_kw, case=False, na=False) |
                df['name'].str.contains(search_kw, case=False, na=False) |
                df['category'].str.contains(search_kw, case=False, na=False)
            )
        ].sort_values("purchase_price").reset_index(drop=True)

        if combo_df.empty:
            ans = f"🔍 **{matched_market}** market mein **'{search_kw.title()}'** ka koi exact product data nahi mila."
            return ans, None, None

        # Build Card HTML Responses
        card_htmls = []
        now_date = datetime.now().strftime("%d %B %Y")

        for _, r in combo_df.iterrows():
            pur_p = float(r.get('purchase_price', r.get('selling_price', 0)))
            mrp_p = float(r.get('retail_mrp', r.get('selling_price', 0)))
            stock_u = int(r.get('stock', 0))
            unit_u = r.get('unit', 'kg')
            mkt_name = r.get('market', matched_market)
            supp_name = r.get('supplier', 'Standard Wholesale Supplier')
            last_dt = r.get('last_updated_date', now_date)
            status_st = r.get('stock_status', '🟢 Healthy')

            card_html = f"""
            <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-left:6px solid #2563EB; padding:20px; border-radius:18px; box-shadow:0 6px 20px rgba(15,23,42,0.04); margin-bottom:16px;">
                <div style="font-size:11px; font-weight:800; color:#2563EB; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:4px;">
                    🤖 AI MATCHED PRODUCT CARD
                </div>
                <div style="font-size:20px; font-weight:900; color:#0F172A; margin-bottom:12px;">
                    🍬 {r['product_name']}
                </div>
                <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap:10px; background:#F8FAFC; padding:12px 16px; border-radius:14px; border:1px solid #E2E8F0; font-size:13px;">
                    <div><b style="color:#64748B;">🏪 Market:</b><br><span style="color:#2563EB; font-weight:700;">{mkt_name}</span></div>
                    <div><b style="color:#64748B;">💰 Purchase Rate:</b><br><span style="color:#059669; font-weight:800;">₹{pur_p:.2f} / {unit_u}</span></div>
                    <div><b style="color:#64748B;">🏷️ Retail MRP:</b><br><span style="color:#1E293B; font-weight:800;">₹{mrp_p:.2f} / {unit_u}</span></div>
                    <div><b style="color:#64748B;">📦 Stock:</b><br><span style="color:#0F172A; font-weight:700;">{stock_u} {unit_u} ({status_st})</span></div>
                    <div><b style="color:#64748B;">🏢 Supplier:</b><br><span style="color:#475569; font-weight:600;">{supp_name}</span></div>
                    <div><b style="color:#64748B;">📅 Last Updated:</b><br><span style="color:#64748B; font-size:12px;">{last_dt}</span></div>
                </div>
            </div>
            """
            card_htmls.append(card_html)

        ans_text = "\n".join(card_htmls)

        chart = px.bar(
            combo_df, x="product_name", y="purchase_price",
            color="purchase_price", color_continuous_scale="Viridis",
            title=f"📊 '{search_kw.title()}' Wholesale Purchase Rates in {matched_market} (₹)",
            labels={"purchase_price": "Purchase Rate (₹)", "product_name": "Product"}
        )
        chart.update_layout(paper_bgcolor="#FFFFFF", plot_bgcolor="#F8FAFC", font=dict(family="Inter"))

        return ans_text, combo_df[['product_name', 'market', 'purchase_price', 'retail_mrp', 'stock', 'unit', 'supplier']], chart

    # 1. Low stock / Reorder
    elif any(k in q for k in ["low stock", "khatam", "stock alert", "reorder", "kam stock", "shortage", "out of stock"]):
        low_df = df[df['stock'] <= df['min_stock']].sort_values("stock")
        if low_df.empty:
            ans = "🎉 **Stock Health Status:** Sabhi products ka stock healthy hai! Kisi bhi item mein stock low nahi hai."
            chart = None
        else:
            ans = f"🚨 **Low Stock Alert:** **{len(low_df)} products** low stock limit par hain. Unhe jaldi reorder karein!"
            chart = px.bar(
                low_df.head(10), x="product_name", y="stock", color="stock",
                title="⚠️ Critical Low Stock Items (Units Remaining)",
                color_continuous_scale="Reds_r"
            )
        return ans, low_df[['product_name', 'category', 'stock', 'min_stock', 'supplier', 'market']], chart

    # 2. Profit / Margin
    elif any(k in q for k in ["profit", "margin", "munafa", "earning", "high margin", "zyada margin"]):
        margin_df = df.sort_values("profit_margin", ascending=False)
        top_m = margin_df.iloc[0]
        ans = (
            f"💰 **Highest Profit Margin:** **{top_m['product_name']}**\n"
            f"- Purchase: ₹{top_m['purchase_price']:.2f} | Selling: ₹{top_m['selling_price']:.2f}\n"
            f"- **Profit per Unit:** ₹{top_m['profit_margin']:.2f} ({top_m['margin_pct']:.1f}%)"
        )
        chart = px.bar(
            margin_df.head(10), x="product_name", y="profit_margin", color="margin_pct",
            labels={"profit_margin": "Profit (₹)", "margin_pct": "Margin %"},
            title="🔥 Top 10 Highest Margin Products"
        )
        return ans, margin_df[['product_name', 'category', 'purchase_price', 'selling_price', 'profit_margin', 'margin_pct']].head(10), chart

    # 3. Cheapest / Sasta
    elif any(k in q for k in ["cheapest", "sasta", "lowest price", "kam daam", "budget price"]):
        cheapest_df = df.sort_values("selling_price", ascending=True)
        top_c = cheapest_df.iloc[0]
        ans = f"💸 **Sabse Sasta:** **{top_c['product_name']}** at **₹{top_c['selling_price']}** ({top_c['market']} market)"
        chart = px.bar(
            cheapest_df.head(10), x="product_name", y="selling_price", color="selling_price",
            title="💸 Top 10 Cheapest Products (₹)", color_continuous_scale="Viridis"
        )
        return ans, cheapest_df[['product_name', 'category', 'market', 'selling_price', 'unit']].head(10), chart

    # 4. Expensive / Mehanga
    elif any(k in q for k in ["expensive", "mehanga", "highest price", "costliest", "premium"]):
        exp_df = df.sort_values("selling_price", ascending=False)
        top_e = exp_df.iloc[0]
        ans = f"🔥 **Sabse Mehanga:** **{top_e['product_name']}** at **₹{top_e['selling_price']}** ({top_e['market']} market)"
        chart = px.bar(
            exp_df.head(10), x="product_name", y="selling_price", color="selling_price",
            title="🔥 Top 10 Most Expensive Products (₹)", color_continuous_scale="Plasma"
        )
        return ans, exp_df[['product_name', 'category', 'market', 'selling_price', 'unit']].head(10), chart

    # 5. Market-only query
    elif matched_market:
        m_df = df[df['market'].str.lower() == matched_market.lower()]
        cat_summary = m_df.groupby('category').agg(
            AvgPrice=('selling_price', 'mean'), Products=('id', 'count')
        ).reset_index().sort_values('AvgPrice', ascending=False)
        ans = (
            f"🏪 **{matched_market} Market:** **{len(m_df)} products** available.\n"
            f"- Avg Selling Price: **₹{m_df['selling_price'].mean():.2f}**\n"
            f"- Top Category: **{cat_summary.iloc[0]['category']}**\n"
            f"- Total Categories: **{m_df['category'].nunique()}**\n\n"
            f"💡 *Tip: Specific product poochne ke liye likhein — e.g. 'sugar {matched_market} mein'*"
        )
        chart = px.bar(
            cat_summary, x="category", y="AvgPrice", color="Products",
            title=f"📊 {matched_market} — Category Average Prices (₹)",
            labels={"AvgPrice": "Avg Price (₹)"}, color_continuous_scale="Blues"
        )
        chart.update_layout(xaxis_tickangle=-30, paper_bgcolor="#FFFFFF")
        return ans, m_df[['product_name', 'category', 'selling_price', 'stock', 'supplier']].head(15), chart

    # 6. Category-only
    elif any(cat.lower() in q for cat in df['category'].unique()):
        matched_cat = next((c for c in df['category'].unique() if c.lower() in q), None)
        c_df = df[df['category'].str.lower() == matched_cat.lower()]
        ans = (
            f"📂 **{matched_cat} Category:** **{len(c_df)} products**\n"
            f"- Price Range: ₹{c_df['selling_price'].min():.0f} – ₹{c_df['selling_price'].max():.0f}"
        )
        chart = px.box(
            c_df, x="market", y="selling_price", points="all",
            title=f"📦 {matched_cat} — Price Distribution Across Markets"
        )
        return ans, c_df[['product_name', 'market', 'selling_price', 'stock', 'unit']], chart

    # 7. Product keyword only (no market)
    elif found_product_kw:
        search_kw = KW_MAP.get(found_product_kw, found_product_kw)
        p_df = df[
            df['product_name'].str.contains(search_kw, case=False, na=False) |
            df['category'].str.contains(search_kw, case=False, na=False)
        ]
        if p_df.empty:
            ans = f"🔍 **'{search_kw.title()}'** ke liye koi product nahi mila."
            return ans, None, None
        cheapest_match = p_df.loc[p_df['selling_price'].idxmin()]
        ans = (
            f"🔍 **{len(p_df)} '{search_kw.title()}' products** mil gaye:\n"
            f"- **Sabse Sasta:** {cheapest_match['product_name']} at **₹{cheapest_match['selling_price']}** in {cheapest_match['market']}\n"
            f"- Market-wise comparison neeche chart mein dekhen."
        )
        chart = px.bar(
            p_df, x="product_name", y="selling_price", color="market",
            title=f"📊 '{search_kw.title()}' — All Markets Price Comparison (₹)"
        )
        return ans, p_df[['product_name', 'category', 'market', 'selling_price', 'stock']], chart

    # 8. Budget
    elif "under" in q or "budget" in q:
        numbers = re.findall(r'\d+', q)
        budget_val = int(numbers[0]) if numbers else 100
        b_df = df[df['selling_price'] <= budget_val].sort_values("selling_price")
        ans = f"💰 **Budget ≤ ₹{budget_val}:** **{len(b_df)} products** available."
        chart = px.pie(b_df, names="category", title=f"📂 Budget Products Under ₹{budget_val}")
        return ans, b_df[['product_name', 'category', 'selling_price', 'market']].head(12), chart

    # 9. Default
    else:
        top_item = df.loc[df['selling_price'].idxmax()]
        low_item = df.loc[df['selling_price'].idxmin()]
        ans = f"""
🤖 **RetailMind AI — Kya jaanna chahte hain?**

Kuch examples try karein:
- 🔍 *"Sugar ka rate Malegaon mein"*
- 🔍 *"Kolam chawal Nashik mein"*
- 📦 *"Low stock items dikhao"*
- 💰 *"Sabse zyada margin wale products"*
- 💸 *"Sabse sasta item konsa hai"*
- 🏪 *"Pune market ka overview"*
- 📂 *"Grains category ki list"*

**Quick Stats:** {len(df)} products | Premium: {top_item['product_name']} (₹{top_item['selling_price']}) | Budget: {low_item['product_name']} (₹{low_item['selling_price']})
"""
        chart = px.sunburst(
            df, path=['category', 'market'], values='selling_price',
            title="🌐 RetailMind Catalog Hierarchy"
        )
        return ans, df[['product_name', 'category', 'market', 'selling_price', 'stock']].head(10), chart


# =====================================================
# TABS INTERFACE
# =====================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "💬 Conversational AI Chat",
    "🔎 Smart Product Finder",
    "📈 Profit & Market Analytics",
    "🚨 Low Stock & Reorder Alerts"
])

# ── TAB 1: CHAT ──────────────────────────────────────
with tab1:
    st.subheader("💬 Chat with RetailMind AI Engine")
    st.caption("Ask in English or Hinglish: 'sugar ka rate Malegaon mein', 'low stock alert', 'high margin products'")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant",
             "content": "👋 **Namaste! Main RetailMind AI hoon.**\n\nMujhse poochh sakte hain:\n- *'Sugar ka rate Malegaon mein'*\n- *'Kolam chawal Nashik mein kitne ka hai?'*\n- *'Low stock alert'* ya *'High profit items'*"}
        ]

    # Display history
    for msg in st.session_state.messages:
        with st.chat_message("user" if msg["role"] == "user" else "assistant"):
            st.markdown(msg["content"], unsafe_allow_html=True)

    # Quick action buttons
    st.write("")
    st.caption("⚡ **Quick Queries:**")
    qb1, qb2, qb3, qb4, qb5 = st.columns(5)
    quick_query = None
    with qb1:
        if st.button("🍚 Chawal Nashik", use_container_width=True, key="qb_chawal"): quick_query = "chawal ka rate Nashik mein"
    with qb2:
        if st.button("🍬 Sugar Malegaon", use_container_width=True, key="qb_sugar"): quick_query = "sugar rate Malegaon mein"
    with qb3:
        if st.button("🚨 Low Stock", use_container_width=True, key="qb_lowstock"): quick_query = "low stock alert"
    with qb4:
        if st.button("💰 High Margin", use_container_width=True, key="qb_margin"): quick_query = "high margin products"
    with qb5:
        if st.button("💸 Sasta Items", use_container_width=True, key="qb_sasta"): quick_query = "cheapest items"

    # Chat input
    user_input = st.chat_input("Ask RetailMind AI (e.g., 'sugar rate Malegaon mein')...")
    if quick_query:
        user_input = quick_query

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.spinner("🤖 RetailMind AI is analyzing market intelligence..."):
            ans, result_df, chart = process_ai_query(user_input, df)

        st.session_state.messages.append({"role": "assistant", "content": ans})
        with st.chat_message("assistant"):
            st.markdown(ans, unsafe_allow_html=True)
            if chart:
                st.plotly_chart(chart, use_container_width=True)
            if result_df is not None and not result_df.empty:
                st.dataframe(result_df, use_container_width=True, hide_index=True)

        if st.button("🗑️ Clear Chat History", key="clear_chat_btn"):
            st.session_state.messages = []
            st.rerun()

# ── TAB 2: SMART PRODUCT FINDER ──────────────────────
with tab2:
    st.subheader("🔎 Smart Product Finder")
    st.caption("Filter products by market, category, price range, and search keyword.")

    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        sel_market = st.selectbox("🏪 Select Market", ["All Markets"] + sorted(df['market'].unique().tolist()))
    with col_f2:
        sel_cat = st.selectbox("📂 Select Category", ["All Categories"] + sorted(df['category'].unique().tolist()))
    with col_f3:
        search_term = st.text_input("🔍 Search Product Name", placeholder="e.g. Sugar, Rice, Atta...")

    price_min, price_max = float(df['selling_price'].min()), float(df['selling_price'].max())
    price_range = st.slider("💰 Price Range (₹)", price_min, price_max, (price_min, price_max))

    filtered = df.copy()
    if sel_market != "All Markets":
        filtered = filtered[filtered['market'] == sel_market]
    if sel_cat != "All Categories":
        filtered = filtered[filtered['category'] == sel_cat]
    if search_term:
        filtered = filtered[filtered['product_name'].str.contains(search_term, case=False, na=False)]
    filtered = filtered[(filtered['selling_price'] >= price_range[0]) & (filtered['selling_price'] <= price_range[1])]

    st.write("")
    r1, r2, r3 = st.columns(3)
    r1.metric("🔢 Results Found", len(filtered))
    r2.metric("💰 Avg Price", f"₹{filtered['selling_price'].mean():.2f}" if not filtered.empty else "—")
    r3.metric("📦 Total Stock", f"{filtered['stock'].sum():,}" if not filtered.empty else "—")

    st.write("")
    if not filtered.empty:
        st.dataframe(
            filtered[['product_name', 'brand', 'category', 'market', 'selling_price', 'purchase_price', 'profit_margin', 'stock', 'unit', 'supplier']].sort_values('selling_price'),
            use_container_width=True, hide_index=True
        )
        csv = filtered.to_csv(index=False).encode('utf-8')
        st.download_button("⬇ Download Results CSV", csv, "FilteredProducts.csv", "text/csv")
    else:
        st.info("No products match your filters. Try adjusting the criteria.")

# ── TAB 3: ANALYTICS ─────────────────────────────────
with tab3:
    st.subheader("📈 Profit & Market Analytics")

    ana1, ana2 = st.columns(2)
    with ana1:
        margin_chart = px.bar(
            df.sort_values('profit_margin', ascending=False).head(12),
            x='product_name', y='profit_margin', color='margin_pct',
            title="🔥 Top 12 Products by Profit Margin (₹)",
            labels={'profit_margin': 'Profit (₹)', 'margin_pct': 'Margin %'},
            color_continuous_scale='Greens'
        )
        margin_chart.update_layout(xaxis_tickangle=-30, paper_bgcolor="#FFFFFF")
        st.plotly_chart(margin_chart, use_container_width=True)

    with ana2:
        mkt_avg = df.groupby('market').agg(
            AvgPrice=('selling_price', 'mean'),
            AvgMargin=('profit_margin', 'mean'),
            Products=('id', 'count')
        ).reset_index()
        mkt_chart = px.scatter(
            mkt_avg, x='AvgPrice', y='AvgMargin', size='Products',
            color='market', title="🏪 Market Performance Matrix",
            labels={'AvgPrice': 'Avg Selling Price (₹)', 'AvgMargin': 'Avg Profit Margin (₹)'},
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        mkt_chart.update_layout(paper_bgcolor="#FFFFFF")
        st.plotly_chart(mkt_chart, use_container_width=True)

    st.write("")
    cat_perf = df.groupby('category').agg(
        AvgPrice=('selling_price', 'mean'),
        AvgMargin=('profit_margin', 'mean'),
        TotalStock=('stock', 'sum'),
        Products=('id', 'count')
    ).reset_index().sort_values('AvgMargin', ascending=False)

    cat_chart = px.bar(
        cat_perf.head(15), x='category', y=['AvgPrice', 'AvgMargin'],
        barmode='group', title="📊 Category: Avg Price vs Avg Margin (₹)",
        color_discrete_map={'AvgPrice': '#2563EB', 'AvgMargin': '#10B981'}
    )
    cat_chart.update_layout(xaxis_tickangle=-30, paper_bgcolor="#FFFFFF")
    st.plotly_chart(cat_chart, use_container_width=True)

# ── TAB 4: LOW STOCK ALERTS ──────────────────────────
with tab4:
    st.subheader("🚨 Low Stock & Reorder Alerts")

    low_df = df[df['stock'] <= df['min_stock']].sort_values('stock')
    healthy_df = df[df['stock'] > df['min_stock']]

    al1, al2, al3, al4 = st.columns(4)
    al1.metric("🔴 Critical Items", len(low_df[low_df['stock'] == 0]), delta="Out of Stock")
    al2.metric("🟡 Low Stock Items", len(low_df), delta_color="inverse", delta=f"{len(low_df)} Need Reorder")
    al3.metric("🟢 Healthy Stock", len(healthy_df))
    al4.metric("📦 Total Products", len(df))

    st.write("")
    if low_df.empty:
        st.success("✅ Sabhi products ka stock healthy hai! Koi reorder required nahi.")
    else:
        st.error(f"🚨 **{len(low_df)} products** low stock limit pe hain — immediate reorder karein!")
        alert_chart = px.bar(
            low_df.head(15), x='product_name', y='stock', color='stock',
            title="⚠️ Low Stock Items (Current vs Min Stock Level)",
            color_continuous_scale='Reds_r',
            labels={'stock': 'Current Stock', 'product_name': 'Product'}
        )
        alert_chart.update_layout(xaxis_tickangle=-30, paper_bgcolor="#FFFFFF")
        st.plotly_chart(alert_chart, use_container_width=True)
        st.dataframe(
            low_df[['product_name', 'category', 'stock', 'min_stock', 'supplier', 'market']],
            use_container_width=True, hide_index=True
        )
        reorder_csv = low_df.to_csv(index=False).encode('utf-8')
        st.download_button("⬇ Download Reorder List CSV", reorder_csv, "ReorderList.csv", "text/csv", use_container_width=True)
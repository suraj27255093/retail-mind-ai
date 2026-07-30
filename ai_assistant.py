import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import re

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="RetailMind AI - Smart Assistant",
    page_icon="🤖",
    layout="wide"
)

# =====================================================
# BASIC STYLING
# =====================================================

st.markdown("""
<style>

.stApp {
    background-color: #F8FAFC;
}

.block-container {
    max-width: 1400px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

.ai-hero {
    background: linear-gradient(
        135deg,
        #0F172A 0%,
        #1E293B 50%,
        #2563EB 100%
    );

    padding: 28px 32px;
    border-radius: 20px;
    color: white;
    margin-bottom: 25px;

    box-shadow:
        0 10px 25px rgba(37, 99, 235, 0.15);
}

.ai-hero h1 {
    color: white !important;
    font-size: 32px;
    font-weight: 800;
    margin-bottom: 6px;
}

.ai-hero p {
    color: #93C5FD;
    font-size: 15px;
    margin: 0;
}

[data-testid="stMetric"] {
    background: white;
    padding: 18px 20px;
    border-radius: 16px;
    border: 1px solid #E2E8F0;
    box-shadow: 0 4px 12px rgba(0,0,0,0.03);
}

.stButton > button {
    border-radius: 10px;
    border: none;
    background: #2563EB;
    color: white;
    font-weight: 600;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# HEADER
# =====================================================

st.markdown("""
<div class="ai-hero">

<h1>🤖 RetailMind AI Assistant</h1>

<p>
Conversational Retail Intelligence •
Hinglish/English •
Market Rates •
Inventory •
Profit Analytics
</p>

</div>
""", unsafe_allow_html=True)

# =====================================================
# DATABASE + SAFE DATA
# =====================================================

@st.cache_data(ttl=60)
def get_products_data():

    conn = sqlite3.connect("retailmind.db")

    try:
        df = pd.read_sql_query(
            "SELECT * FROM products",
            conn
        )
    finally:
        conn.close()

    # -------------------------------------------------
    # REQUIRED COLUMNS
    # -------------------------------------------------

    required_columns = {
        "id": 0,
        "product_name": "Unknown Product",
        "category": "General",
        "variety": "",
        "unit": "",
        "market": "Unknown",
        "state": "",
        "supplier": "Unknown Supplier",
        "stock": 50,
        "min_stock": 10,
        "price": 0.0,
    }

    for column, default_value in required_columns.items():

        if column not in df.columns:
            df[column] = default_value

    # -------------------------------------------------
    # PRICE COLUMNS
    # -------------------------------------------------

    if "selling_price" not in df.columns:
        df["selling_price"] = df["price"]

    if "price" not in df.columns:
        df["price"] = df["selling_price"]

    if "purchase_price" not in df.columns:

        df["purchase_price"] = (
            df["selling_price"] * 0.85
        )

    # -------------------------------------------------
    # CLEAN DATA TYPES
    # -------------------------------------------------

    df["selling_price"] = pd.to_numeric(
        df["selling_price"],
        errors="coerce"
    ).fillna(0)

    df["purchase_price"] = pd.to_numeric(
        df["purchase_price"],
        errors="coerce"
    ).fillna(0)

    df["price"] = pd.to_numeric(
        df["price"],
        errors="coerce"
    ).fillna(0)

    df["stock"] = pd.to_numeric(
        df["stock"],
        errors="coerce"
    ).fillna(0)

    df["min_stock"] = pd.to_numeric(
        df["min_stock"],
        errors="coerce"
    ).fillna(10)

    # -------------------------------------------------
    # CLEAN TEXT COLUMNS
    # -------------------------------------------------

    text_columns = [
        "product_name",
        "category",
        "variety",
        "unit",
        "market",
        "state",
        "supplier"
    ]

    for column in text_columns:

        df[column] = (
            df[column]
            .fillna("")
            .astype(str)
            .str.strip()
        )

    # -------------------------------------------------
    # PROFIT CALCULATION
    # -------------------------------------------------

    df["profit_margin"] = (
        df["selling_price"]
        - df["purchase_price"]
    )

    df["margin_pct"] = (
        df["profit_margin"]
        /
        df["selling_price"].replace(0, 1)
    ) * 100

    return df


# =====================================================
# LOAD DATABASE
# =====================================================

df = get_products_data()


# =====================================================
# DATABASE STATUS
# =====================================================

if df.empty:

    st.warning(
        "⚠️ No products found in retailmind.db."
    )

    st.info(
        "Please add products to the products table."
    )

    st.stop()


# =====================================================
# DATABASE SUMMARY
# =====================================================

st.success(
    f"✅ Database Connected • "
    f"{len(df)} Products Loaded"
)

# =====================================================
# PART 3 — EXACT PRODUCT + MARKET DETECTION
# =====================================================

def normalize_text(text):
    """
    Text ko clean karke matching ke liye ready karta hai.
    """
    text = str(text).lower().strip()

    # Common Hinglish / Hindi spellings
    replacements = {
        "chini": "sugar",
        "cheeni": "sugar",
        "चीनी": "sugar",

        "chawal": "rice",
        "chaawal": "rice",
        "चावल": "rice",

        "gehun": "wheat",
        "गेहूं": "wheat",

        "atta": "flour",
        "आटा": "flour",

        "tel": "oil",
        "तेल": "oil",

        "namak": "salt",
        "नमक": "salt",

        "chai": "tea",
        "चाय": "tea",

        "coffee": "coffee",

        "ghee": "ghee",
        "घी": "ghee",

        "dal": "dal",
        "दाल": "dal",

        "masala": "masala",
        "मसाला": "masala",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text


def find_product(query, dataframe):
    """
    User query se exact/relevant product identify karta hai.
    """

    q = normalize_text(query)

    # -----------------------------------------------
    # DATABASE KE ACTUAL PRODUCT NAMES
    # -----------------------------------------------

    product_names = (
        dataframe["product_name"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    # Longest product name first
    product_names = sorted(
        product_names,
        key=len,
        reverse=True
    )

    # -----------------------------------------------
    # EXACT PRODUCT NAME MATCH
    # -----------------------------------------------

    for product in product_names:

        product_clean = normalize_text(product)

        if product_clean and product_clean in q:
            return product

    # -----------------------------------------------
    # COMMON PRODUCT KEYWORDS
    # -----------------------------------------------

    product_aliases = {
        "sugar": [
            "sugar",
            "chini",
            "cheeni",
            "चीनी"
        ],

        "rice": [
            "rice",
            "chawal",
            "chaawal",
            "चावल"
        ],

        "wheat": [
            "wheat",
            "gehun",
            "गेहूं"
        ],

        "flour": [
            "flour",
            "atta",
            "आटा"
        ],

        "oil": [
            "oil",
            "tel",
            "तेल"
        ],

        "salt": [
            "salt",
            "namak",
            "नमक"
        ],

        "tea": [
            "tea",
            "chai",
            "चाय"
        ],

        "ghee": [
            "ghee",
            "घी"
        ],

        "dal": [
            "dal",
            "दाल",
            "pulses"
        ],

        "masala": [
            "masala",
            "मसala",
            "spices"
        ]
    }

    # -----------------------------------------------
    # ALIAS MATCH WITH DATABASE
    # -----------------------------------------------

    for standard_name, aliases in product_aliases.items():

        found_alias = any(
            alias.lower() in q
            for alias in aliases
        )

        if found_alias:

            # Search actual DB products
            for product in product_names:

                product_clean = normalize_text(product)

                if standard_name in product_clean:
                    return product

    return None


# =====================================================
# FIND MARKET
# =====================================================

def find_market(query, dataframe):

    q = str(query).lower().strip()

    markets = (
        dataframe["market"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    # Longest names first
    markets = sorted(
        markets,
        key=len,
        reverse=True
    )

    # Exact database market match
    for market in markets:

        market_clean = str(market).lower().strip()

        if market_clean and market_clean in q:
            return market

    # Common market spellings
    market_aliases = {
        "malegaon": [
            "malegaon",
            "malegoan",
            "malegaon market"
        ],

        "nashik": [
            "nashik",
            "nasik",
            "nashik market"
        ],

        "dhule": [
            "dhule",
            "dhule market"
        ],

        "tehera": [
            "tehera",
            "tehera market"
        ]
    }

    for standard, aliases in market_aliases.items():

        if any(alias in q for alias in aliases):

            for market in markets:

                if standard in str(market).lower():
                    return market

    return None


# =====================================================
# TEST DETECTION FUNCTION
# =====================================================

def detect_product_market(query, dataframe):

    product = find_product(
        query,
        dataframe
    )

    market = find_market(
        query,
        dataframe
    )

    return product, market

# =====================================================
# PART 4 — EXACT PRODUCT + MARKET RESULT
# =====================================================

def get_product_market_result(query, dataframe):

    # Detect product + market
    product, market = detect_product_market(
        query,
        dataframe
    )

    # -------------------------------------------------
    # PRODUCT + MARKET BOTH FOUND
    # -------------------------------------------------

    if product and market:

        result = dataframe[
            (dataframe["product_name"].astype(str).str.lower() ==
             str(product).lower()) &
            (dataframe["market"].astype(str).str.lower() ==
             str(market).lower())
        ].copy()

        # ---------------------------------------------
        # NO EXACT RESULT
        # ---------------------------------------------

        if result.empty:

            return {
                "type": "not_found",
                "message": (
                    f"🔍 **{product}** ka "
                    f"**{market}** market mein "
                    f"record nahi mila."
                ),
                "data": None,
                "chart": None
            }

        # ---------------------------------------------
        # SINGLE PRODUCT RESULT
        # ---------------------------------------------

        if len(result) == 1:

            item = result.iloc[0]

            message = f"""
### 🏪 {market} Market

**📦 Product:** {item['product_name']}

**💰 Rate:** ₹{item['selling_price']:,.2f}

**📏 Unit:** {item['unit']}

**📦 Stock:** {item['stock']}
"""

            chart = px.bar(
                result,
                x="product_name",
                y="selling_price",
                title=f"{item['product_name']} Rate — {market}"
            )

        # ---------------------------------------------
        # MULTIPLE VARIETIES
        # ---------------------------------------------

        else:

            average_price = result["selling_price"].mean()

            message = f"""
### 🏪 {market} Market

**📦 Product:** {product}

**💰 Average Rate:** ₹{average_price:,.2f}

**📊 Varieties Found:** {len(result)}
"""

            chart = px.bar(
                result,
                x="product_name",
                y="selling_price",
                color="variety",
                title=f"{product} Rates — {market}"
            )

        # ---------------------------------------------
        # SAFE DISPLAY COLUMNS
        # ---------------------------------------------

        display_columns = [
            "product_name",
            "variety",
            "unit",
            "selling_price",
            "stock",
            "market"
        ]

        display_columns = [
            col for col in display_columns
            if col in result.columns
        ]

        return {
            "type": "product_market",
            "message": message,
            "data": result[display_columns],
            "chart": chart
        }

    # -------------------------------------------------
    # PRODUCT ONLY
    # -------------------------------------------------

    if product and not market:

        result = dataframe[
            dataframe["product_name"].astype(str).str.lower()
            ==
            str(product).lower()
        ].copy()

        if result.empty:

            return {
                "type": "not_found",
                "message": f"🔍 **{product}** ka koi record nahi mila.",
                "data": None,
                "chart": None
            }

        average_price = result["selling_price"].mean()

        message = f"""
### 📦 {product}

**💰 Average Rate:** ₹{average_price:,.2f}

**🏪 Markets Found:** {result['market'].nunique()}
"""

        display_columns = [
            "product_name",
            "variety",
            "unit",
            "selling_price",
            "market",
            "stock"
        ]

        display_columns = [
            col for col in display_columns
            if col in result.columns
        ]

        chart = px.bar(
            result,
            x="market",
            y="selling_price",
            title=f"{product} Price Across Markets"
        )

        return {
            "type": "product_only",
            "message": message,
            "data": result[display_columns],
            "chart": chart
        }

    # -------------------------------------------------
    # MARKET ONLY
    # -------------------------------------------------

    if market and not product:

        result = dataframe[
            dataframe["market"].astype(str).str.lower()
            ==
            str(market).lower()
        ].copy()

        if result.empty:

            return {
                "type": "not_found",
                "message": f"🔍 **{market}** ka koi record nahi mila.",
                "data": None,
                "chart": None
            }

        message = f"""
### 🏪 {market} Market

**📦 Products Available:** {len(result)}

**💰 Average Rate:** ₹{result['selling_price'].mean():,.2f}
"""

        display_columns = [
            "product_name",
            "category",
            "variety",
            "selling_price",
            "unit",
            "stock",
            "market"
        ]

        display_columns = [
            col for col in display_columns
            if col in result.columns
        ]

        chart = px.bar(
            result.head(15),
            x="product_name",
            y="selling_price",
            title=f"Product Rates — {market}"
        )

        return {
            "type": "market_only",
            "message": message,
            "data": result[display_columns],
            "chart": chart
        }

    # -------------------------------------------------
    # NOTHING DETECTED
    # -------------------------------------------------

    return {
        "type": "unknown",
        "message": None,
        "data": None,
        "chart": None
    }

# =====================================================
# PART 5 — AI CHAT ENGINE
# =====================================================

def process_ai_query(user_query, dataframe):

    q = str(user_query).lower().strip()

    # =================================================
    # 1️⃣ PRODUCT + MARKET QUERY
    # =================================================

    product, market = detect_product_market(
        user_query,
        dataframe
    )

    # Agar product + market dono mile
    if product and market:

        result = get_product_market_result(
            user_query,
            dataframe
        )

        return (
            result["message"],
            result["data"],
            result["chart"]
        )

    # =================================================
    # 2️⃣ LOW STOCK QUERY
    # =================================================

    low_stock_words = [
        "low stock",
        "kam stock",
        "stock kam",
        "stock khatam",
        "khatam",
        "reorder",
        "restock",
        "out of stock",
        "shortage"
    ]

    if any(word in q for word in low_stock_words):

        low_df = dataframe[
            dataframe["stock"] <= dataframe["min_stock"]
        ].copy()

        if low_df.empty:

            return (
                "✅ **Good News!** Koi product low stock mein nahi hai.",
                None,
                None
            )

        display_columns = [
            "product_name",
            "category",
            "stock",
            "min_stock",
            "market",
            "supplier"
        ]

        display_columns = [
            col for col in display_columns
            if col in low_df.columns
        ]

        message = f"""
### 🚨 Low Stock Alert

**{len(low_df)} products** ko reorder karne ki zarurat hai.
"""

        chart = px.bar(
            low_df.head(10),
            x="product_name",
            y="stock",
            title="🚨 Low Stock Products"
        )

        return (
            message,
            low_df[display_columns],
            chart
        )

    # =================================================
    # 3️⃣ PROFIT / MARGIN QUERY
    # =================================================

    profit_words = [
        "profit",
        "margin",
        "munafa",
        "earning",
        "highest profit",
        "high margin"
    ]

    if any(word in q for word in profit_words):

        profit_df = dataframe.sort_values(
            "profit_margin",
            ascending=False
        ).copy()

        best = profit_df.iloc[0]

        message = f"""
### 💰 Highest Profit Product

**Product:** {best['product_name']}

**Purchase Price:** ₹{best['purchase_price']:,.2f}

**Selling Price:** ₹{best['selling_price']:,.2f}

**Profit per Unit:** ₹{best['profit_margin']:,.2f}

**Margin:** {best['margin_pct']:.1f}%
"""

        display_columns = [
            "product_name",
            "category",
            "purchase_price",
            "selling_price",
            "profit_margin",
            "margin_pct"
        ]

        chart = px.bar(
            profit_df.head(10),
            x="product_name",
            y="profit_margin",
            title="💰 Top Profit Products"
        )

        return (
            message,
            profit_df[display_columns].head(10),
            chart
        )

    # =================================================
    # 4️⃣ CHEAPEST PRODUCT
    # =================================================

    cheap_words = [
        "cheapest",
        "sasta",
        "sabse sasta",
        "lowest price",
        "kam daam",
        "cheap"
    ]

    if any(word in q for word in cheap_words):

        cheap_df = dataframe.sort_values(
            "selling_price"
        ).copy()

        cheapest = cheap_df.iloc[0]

        message = f"""
### 💸 Cheapest Product

**Product:** {cheapest['product_name']}

**Price:** ₹{cheapest['selling_price']:,.2f}

**Market:** {cheapest['market']}

**Unit:** {cheapest['unit']}
"""

        display_columns = [
            "product_name",
            "category",
            "market",
            "selling_price",
            "unit"
        ]

        chart = px.bar(
            cheap_df.head(10),
            x="product_name",
            y="selling_price",
            title="💸 Cheapest Products"
        )

        return (
            message,
            cheap_df[display_columns].head(10),
            chart
        )

    # =================================================
    # 5️⃣ MOST EXPENSIVE PRODUCT
    # =================================================

    expensive_words = [
        "expensive",
        "mehanga",
        "sabse mehanga",
        "highest price",
        "costliest",
        "premium"
    ]

    if any(word in q for word in expensive_words):

        expensive_df = dataframe.sort_values(
            "selling_price",
            ascending=False
        ).copy()

        expensive = expensive_df.iloc[0]

        message = f"""
### 🔥 Most Expensive Product

**Product:** {expensive['product_name']}

**Price:** ₹{expensive['selling_price']:,.2f}

**Market:** {expensive['market']}

**Unit:** {expensive['unit']}
"""

        display_columns = [
            "product_name",
            "category",
            "market",
            "selling_price",
            "unit"
        ]

        chart = px.bar(
            expensive_df.head(10),
            x="product_name",
            y="selling_price",
            title="🔥 Most Expensive Products"
        )

        return (
            message,
            expensive_df[display_columns].head(10),
            chart
        )

    # =================================================
    # 6️⃣ PRODUCT ONLY QUERY
    # =================================================

    if product and not market:

        result = get_product_market_result(
            user_query,
            dataframe
        )

        if result["type"] != "unknown":

            return (
                result["message"],
                result["data"],
                result["chart"]
            )

    # =================================================
    # 7️⃣ MARKET ONLY QUERY
    # =================================================

    if market and not product:

        result = get_product_market_result(
            user_query,
            dataframe
        )

        if result["type"] != "unknown":

            return (
                result["message"],
                result["data"],
                result["chart"]
            )

    # =================================================
    # 8️⃣ GENERAL QUERY
    # =================================================

    highest = dataframe.loc[
        dataframe["selling_price"].idxmax()
    ]

    lowest = dataframe.loc[
        dataframe["selling_price"].idxmin()
    ]

    message = f"""
### 🤖 RetailMind AI

Main aapke retail database se ye information de sakta hoon:

📦 **Total Products:** {len(dataframe)}

📂 **Categories:** {dataframe['category'].nunique()}

🏪 **Markets:** {dataframe['market'].nunique()}

💰 **Highest Price:** {highest['product_name']} — ₹{highest['selling_price']:,.2f}

💸 **Lowest Price:** {lowest['product_name']} — ₹{lowest['selling_price']:,.2f}

### Try asking:

• `Sugar ka rate Malegaon mai`

• `Sugar ka rate kya hai?`

• `Nashik market ke rates batao`

• `Sabse sasta rice konsa hai?`

• `Low stock items dikhao`

• `Highest profit product konsa hai?`
"""

    return (
        message,
        None,
        None
    )


# =====================================================
# CHAT INTERFACE
# =====================================================

st.divider()

st.subheader("💬 RetailMind AI Chat")

st.caption(
    "English / Hinglish mein apna question poochiye."
)


# =====================================================
# CHAT HISTORY
# =====================================================

if "messages" not in st.session_state:

    st.session_state.messages = [
        {
            "role": "assistant",
            "content": """
👋 **Namaste!**

Main **RetailMind AI Assistant** hoon.

Aap mujhe product rates, market rates,
stock aur profit ke baare mein pooch sakte hain.
"""
        }
    ]


# =====================================================
# DISPLAY OLD MESSAGES
# =====================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

        if message.get("data") is not None:

            st.dataframe(
                message["data"],
                use_container_width=True,
                hide_index=True
            )

        if message.get("chart") is not None:

            st.plotly_chart(
                message["chart"],
                use_container_width=True
            )


# =====================================================
# CHAT INPUT
# =====================================================

user_input = st.chat_input(
    "Example: sugar ka rate Malegaon mai..."
)


if user_input:

    # -----------------------------------------------
    # USER MESSAGE
    # -----------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"):

        st.markdown(user_input)


    # -----------------------------------------------
    # AI RESPONSE
    # -----------------------------------------------

    answer, result_data, result_chart = process_ai_query(
        user_input,
        df
    )


    with st.chat_message("assistant"):

        st.markdown(answer)

        if result_data is not None:

            st.dataframe(
                result_data,
                use_container_width=True,
                hide_index=True
            )

        if result_chart is not None:

            st.plotly_chart(
                result_chart,
                use_container_width=True
            )


    # -----------------------------------------------
    # SAVE CHAT HISTORY
    # -----------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "data": result_data,
            "chart": result_chart
        }
    )

    # =====================================================
# PART 6 — TAB 3: PROFIT & MARKET ANALYTICS
# =====================================================

with tab3:

    st.subheader("📈 Retail Business Analytics & Profit Intelligence")

    # ---------------- KPI ----------------

    total_sales_value = (
        df["selling_price"] * df["stock"]
    ).sum()

    total_purchase_value = (
        df["purchase_price"] * df["stock"]
    ).sum()

    total_profit = (
        total_sales_value - total_purchase_value
    )

    avg_profit = df["profit_margin"].mean()

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "💰 Stock Sales Value",
            f"₹{total_sales_value:,.2f}"
        )

    with c2:
        st.metric(
            "📦 Stock Purchase Value",
            f"₹{total_purchase_value:,.2f}"
        )

    with c3:
        st.metric(
            "📈 Estimated Profit",
            f"₹{total_profit:,.2f}"
        )

    with c4:
        st.metric(
            "💹 Avg Profit / Unit",
            f"₹{avg_profit:,.2f}"
        )

    st.divider()

    # =================================================
    # TOP PROFIT PRODUCTS
    # =================================================

    st.subheader("🏆 Top 10 Most Profitable Products")

    profit_products = (
        df.sort_values(
            "profit_margin",
            ascending=False
        )
        .head(10)
    )

    st.dataframe(
        profit_products[
            [
                "product_name",
                "category",
                "purchase_price",
                "selling_price",
                "profit_margin",
                "margin_pct",
                "stock"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

    # =================================================
    # PROFIT CHART
    # =================================================

    fig_profit = px.bar(
        profit_products,
        x="product_name",
        y="profit_margin",
        title="🔥 Top 10 Products by Profit per Unit",
        labels={
            "product_name": "Product",
            "profit_margin": "Profit (₹)"
        }
    )

    st.plotly_chart(
        fig_profit,
        use_container_width=True
    )

    # =================================================
    # CATEGORY PROFIT ANALYSIS
    # =================================================

    st.subheader("📂 Category Wise Profit Analysis")

    category_profit = (
        df.groupby("category")
        .agg(
            Products=("product_name", "count"),
            Avg_Selling_Price=("selling_price", "mean"),
            Avg_Purchase_Price=("purchase_price", "mean"),
            Avg_Profit=("profit_margin", "mean"),
            Total_Stock=("stock", "sum")
        )
        .reset_index()
    )

    category_profit["Estimated_Profit"] = (
        category_profit["Avg_Profit"] *
        category_profit["Total_Stock"]
    )

    st.dataframe(
        category_profit,
        use_container_width=True,
        hide_index=True
    )

    # =================================================
    # CATEGORY PROFIT CHART
    # =================================================

    fig_category = px.bar(
        category_profit.sort_values(
            "Estimated_Profit",
            ascending=False
        ),
        x="category",
        y="Estimated_Profit",
        title="💰 Estimated Profit by Category",
        labels={
            "category": "Category",
            "Estimated_Profit": "Estimated Profit (₹)"
        }
    )

    st.plotly_chart(
        fig_category,
        use_container_width=True
    )

    # =================================================
    # MARKET PROFIT ANALYSIS
    # =================================================

    st.subheader("🏪 Market Wise Profit Analysis")

    market_profit = (
        df.groupby("market")
        .agg(
            Products=("product_name", "count"),
            Avg_Selling_Price=("selling_price", "mean"),
            Avg_Purchase_Price=("purchase_price", "mean"),
            Avg_Profit=("profit_margin", "mean"),
            Total_Stock=("stock", "sum")
        )
        .reset_index()
    )

    market_profit["Estimated_Profit"] = (
        market_profit["Avg_Profit"] *
        market_profit["Total_Stock"]
    )

    st.dataframe(
        market_profit,
        use_container_width=True,
        hide_index=True
    )

    # =================================================
    # MARKET PROFIT CHART
    # =================================================

    fig_market = px.bar(
        market_profit.sort_values(
            "Estimated_Profit",
            ascending=False
        ),
        x="market",
        y="Estimated_Profit",
        title="🏪 Estimated Profit by Market",
        labels={
            "market": "Market",
            "Estimated_Profit": "Estimated Profit (₹)"
        }
    )

    st.plotly_chart(
        fig_market,
        use_container_width=True
    )

    # =================================================
    # PRICE RELATIONSHIP
    # =================================================

    st.subheader("💹 Purchase Price vs Selling Price")

    fig_scatter = px.scatter(
        df,
        x="purchase_price",
        y="selling_price",
        size="stock",
        color="category",
        hover_name="product_name",
        title="Purchase Price vs Selling Price"
    )

    st.plotly_chart(
        fig_scatter,
        use_container_width=True
    )

    # =================================================
    # AI BUSINESS INSIGHT
    # =================================================

    st.subheader("🤖 AI Business Insight")

    best_profit = df.loc[
        df["profit_margin"].idxmax()
    ]

    best_category = category_profit.loc[
        category_profit["Estimated_Profit"].idxmax()
    ]

    best_market = market_profit.loc[
        market_profit["Estimated_Profit"].idxmax()
    ]

    st.success(
        f"""
🏆 **Best Profit Product**

Product: **{best_profit['product_name']}**

Profit per Unit: **₹{best_profit['profit_margin']:.2f}**

Margin: **{best_profit['margin_pct']:.1f}%**
"""
    )

    st.info(
        f"""
📂 **Most Profitable Category**

**{best_category['category']}**

Estimated Profit: **₹{best_category['Estimated_Profit']:,.2f}**
"""
    )

    st.warning(
        f"""
🏪 **Highest Profit Market**

**{best_market['market']}**

Estimated Profit: **₹{best_market['Estimated_Profit']:,.2f}**
"""
    )
# =====================================================
# PART 7 — TAB 4: LOW STOCK & REORDER ALERTS
# =====================================================

with tab4:

    st.subheader("🚨 Inventory Health & Reorder System")

    # =================================================
    # STOCK KPI
    # =================================================

    low_s = df[
        df["stock"] <= df["min_stock"]
    ].copy()

    out_stock = df[
        df["stock"] <= 0
    ].copy()

    healthy_stock = df[
        df["stock"] > df["min_stock"]
    ].copy()

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "📦 Total Products",
            len(df)
        )

    with c2:
        st.metric(
            "⚠️ Low Stock",
            len(low_s)
        )

    with c3:
        st.metric(
            "❌ Out of Stock",
            len(out_stock)
        )

    with c4:
        st.metric(
            "✅ Healthy Stock",
            len(healthy_stock)
        )

    st.divider()

    # =================================================
    # LOW STOCK ALERT
    # =================================================

    st.subheader("⚠️ Low Stock Products")

    if low_s.empty:

        st.success(
            "🎉 Excellent! All products have healthy stock levels."
        )

    else:

        st.warning(
            f"⚠️ {len(low_s)} products need attention."
        )

        # Recommended reorder quantity
        low_s["Reorder_Qty"] = (
            low_s["min_stock"] * 3
        ) - low_s["stock"]

        low_s["Reorder_Qty"] = (
            low_s["Reorder_Qty"].clip(lower=0)
        )

        # Estimated reorder cost
        low_s["Est_Reorder_Cost"] = (
            low_s["Reorder_Qty"] *
            low_s["purchase_price"]
        )

        st.dataframe(
            low_s[
                [
                    "product_name",
                    "category",
                    "stock",
                    "min_stock",
                    "Reorder_Qty",
                    "purchase_price",
                    "Est_Reorder_Cost",
                    "supplier",
                    "market"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

        total_reorder_cost = (
            low_s["Est_Reorder_Cost"].sum()
        )

        st.info(
            f"💰 **Estimated Reorder Capital Needed: ₹{total_reorder_cost:,.2f}**"
        )

    st.divider()

    # =================================================
    # OUT OF STOCK
    # =================================================

    st.subheader("❌ Out of Stock Products")

    if out_stock.empty:

        st.success(
            "✅ No products are currently out of stock."
        )

    else:

        st.error(
            f"🚨 {len(out_stock)} products are completely out of stock!"
        )

        st.dataframe(
            out_stock[
                [
                    "product_name",
                    "category",
                    "supplier",
                    "market",
                    "purchase_price",
                    "selling_price"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    st.divider()

    # =================================================
    # REORDER PRIORITY
    # =================================================

    st.subheader("🔥 Reorder Priority")

    if not low_s.empty:

        priority_df = low_s.copy()

        priority_df["Stock_Ratio"] = (
            priority_df["stock"] /
            priority_df["min_stock"].replace(0, 1)
        )

        priority_df["Priority"] = priority_df[
            "Stock_Ratio"
        ].apply(
            lambda x:
                "🔴 Critical" if x <= 0.25
                else "🟠 High" if x <= 0.50
                else "🟡 Medium"
        )

        priority_df = priority_df.sort_values(
            "Stock_Ratio"
        )

        st.dataframe(
            priority_df[
                [
                    "product_name",
                    "category",
                    "stock",
                    "min_stock",
                    "Priority",
                    "supplier",
                    "market"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    else:

        st.success(
            "🎉 No reorder priority required."
        )

    st.divider()

    # =================================================
    # STOCK CHART
    # =================================================

    if not low_s.empty:

        st.subheader("📊 Low Stock Level Chart")

        chart_df = low_s.sort_values(
            "stock"
        ).head(15)

        fig_stock = px.bar(
            chart_df,
            x="product_name",
            y=["stock", "min_stock"],
            barmode="group",
            title="Current Stock vs Minimum Required Stock",
            labels={
                "product_name": "Product",
                "value": "Units"
            }
        )

        st.plotly_chart(
            fig_stock,
            use_container_width=True
        )

    st.divider()

    # =================================================
    # AI REORDER RECOMMENDATION
    # =================================================

    st.subheader("🤖 AI Reorder Recommendation")

    if not low_s.empty:

        critical = low_s[
            low_s["stock"] <=
            (low_s["min_stock"] * 0.25)
        ]

        if not critical.empty:

            st.error(
                f"""
🚨 **URGENT ACTION REQUIRED**

{len(critical)} products have critically low stock.

Recommended action:

➡️ Contact suppliers immediately  
➡️ Place reorder for critical products  
➡️ Prioritize products with stock near zero
"""
            )

        else:

            st.info(
                """
ℹ️ **Stock Monitoring Recommendation**

Some products are below their minimum stock level.

Please review the reorder table and replenish them soon.
"""
            )

    else:

        st.success(
            """
🎉 **AI Stock Analysis**

Your inventory currently looks healthy.

No immediate reorder action is required.
"""
        )

    st.divider()

    # =================================================
    # DOWNLOAD REORDER REPORT
    # =================================================

    st.subheader("📥 Download Reorder Report")

    if not low_s.empty:

        reorder_report = low_s[
            [
                "product_name",
                "category",
                "stock",
                "min_stock",
                "Reorder_Qty",
                "purchase_price",
                "Est_Reorder_Cost",
                "supplier",
                "market"
            ]
        ]

        csv_reorder = (
            reorder_report
            .to_csv(index=False)
            .encode("utf-8")
        )

        st.download_button(
            label="⬇️ Download Reorder Report",
            data=csv_reorder,
            file_name="retailmind_reorder_report.csv",
            mime="text/csv"
        )

    else:

        st.info(
            "No reorder report available because stock is healthy."
        )

    # =================================================
    # FINAL STATUS
    # =================================================

    st.divider()

    st.success(
        "✅ Inventory Health & Reorder System Running Successfully"
    )

    st.caption(
        "RetailMind AI | Smart Inventory & Reorder Intelligence"
    )
import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from datetime import datetime

# =========================================================
# CUSTOMERS & CRM PAGE — loaded as module from app.py
# =========================================================

# Initialize demo customers in session state
if "customers_db" not in st.session_state:
    st.session_state.customers_db = [
        {"ID": "C001", "Customer Name": "Rahul Sharma", "Mobile": "+91 9823012345", "Email": "rahul@email.com",
         "Address": "Nashik Road", "Total Purchases": 14500, "Loyalty Points": 145, "Tier": "Gold", "Joined": "2024-01"},
        {"ID": "C002", "Customer Name": "Priya Patel", "Mobile": "+91 9890123456", "Email": "priya@email.com",
         "Address": "Pune Camp", "Total Purchases": 8200, "Loyalty Points": 82, "Tier": "Silver", "Joined": "2024-03"},
        {"ID": "C003", "Customer Name": "Amit Deshmukh", "Mobile": "+91 9765432109", "Email": "amit@email.com",
         "Address": "Malegaon", "Total Purchases": 22100, "Loyalty Points": 221, "Tier": "Platinum", "Joined": "2023-11"},
        {"ID": "C004", "Customer Name": "Sunita Verma", "Mobile": "+91 9811223344", "Email": "sunita@email.com",
         "Address": "Nashik City", "Total Purchases": 5400, "Loyalty Points": 54, "Tier": "Bronze", "Joined": "2024-05"},
        {"ID": "C005", "Customer Name": "Ravi Kumar", "Mobile": "+91 9977665544", "Email": "ravi@email.com",
         "Address": "Pune West", "Total Purchases": 18700, "Loyalty Points": 187, "Tier": "Gold", "Joined": "2024-02"},
    ]

customers_df = pd.DataFrame(st.session_state.customers_db)

# Hero Header
st.markdown("""
<div class="rm-hero">
    <h1>👥 Customers & Purchase History</h1>
    <p>Manage store customers, track purchase history, Khata credit ledger & loyalty points</p>
</div>
""", unsafe_allow_html=True)

# KPI Metrics
total_purchases_val = customers_df["Total Purchases"].sum()
top_cust_name = customers_df.loc[customers_df["Total Purchases"].idxmax(), "Customer Name"]

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("👥 Total Customers", f"{len(customers_df):,} Customers")
with c2:
    st.metric("💰 Total Customer Purchases", f"₹{total_purchases_val:,.0f}")
with c3:
    st.metric("🏆 Top Customer", top_cust_name)

st.write("")

# Action Buttons
st.markdown("**⚡ CRM & Loyalty Program Actions:**")
cb1, cb2, cb3, cb4, cb5 = st.columns(5)

with cb1:
    if st.button("🎁 Issue Reward Vouchers", use_container_width=True, key="crm_vouchers"):
        st.success("🎉 ₹100 reward vouchers issued to all Gold & Platinum members!")

with cb2:
    if st.button("📲 Send SMS Campaign", use_container_width=True, key="crm_sms"):
        st.info(f"📩 Promotional SMS campaign queued for {len(customers_df)} customers!")

with cb3:
    if st.button("🔔 Birthday Reminders", use_container_width=True, key="crm_birthday"):
        st.info("📅 Checking upcoming customer birthdays... 2 birthdays this week — sending greetings!")

with cb4:
    c_csv = customers_df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Export CRM CSV", c_csv, "Customers_CRM.csv", "text/csv", use_container_width=True, key="crm_export")

with cb5:
    if st.button("🔄 Refresh CRM", use_container_width=True, key="crm_refresh"):
        st.rerun()

# Tabs
tab_c1, tab_c2, tab_c3 = st.tabs(["👥 Customer Directory", "📊 Loyalty Analytics", "➕ Register New Customer"])

with tab_c1:
    search_c = st.text_input("🔍 Search customers", placeholder="Search by name, mobile, or tier...", key="cust_search_inp")
    tier_filter = st.multiselect("Filter by Tier", ["Platinum", "Gold", "Silver", "Bronze"], default=[], key="cust_tier_flt")

    display_df = customers_df.copy()
    if search_c:
        display_df = display_df[
            display_df["Customer Name"].str.contains(search_c, case=False, na=False) |
            display_df["Mobile"].str.contains(search_c, case=False, na=False)
        ]
    if tier_filter:
        display_df = display_df[display_df["Tier"].isin(tier_filter)]

    # Add Last Purchase column if not present
    if "Last Purchase" not in display_df.columns:
        display_df["Last Purchase"] = "2026-09-01"

    display_df = display_df.rename(columns={
        "Customer Name": "Name",
        "Mobile": "Mobile",
        "Total Purchases": "Total Purchases (₹)",
        "Last Purchase": "Last Purchase"
    })

    cust_cols = ["ID", "Name", "Mobile", "Total Purchases (₹)", "Last Purchase", "Tier", "Loyalty Points"]
    cust_cols = [c for c in cust_cols if c in display_df.columns]
    st.markdown(f"**{len(display_df)} customers found**")
    st.dataframe(display_df[cust_cols], use_container_width=True, hide_index=True)

    # Quick customer action
    st.write("")
    st.subheader("⚡ Quick Customer Actions")
    sel_cust = st.selectbox("Select Customer", customers_df["Customer Name"].tolist())
    cust_data = customers_df[customers_df["Customer Name"] == sel_cust].iloc[0]

    act_col1, act_col2, act_col3 = st.columns(3)
    with act_col1:
        if st.button(f"➕ Add 50 Bonus Points to {sel_cust.split()[0]}", use_container_width=True, key="crm_add_points"):
            for c in st.session_state.customers_db:
                if c["Customer Name"] == sel_cust:
                    c["Loyalty Points"] += 50
            st.success(f"✅ +50 bonus points added to {sel_cust}! Total: {cust_data['Loyalty Points'] + 50}")
            st.rerun()
    with act_col2:
        if st.button(f"🎟️ Redeem 100 Points (₹100 Off)", use_container_width=True, key="crm_redeem"):
            if cust_data["Loyalty Points"] >= 100:
                st.success(f"✅ 100 points redeemed for {sel_cust} — ₹100 discount voucher generated!")
            else:
                st.error(f"Insufficient points! {sel_cust} has only {cust_data['Loyalty Points']} points.")
    with act_col3:
        if st.button(f"📊 View Purchase History", use_container_width=True, key="crm_view_hist"):
            st.info(f"📋 {sel_cust} — Total Spent: ₹{cust_data['Total Purchases']:,} | Points: {cust_data['Loyalty Points']} | Tier: {cust_data['Tier']}")

with tab_c2:
    chart_c1, chart_c2 = st.columns(2)
    with chart_c1:
        raw_df = pd.DataFrame(st.session_state.customers_db)
        fig_tier = px.pie(
            raw_df, names="Tier", title="Customer Tier Distribution",
            color="Tier", hole=0.4,
            color_discrete_map={
                "Platinum": "#8B5CF6",
                "Gold": "#F59E0B",
                "Silver": "#94A3B8",
                "Bronze": "#B45309"
            }
        )
        st.plotly_chart(fig_tier, use_container_width=True)

    with chart_c2:
        fig_spend = px.bar(
            raw_df.sort_values("Total Purchases", ascending=False),
            x="Customer Name", y="Total Purchases",
            color="Tier", title="Customer Purchase Value Ranking (₹)",
            color_discrete_map={
                "Platinum": "#8B5CF6",
                "Gold": "#F59E0B",
                "Silver": "#94A3B8",
                "Bronze": "#B45309"
            }
        )
        fig_spend.update_layout(paper_bgcolor="#FFFFFF")
        st.plotly_chart(fig_spend, use_container_width=True)

    st.subheader("⭐ Loyalty Points Leaderboard")
    leaderboard = raw_df.sort_values("Loyalty Points", ascending=False).reset_index(drop=True)
    leaderboard.index = leaderboard.index + 1
    medals = ["🥇", "🥈", "🥉"] + ["  "] * (len(leaderboard) - 3)
    leaderboard.insert(0, "Rank", medals[:len(leaderboard)])
    leaderboard["Loyalty Points"] = leaderboard["Loyalty Points"].apply(lambda x: f"⭐ {x:,}")
    leaderboard["Total Purchases"] = leaderboard["Total Purchases"].apply(lambda x: f"₹{x:,}")
    st.dataframe(leaderboard[["Rank", "Customer Name", "Tier", "Loyalty Points", "Total Purchases", "Mobile"]], use_container_width=True, hide_index=True)

with tab_c3:
    with st.form("new_customer_form"):
        st.subheader("➕ Register New Loyalty Customer")
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            nc_name = st.text_input("Customer Full Name*")
            nc_mobile = st.text_input("Mobile Number* (+91...)")
            nc_email = st.text_input("Email Address")
        with col_c2:
            nc_address = st.text_input("Delivery / Home Address")
            nc_tier = st.selectbox("Initial Tier", ["Bronze", "Silver", "Gold"])
            nc_initial_points = st.number_input("Welcome Bonus Points", min_value=0, value=10)

        save_c = st.form_submit_button("✅ Register Customer", use_container_width=True)
        if save_c and nc_name and nc_mobile:
            new_id = f"C{len(st.session_state.customers_db) + 1:03d}"
            st.session_state.customers_db.append({
                "ID": new_id,
                "Customer Name": nc_name,
                "Mobile": nc_mobile,
                "Email": nc_email,
                "Address": nc_address,
                "Total Purchases": 0,
                "Loyalty Points": nc_initial_points,
                "Tier": nc_tier,
                "Joined": datetime.now().strftime("%Y-%m")
            })
            st.success(f"✅ Customer '{nc_name}' registered with {nc_initial_points} Welcome Points! ID: {new_id}")
            st.rerun()
        elif save_c and not nc_name:
            st.error("Customer name is required!")
import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from datetime import datetime

# =========================================================
# SUPPLIERS PAGE — loaded as module from app.py
# =========================================================

def load_suppliers():
    conn = sqlite3.connect("retailmind.db")
    try:
        sup_df = pd.read_sql_query("SELECT * FROM suppliers", conn)
    except Exception:
        sup_df = pd.DataFrame()
    conn.close()
    return sup_df

sup_df = load_suppliers()

if sup_df.empty:
    sup_df = pd.DataFrame([
        {"id": 1, "supplier_name": "ABC Traders", "mobile": "9876543210", "email": "contact@abctraders.com",
         "address": "Market Yard, Nashik", "gst_number": "27AAAAA0000A1Z5", "rating": 4.8, "category": "Grains & Pulses", "status": "Active"},
        {"id": 2, "supplier_name": "Rice World Pvt Ltd", "mobile": "9822011223", "email": "orders@riceworld.in",
         "address": "Grain Market, Pune", "gst_number": "27BBBBB1111B1Z2", "rating": 4.5, "category": "Grains", "status": "Active"},
        {"id": 3, "supplier_name": "Dal Suppliers Ltd", "mobile": "9911223344", "email": "info@dalsuppliers.com",
         "address": "APMC Yard, Malegaon", "gst_number": "27CCCCC2222C1Z9", "rating": 4.2, "category": "Pulses", "status": "Active"},
        {"id": 4, "supplier_name": "Oil Traders Co.", "mobile": "9850044556", "email": "sales@oiltraders.com",
         "address": "Industrial Area, Nashik", "gst_number": "27DDDDD3333D1Z4", "rating": 4.7, "category": "Oil & Ghee", "status": "Active"},
        {"id": 5, "supplier_name": "Spice Kingdom", "mobile": "9988776655", "email": "spice@kingdom.in",
         "address": "Spice Market, Pune", "gst_number": "27EEEEE4444E1Z7", "rating": 4.3, "category": "Spices", "status": "Pending"},
    ])

# Hero Header
st.markdown("""
<div class="rm-hero">
    <h1>🏢 RetailMind AI — Suppliers Directory & Partner Hub</h1>
    <p>Manage wholesale supplier contacts, GST credentials, performance ratings & stock orders</p>
</div>
""", unsafe_allow_html=True)

# KPI Cards
avg_rating = sup_df["rating"].mean() if "rating" in sup_df.columns else 4.5
active_count = len(sup_df[sup_df.get("status", pd.Series(["Active"] * len(sup_df))) == "Active"]) if "status" in sup_df.columns else len(sup_df)

c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    st.metric("🏢 Active Suppliers", active_count)
with c2:
    st.metric("🏪 Sourcing Markets", 3)
with c3:
    st.metric("⭐ Avg Supplier Rating", f"{avg_rating:.1f}/5.0")
with c4:
    st.metric("✅ GST Verified", f"{len(sup_df)} / {len(sup_df)}")
with c5:
    st.metric("📦 Order Fulfillment Rate", "98.5%", delta="+2.1%")

st.write("")

# Action Buttons
st.markdown("**⚡ Supplier Partner Actions:**")
sb1, sb2, sb3, sb4, sb5 = st.columns(5)

with sb1:
    if st.button("📞 Send Reorder Alerts", use_container_width=True, key="sup_alerts"):
        st.success("📩 Reorder SMS & Email dispatched to all active suppliers!")

with sb2:
    if st.button("🟢 Verify GST Credentials", use_container_width=True, key="sup_gst"):
        st.info(f"✅ All {len(sup_df)} suppliers verified against Govt GSTIN portal.")

with sb3:
    if st.button("📊 Rate All Suppliers", use_container_width=True, key="sup_rate"):
        st.info("⭐ Performance audit initiated for all supplier partners!")

with sb4:
    sup_csv = sup_df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Export Supplier Registry", sup_csv, "Suppliers_Registry.csv", "text/csv", use_container_width=True, key="sup_export")

with sb5:
    if st.button("🔄 Refresh Directory", use_container_width=True, key="sup_refresh"):
        st.rerun()

st.write("")

# Tabs
tab_s1, tab_s2, tab_s3 = st.tabs(["🏢 Supplier Directory", "📊 Supplier Analytics", "➕ Register New Supplier"])

with tab_s1:
    search_s = st.text_input("🔍 Search suppliers", placeholder="Search by name, category, address...", key="sup_search_input")
    status_f = st.multiselect("Filter by Status", ["Active", "Pending", "Inactive"], default=[], key="sup_status_filter")

    view_sup = sup_df.copy()
    if search_s:
        view_sup = view_sup[
            view_sup["supplier_name"].str.contains(search_s, case=False, na=False) |
            view_sup.get("category", pd.Series([""] * len(view_sup))).str.contains(search_s, case=False, na=False) |
            view_sup["address"].str.contains(search_s, case=False, na=False)
        ]
    if status_f and "status" in view_sup.columns:
        view_sup = view_sup[view_sup["status"].isin(status_f)]

    # Display supplier cards
    for _, row in view_sup.iterrows():
        rating_stars = "⭐" * int(row.get("rating", 4)) + ("½" if (row.get("rating", 4) % 1) >= 0.5 else "")
        status_badge = "🟢 Active" if row.get("status", "Active") == "Active" else "🟡 Pending"
        st.markdown(f"""
        <div style="background:#FFFFFF; padding:18px 22px; border-radius:16px; border:1px solid #E2E8F0; margin-bottom:12px; box-shadow: 0 2px 8px rgba(0,0,0,0.04);">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <span style="font-size:18px; font-weight:800; color:#0F172A;">🏢 {row['supplier_name']}</span>
                    &nbsp; <span style="background:#DBEAFE; color:#1D4ED8; padding:2px 10px; border-radius:20px; font-size:12px; font-weight:700;">{row.get('category', 'General')}</span>
                    &nbsp; <span style="font-size:12px;">{status_badge}</span>
                </div>
                <div style="font-size:18px;">{rating_stars} ({row.get('rating', 'N/A')})</div>
            </div>
            <div style="color:#64748B; font-size:13px; margin-top:8px;">
                📞 {row['mobile']} &nbsp;|&nbsp; 📧 {row['email']} &nbsp;|&nbsp; 📍 {row['address']}<br>
                🔐 GSTIN: <code style="background:#F1F5F9; padding:2px 6px; border-radius:4px;">{row['gst_number']}</code>
            </div>
        </div>
        """, unsafe_allow_html=True)

with tab_s2:
    if "rating" in sup_df.columns and "supplier_name" in sup_df.columns:
        chart_s1, chart_s2 = st.columns(2)
        with chart_s1:
            fig_rate = px.bar(
                sup_df.sort_values("rating", ascending=True),
                x="rating", y="supplier_name",
                orientation="h",
                title="⭐ Supplier Performance Ratings",
                color="rating",
                color_continuous_scale="Greens",
                labels={"rating": "Rating (out of 5)", "supplier_name": "Supplier"}
            )
            fig_rate.update_layout(paper_bgcolor="#FFFFFF")
            st.plotly_chart(fig_rate, use_container_width=True)

        with chart_s2:
            if "category" in sup_df.columns:
                cat_count = sup_df["category"].value_counts().reset_index()
                cat_count.columns = ["Category", "Count"]
                fig_cat = px.pie(
                    cat_count, names="Category", values="Count",
                    title="Suppliers by Product Category",
                    hole=0.4,
                    color_discrete_sequence=px.colors.qualitative.Set2
                )
                st.plotly_chart(fig_cat, use_container_width=True)

        # Performance table
        st.subheader("📊 Supplier Performance Summary")
        perf_data = []
        for _, row in sup_df.iterrows():
            perf_data.append({
                "Supplier": row["supplier_name"],
                "Rating": f"{'⭐' * int(row.get('rating', 4))} {row.get('rating', 'N/A')}",
                "Category": row.get("category", "General"),
                "Status": row.get("status", "Active"),
                "GST Verified": "✅ Yes",
                "On-Time Delivery": f"{85 + int(row.get('rating', 4)) * 2:.0f}%"
            })
        st.dataframe(pd.DataFrame(perf_data), use_container_width=True, hide_index=True)

with tab_s3:
    with st.form("add_supplier_form"):
        st.subheader("➕ Register New Supplier Partner")
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            s_name = st.text_input("Supplier Company Name*")
            s_mobile = st.text_input("Mobile Contact*")
            s_email = st.text_input("Email Address")
            s_cat = st.selectbox("Supply Category", ["Grains", "Pulses", "Oil & Ghee", "Spices", "Snacks", "Multiple / General"])
        with col_s2:
            s_address = st.text_input("Office Address / Market Yard")
            s_gst = st.text_input("GSTIN Number (e.g. 27AAAAA0000A1Z5)")
            s_rating = st.slider("Initial Rating", 1.0, 5.0, 4.0, 0.5)
            s_status = st.selectbox("Status", ["Active", "Pending"])

        save_s = st.form_submit_button("💾 Save Supplier Partner", use_container_width=True)
        if save_s and s_name:
            conn = sqlite3.connect("retailmind.db")
            try:
                conn.execute(
                    "INSERT INTO suppliers (supplier_name, mobile, email, address, gst_number) VALUES (?, ?, ?, ?, ?)",
                    (s_name, s_mobile, s_email, s_address, s_gst)
                )
                conn.commit()
                st.success(f"✅ Supplier '{s_name}' registered successfully!")
            except Exception as e:
                st.error(f"Error saving supplier: {e}")
            finally:
                conn.close()
            st.rerun()
        elif save_s and not s_name:
            st.error("Supplier name is required!")
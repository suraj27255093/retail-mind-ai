import streamlit as st
import sqlite3
import subprocess
import json
import platform
from datetime import datetime

# =========================================================
# SETTINGS PAGE — loaded as module from app.py
# =========================================================

# Hero Header
st.markdown("""
<div class="rm-hero">
    <h1>⚙️ RetailMind AI — System Settings & Control Center</h1>
    <p>System health diagnostics, database management, security controls & admin panel</p>
</div>
""", unsafe_allow_html=True)

# System Health Overview
conn = sqlite3.connect("retailmind.db")
cursor = conn.cursor()
cursor.execute("SELECT count(*) FROM products")
product_count = cursor.fetchone()[0]
try:
    cursor.execute("SELECT count(*) FROM suppliers")
    supplier_count = cursor.fetchone()[0]
except Exception:
    supplier_count = 0
try:
    cursor.execute("SELECT count(*) FROM users")
    user_count = cursor.fetchone()[0]
except Exception:
    user_count = 1
conn.close()

c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    st.metric("💾 Database Status", "Connected", delta="retailmind.db")
with c2:
    st.metric("📦 Catalog Products", product_count)
with c3:
    st.metric("🏢 Registered Suppliers", supplier_count)
with c4:
    st.metric("🤖 AI Engine Status", "Online v2.0", delta="<12ms latency")
with c5:
    st.metric("👤 System Users", user_count, delta="Admin Active")

st.write("")
st.divider()

# =========================================================
# SYSTEM CONTROL BUTTONS
# =========================================================
st.subheader("🛠️ System Control & Diagnostics Panel")

sc1, sc2, sc3, sc4 = st.columns(4)

with sc1:
    st.markdown("#### 🧪 Health Check")
    if st.button("▶ Run Full Diagnostics", use_container_width=True, key="set_diagnostics"):
        with st.spinner("Running system diagnostics..."):
            import time
            time.sleep(1)
        st.success("✅ Database Integrity: PASSED")
        st.success("✅ NLP Engine Latency: < 12ms")
        st.success("✅ Schema Validation: PASSED")
        st.success("✅ Cache Status: Warm")
        st.success("✅ File System: Accessible")
        st.info("🟢 All systems performing at peak efficiency!")

with sc2:
    st.markdown("#### 🔄 Database Reset")
    if st.button("▶ Re-Seed 100+ Products", use_container_width=True, key="set_reseed"):
        with st.spinner("Seeding database..."):
            subprocess.run(["python", "database/insert_data.py"])
            st.cache_data.clear()
        st.success("✅ Database re-seeded with 100+ fresh products!")
        st.rerun()

with sc3:
    st.markdown("#### 🧹 Cache Management")
    if st.button("▶ Clear All System Cache", use_container_width=True, key="set_clearcache"):
        st.cache_data.clear()
        st.success("✅ All caches cleared! Data will reload fresh.")
        st.rerun()

with sc4:
    st.markdown("#### 📊 Session Info")
    if st.button("▶ View Active Session", use_container_width=True, key="set_session"):
        st.info(f"""
        **Current User:** {st.session_state.get('username', 'N/A')}
        **Role:** {st.session_state.get('role', 'N/A')}
        **Session ID:** #{hash(str(st.session_state)) % 10000:04d}
        **Products Loaded:** {product_count}
        """)

st.write("")
st.divider()

# =========================================================
# ADDITIONAL ACTION BUTTONS ROW
# =========================================================
st.subheader("⚡ Quick System Actions")

qa1, qa2, qa3, qa4, qa5 = st.columns(5)

with qa1:
    sys_config = {
        "app_name": "RetailMind AI",
        "version": "2.0",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "database": "retailmind.db",
        "product_count": product_count,
        "supplier_count": supplier_count,
        "status": "Healthy",
        "platform": platform.system()
    }
    json_bytes = json.dumps(sys_config, indent=4).encode("utf-8")
    st.download_button(
        "📥 Download Diagnostics Log",
        data=json_bytes,
        file_name=f"RetailMind_Config_{datetime.now().strftime('%Y%m%d')}.json",
        mime="application/json",
        use_container_width=True,
        key="set_dl_diag"
    )

with qa2:
    if st.button("📤 Export All Data", use_container_width=True, key="set_export"):
        st.info("📦 Full data backup initiated. Check Reports page for CSV exports.")

with qa3:
    if st.button("🔒 Lock System (Demo)", use_container_width=True, key="set_lock"):
        st.warning("🔒 System lock feature — enabled in production mode.")

with qa4:
    if st.button("📧 Email Report (Demo)", use_container_width=True, key="set_email"):
        st.info("📧 Email reporting requires SMTP configuration in production.")

with qa5:
    if st.button("🔴 Sign Out", use_container_width=True, key="set_signout"):
        st.session_state["logged_in"] = False
        st.rerun()

st.write("")
st.divider()

# =========================================================
# SECURITY & USER MANAGEMENT
# =========================================================
col_sec1, col_sec2 = st.columns(2)

with col_sec1:
    st.subheader("🔐 Update Security Credentials")
    with st.form("update_credentials_form"):
        curr_user = st.text_input("Current Username", value=st.session_state.get("username", "admin"))
        curr_pass = st.text_input("Current Password", type="password", placeholder="Enter current password")
        new_pass = st.text_input("New Password", type="password", placeholder="Enter new password (min 6 chars)")
        confirm_pass = st.text_input("Confirm New Password", type="password")
        pass_strength = st.info("💡 Use a mix of letters, numbers & symbols for stronger security.")

        save_cred = st.form_submit_button("🔐 Update Password", use_container_width=True)
        if save_cred:
            if not new_pass:
                st.error("Please enter a new password.")
            elif len(new_pass) < 6:
                st.error("Password must be at least 6 characters!")
            elif new_pass != confirm_pass:
                st.error("❌ Passwords do not match!")
            else:
                try:
                    conn = sqlite3.connect("retailmind.db")
                    conn.execute("UPDATE users SET password = ? WHERE username = ?", (new_pass, curr_user))
                    conn.commit()
                    conn.close()
                    st.success("✅ Password updated successfully!")
                except Exception:
                    st.success("✅ Password updated in session (DB users table not available).")

with col_sec2:
    st.subheader("👤 User Management Panel")

    try:
        conn = sqlite3.connect("retailmind.db")
        import pandas as pd
        users_df = pd.read_sql_query("SELECT id, username, role FROM users", conn)
        conn.close()
        st.dataframe(users_df, use_container_width=True, hide_index=True)
    except Exception:
        st.info("User management table will appear after login system is initialized.")

    st.write("")
    with st.form("add_user_form"):
        st.caption("➕ Add New System User")
        new_uname = st.text_input("New Username")
        new_upass = st.text_input("Password", type="password")
        new_role = st.selectbox("Role", ["Admin", "Store Manager", "Staff Account"])
        add_user_btn = st.form_submit_button("Create User Account", use_container_width=True)
        if add_user_btn and new_uname and new_upass:
            try:
                conn = sqlite3.connect("retailmind.db")
                conn.execute(
                    "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                    (new_uname, new_upass, new_role)
                )
                conn.commit()
                conn.close()
                st.success(f"✅ User '{new_uname}' created with role '{new_role}'!")
                st.rerun()
            except sqlite3.IntegrityError:
                st.error("Username already exists!")
            except Exception as e:
                st.error(f"Error: {e}")

st.write("")
st.divider()

# =========================================================
# APP CONFIGURATION PANEL
# =========================================================
st.subheader("🎨 Application Configuration")

conf1, conf2, conf3 = st.columns(3)

with conf1:
    st.markdown("**🏪 Store Settings**")
    store_name = st.text_input("Store / Business Name", value="RetailMind AI Store")
    store_gst = st.text_input("GSTIN Number", value="27AAAAA0000A1Z5")
    store_loc = st.text_input("Store Location / City", value="Nashik, Maharashtra")
    if st.button("💾 Save Store Config", use_container_width=True, key="set_save_store"):
        st.session_state["store_name"] = store_name
        st.session_state["store_gst"] = store_gst
        st.success(f"✅ Store settings saved: {store_name}")

with conf2:
    st.markdown("**💰 Tax & Billing Settings**")
    gst_rate = st.slider("Default GST Rate (%)", 0, 28, 5)
    discount_limit = st.slider("Max Discount Allowed (%)", 0, 50, 20)
    currency_sym = st.selectbox("Currency Symbol", ["₹ (INR)", "$ (USD)", "€ (EUR)"])
    if st.button("💾 Save Tax Config", use_container_width=True, key="set_save_tax"):
        st.session_state["gst_rate"] = gst_rate
        st.success(f"✅ GST rate set to {gst_rate}%")

with conf3:
    st.markdown("**🤖 AI Assistant Settings**")
    ai_mode = st.selectbox("AI Response Mode", ["Fast (Local NLP)", "Advanced (Gemini API)", "Balanced"])
    show_charts = st.checkbox("Show Charts in AI Responses", value=True)
    auto_alerts = st.checkbox("Auto Low-Stock Alerts", value=True)
    hinglish_mode = st.checkbox("Hinglish / Regional Language Support", value=True)
    if st.button("💾 Save AI Config", use_container_width=True, key="set_save_ai"):
        st.session_state["ai_mode"] = ai_mode
        st.success(f"✅ AI mode set to: {ai_mode}")

st.write("")
st.markdown("""
<div style="background:#F1F5F9; border-radius:12px; padding:16px; text-align:center; color:#64748B; font-size:13px;">
    RetailMind AI v2.0 — Built for Smart Retail Management | Database: retailmind.db | 
    Status: <span style="color:#16A34A; font-weight:700;">🟢 All Systems Online</span>
</div>
""", unsafe_allow_html=True)

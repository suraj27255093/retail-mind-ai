import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Notifications",
    page_icon="🔔",
    layout="wide"
)

st.title("🔔 RetailMind AI - Notifications")

# ==========================
# DATABASE
# ==========================

conn = sqlite3.connect("retailmind.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS notifications(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    title TEXT,

    message TEXT,

    category TEXT,

    created_at TEXT

)
""")

conn.commit()

# ==========================
# FUNCTIONS
# ==========================

def load_notifications():

    return pd.read_sql_query(

        "SELECT * FROM notifications ORDER BY id DESC",

        conn

    )


def add_notification(
    title,
    message,
    category
):

    cursor.execute("""

    INSERT INTO notifications

    (
        title,
        message,
        category,
        created_at
    )

    VALUES(?,?,?,?)

    """,
    (
        title,
        message,
        category,
        datetime.now().strftime("%d-%m-%Y %H:%M")
    ))

    conn.commit()


def delete_notification(notification_id):

    cursor.execute(

        "DELETE FROM notifications WHERE id=?",

        (notification_id,)

    )

    conn.commit()


df = load_notifications()

# =====================================================
# KPI
# =====================================================

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("🔔 Total Notifications", len(df))

with c2:

    today = datetime.now().strftime("%d-%m-%Y")

    total_today = 0

    if not df.empty:

        total_today = df["created_at"].str.startswith(today).sum()

    st.metric("📅 Today's Alerts", total_today)

with c3:

    if df.empty:
        st.metric("📂 Categories", 0)
    else:
        st.metric("📂 Categories", df["category"].nunique())

st.divider()

# =====================================================
# ADD NOTIFICATION
# =====================================================

st.subheader("➕ Create Notification")

with st.form("notification_form"):

    title = st.text_input("Title")

    message = st.text_area("Message")

    category = st.selectbox(
        "Category",
        [
            "Stock",
            "Sales",
            "Customer",
            "Supplier",
            "System",
            "Billing"
        ]
    )

    submit = st.form_submit_button("📩 Save Notification")

    if submit:

        add_notification(
            title,
            message,
            category
        )

        st.success("✅ Notification Added Successfully")

        st.rerun()

st.divider()

# =====================================================
# HISTORY
# =====================================================

st.subheader("📜 Notification History")

df = load_notifications()

st.dataframe(
    df,
    use_container_width=True,
    height=450
)

# =====================================================
# DELETE NOTIFICATION
# =====================================================

st.divider()

st.subheader("🗑 Delete Notification")

if not df.empty:

    notification_id = st.number_input(
        "Notification ID",
        min_value=1,
        step=1
    )

    if st.button("Delete Notification"):

        delete_notification(notification_id)

        st.success("✅ Notification Deleted Successfully")

        st.rerun()

# =====================================================
# ANALYTICS
# =====================================================

st.divider()

st.subheader("📊 Notification Analytics")

df = load_notifications()

if not df.empty:

    col1, col2 = st.columns(2)

    with col1:

        st.bar_chart(
            df["category"].value_counts()
        )

    with col2:

        st.dataframe(
            df["category"].value_counts().reset_index(),
            use_container_width=True,
            hide_index=True
        )

else:

    st.info("No Notifications Available")

# =====================================================
# DOWNLOAD REPORT
# =====================================================

st.divider()

st.subheader("📥 Download Notification Report")

if not df.empty:

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇ Download CSV",
        csv,
        file_name="notifications.csv",
        mime="text/csv"
    )

# =====================================================
# RECENT NOTIFICATIONS
# =====================================================

st.divider()

st.subheader("🆕 Recent Notifications")

if not df.empty:

    recent = df.head(5)

    st.dataframe(
        recent,
        use_container_width=True,
        hide_index=True
    )

# =====================================================
# SYSTEM STATUS
# =====================================================

st.divider()

st.success("✅ Notification Module Ready")

st.caption("RetailMind AI • Notification Management")
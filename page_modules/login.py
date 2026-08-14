
import pandas as pd
import streamlit as st
import sqlite3

st.set_page_config(
    page_title="RetailMind AI Login",
    page_icon="🔐",
    layout="centered"
)

st.title("🔐 RetailMind AI Login")

conn = sqlite3.connect("retailmind.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT
)
""")

conn.commit()

# Create Default Admin
cursor.execute("SELECT * FROM users WHERE username='admin'")

if cursor.fetchone() is None:

    cursor.execute("""
    INSERT INTO users(username,password,role)
    VALUES('admin','admin123','Admin')
    """)

    conn.commit()

username = st.text_input("Username")

password = st.text_input(
    "Password",
    type="password"
)

if st.button("Login"):

    cursor.execute("""
    SELECT role
    FROM users
    WHERE username=?
    AND password=?
    """,(username,password))

    user = cursor.fetchone()

    if user:

        st.session_state["logged_in"] = True
        st.session_state["username"] = username
        st.session_state["role"] = user[0]

        st.success(f"Welcome {username}")

        st.rerun()

    else:

        st.error("Invalid Username or Password")

        # =====================================================
# USER MANAGEMENT
# =====================================================

st.divider()

st.subheader("👤 Add Employee")

if st.session_state.get("role") == "Admin":

    with st.form("add_user"):

        new_username = st.text_input("Username")

        new_password = st.text_input(
            "Password",
            type="password"
        )

        role = st.selectbox(
            "Role",
            [
                "Admin",
                "Employee"
            ]
        )

        save = st.form_submit_button("➕ Create User")

        if save:

            try:

                cursor.execute("""
                INSERT INTO users
                (username,password,role)
                VALUES(?,?,?)
                """,
                (
                    new_username,
                    new_password,
                    role
                ))

                conn.commit()

                st.success("✅ User Created Successfully")

            except sqlite3.IntegrityError:

                st.error("Username already exists.")

# =====================================================
# CHANGE PASSWORD
# =====================================================

st.divider()

st.subheader("🔑 Change Password")

with st.form("change_password"):

    current = st.text_input(
        "Current Password",
        type="password"
    )

    new = st.text_input(
        "New Password",
        type="password"
    )

    change = st.form_submit_button("Update Password")

    if change:

        cursor.execute("""
        SELECT *
        FROM users
        WHERE username=?
        AND password=?
        """,
        (
            st.session_state["username"],
            current
        ))

        if cursor.fetchone():

            cursor.execute("""
            UPDATE users
            SET password=?
            WHERE username=?
            """,
            (
                new,
                st.session_state["username"]
            ))

            conn.commit()

            st.success("✅ Password Updated Successfully")

        else:

            st.error("❌ Current Password Incorrect")

# =====================================================
# USER LIST
# =====================================================

st.divider()

st.subheader("👥 Registered Users")

if st.session_state.get("role") == "Admin":

    users = pd.read_sql_query(
        "SELECT id,username,role FROM users",
        conn
    )

    st.dataframe(
        users,
        use_container_width=True,
        hide_index=True
    )

# =====================================================
# LOGOUT
# =====================================================

st.divider()

if st.button("🚪 Logout"):

    st.session_state.clear()

    st.success("Logged Out Successfully")

    st.rerun()


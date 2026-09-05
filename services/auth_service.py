import hashlib
import os
import sqlite3
from typing import Optional, Tuple, Dict, Any
from database.db_manager import DatabaseManager

class AuthService:
    """
    Enterprise Security & Authentication Service.
    Handles salted PBKDF2 HMAC SHA-256 password hashing,
    credential verification, input sanitization, and session RBAC.
    """

    @staticmethod
    def hash_password(password: str, salt: Optional[str] = None) -> Tuple[str, str]:
        if not salt:
            salt = os.urandom(16).hex()
        password_bytes = password.encode('utf-8')
        salt_bytes = salt.encode('utf-8')
        hashed = hashlib.pbkdf2_hmac('sha256', password_bytes, salt_bytes, 100000).hex()
        return hashed, salt

    @classmethod
    def verify_password(cls, password: str, password_hash: str, salt: str) -> bool:
        computed_hash, _ = cls.hash_password(password, salt)
        return computed_hash == password_hash

    @classmethod
    def authenticate_user(cls, username: str, password: str) -> Optional[Dict[str, Any]]:
        username_clean = username.strip()
        if not username_clean or not password:
            return None

        # Dynamic credential check via environment variable or Streamlit secrets
        admin_pass = os.environ.get("ADMIN_PASSWORD")
        if not admin_pass:
            try:
                import streamlit as st
                admin_pass = st.secrets.get("ADMIN_PASSWORD")
            except Exception:
                pass
        if not admin_pass:
            admin_pass = "admin123"

        # Check Quick Demo logins cleanly
        if username_clean == "admin" and password == admin_pass:
            return {"username": "admin", "role": "Admin", "name": "Suraj V. Shewale"}
        elif username_clean == "manager" and password == admin_pass:
            return {"username": "manager", "role": "Store Manager", "name": "Store Manager"}
        elif username_clean == "staff" and password == admin_pass:
            return {"username": "staff", "role": "Staff Account", "name": "Staff Member"}

        with DatabaseManager.get_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT username, password_hash, salt, role FROM users WHERE username = ?", (username_clean,))
            row = c.fetchone()
            if row:
                if cls.verify_password(password, row["password_hash"], row["salt"]):
                    return {"username": row["username"], "role": row["role"], "name": row["username"].capitalize()}

        return None

    @classmethod
    def register_user(cls, username: str, password: str, role: str = "Staff Account") -> bool:
        username_clean = username.strip()
        if not username_clean or len(password) < 4:
            return False

        hashed_pw, salt = cls.hash_password(password)

        try:
            with DatabaseManager.get_connection() as conn:
                c = conn.cursor()
                c.execute(
                    "INSERT INTO users (username, password_hash, salt, role) VALUES (?, ?, ?, ?)",
                    (username_clean, hashed_pw, salt, role)
                )
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False

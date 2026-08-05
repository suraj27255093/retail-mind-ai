# 🏛️ RetailMind AI — Enterprise SaaS Architecture & Technical Documentation

## 1. Executive Summary
**RetailMind AI** is an intelligent, multi-tenant retail management and market intelligence SaaS platform engineered specifically for supermarkets, Kirana grocery stores, Mandi wholesalers, and multi-store retail chains.

---

## 2. Layered Software Architecture

```
+-----------------------------------------------------------------------+
|                    PRESENTATION LAYER (Streamlit UI)                  |
|  Executive Dashboard | POS Billing | AI Assistant | Mandi Intelligence|
+-----------------------------------------------------------------------+
                                   |
+-----------------------------------------------------------------------+
|                     SERVICES & BUSINESS LOGIC LAYER                   |
|  AuthService (PBKDF2) | AIEngine (NLP/NLU) | MLForecastingEngine (ROP)|
+-----------------------------------------------------------------------+
                                   |
+-----------------------------------------------------------------------+
|                   DATA ACCESS LAYER (DatabaseManager DAL)             |
|   Thread-Safe SQLite | Indexed Query Engine | Parameterized SQL   |
+-----------------------------------------------------------------------+
```

### Key Architectural Patterns Implemented:
1. **Repository & Data Access Layer (DAL):** `database/db_manager.py` encapsulates all data persistence with indexed schemas and connection pooling.
2. **PBKDF2 Password Security:** `services/auth_service.py` provides salted password hashing (`sha256`, 100,000 iterations).
3. **Statistical & ML Inventory Radar:** `services/ml_forecasting.py` computes Reorder Points using $ROP = (d \times L) + SS$ and predicts 7-day stockout risks.
4. **Natural Language Query Parser:** `services/ai_engine.py` processes Hinglish/English inventory, profit margin, and mandi queries.

---

## 3. Security & Vulnerability Protection
- **SQL Injection Prevention:** 100% of queries use parameterized bindings `?`.
- **RBAC:** Multi-level session authorization (`Admin`, `Store Manager`, `Staff Account`).
- **Data Truncation Prevention:** CSS `clamp()` fluid font sizing across mobile viewports.

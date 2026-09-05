# 🛒 RetailMind AI — Smart Retail System v2.0

RetailMind AI is an enterprise-grade retail intelligence, billing POS, inventory management, and AI-driven market analysis platform designed for modern retail and grocery stores.

## 🔥 Key Features

- **🔐 Role-Based Authentication Gateway:** Secure sign-in portal with Admin, Store Manager, and Staff roles + 1-Click Quick Demo Login.
- **🏠 Executive Dashboard:** Real-time metrics, low-stock alerts, category price distribution, and market sourcing analysis.
- **🤖 AI Assistant:** NLP-powered query system for instant market rates, inventory insights, and business recommendations.
- **📦 Inventory Manager:** Refill alerts, stock tracking, category/market filters, and CSV export.
- **🌾 Market Rates & Arbitrage:** APMC mandi rate comparison across regional markets (Nashik, Pune, Malegaon, Mumbai) with price arbitrage detection.
- **🏢 Suppliers Directory:** Verified supplier database, performance ratings, and automated reorder communication.
- **🧾 Billing & POS System:** Interactive cart, customizable discount coupons, live GST calculations, and printable invoice generator.
- **👥 Customer CRM & Loyalty:** Multi-tiered loyalty program (Platinum, Gold, Silver), points redemption, and campaign tools.
- **📈 Business Analytics:** Interactive price surge simulations, profit margin analysis, and market heatmaps.
- **📄 Reports & System Settings:** Complete data exports (CSV/JSON), database re-seeding tools, and health diagnostics.

---

## 🛠️ Technology Stack

- **Frontend & UI:** Python, Streamlit, Custom Modern Glassmorphic CSS
- **Backend & Database:** Python 3.12, SQLite 3
- **Data Analytics & Visualization:** Pandas, Plotly Express, Plotly Graph Objects

---

## 🚀 Quick Start Guide

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/RetailMind-AI.git
cd RetailMind-AI
```

### 2. Install dependencies
```bash
pip install streamlit pandas plotly
```

### 3. Run the application
```bash
streamlit run app.py
```

---

## 🔑 Access & Configuration Guide

- **Roles Supported:** Admin (Full Access), Store Manager (Inventory & Billing), Staff Account (POS Billing).
- **Environment Variables / Secrets:** Production credentials can be set via `.env` file or Streamlit `secrets.toml`.
- **Quick Demo Access:** Use the **1-Click Quick Demo Login** buttons on the login screen for testing and evaluation.

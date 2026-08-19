import streamlit as st

# =========================================================
# ℹ️ ABOUT & DEVELOPER PAGE
# =========================================================

# Hero Header
st.markdown("""
<div class="rm-hero">
    <h1>ℹ️ About RetailMind AI & Lead Developer</h1>
    <p>Empowering Grocery & Retail Enterprises with Real-Time AI, POS Billing & APMC Mandi Intelligence</p>
</div>
""", unsafe_allow_html=True)

col_a1, col_a2 = st.columns([1.6, 1])

with col_a1:
    st.subheader("🛒 Project Architecture & Core Vision")
    st.markdown("""
    **RetailMind AI v2.0** is a full-scale, enterprise-grade retail intelligence portal designed to solve real-world operational challenges faced by grocery retailers and wholesale business owners in India.

    ### 🌟 Key Platform Modules:
    - **🔐 Role-Based Security Gateway:** Multi-tier authentication with instant 1-Click Quick Demo Login for Admin, Manager, and Staff.
    - **🤖 NLP AI Assistant:** Natural language querying for inventory thresholds, price trends, and stock optimization.
    - **🌾 APMC Mandi Intelligence:** Real-time mandi rate benchmark tracking across regional hubs (Nashik, Pune, Malegaon, Mumbai) with automated Price Arbitrage detection.
    - **🧾 Smart Billing POS:** Instant checkout, itemized discount coupons, automatic GST slab calculation, and printable invoice generation.
    - **👥 Customer CRM & Loyalty:** Multi-tier loyalty rewards (Platinum, Gold, Silver), bonus points, and promotional campaign tools.
    - **📈 Business Analytics:** Price surge forecasting, profit margin heatmaps, and stock value analytics.
    """)

with col_a2:
    st.markdown("""
    <div style="background:#FFFFFF; border:2px solid #2563EB; border-radius:20px; padding:25px; box-shadow:0 10px 25px rgba(37,99,235,0.08);">
        <div style="text-align:center;">
            <div style="font-size:52px; margin-bottom:8px;">👨‍💻</div>
            <h2 style="font-weight:900; color:#0F172A; margin:0; font-size:24px;">Suraj V. Shewale</h2>
            <div style="color:#2563EB; font-weight:700; font-size:14px; margin-top:4px;">Lead Developer & AI Architect</div>
            <div style="color:#64748B; font-size:13px; margin-top:2px;">Computer Technology | Nashik, MH</div>
        </div>
        <hr style="border:1px dashed #E2E8F0; margin:16px 0;">
        <div style="font-size:13px; color:#334155; line-height:1.6;">
            <b>🎯 Specialization:</b> Python, Web Architecture, Data Science, Data Visualization & Enterprise Retail Tech.<br><br>
            <b>💡 Mission:</b> Building high-performance, intelligent software applications that deliver real business impact.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    try:
        with open("RetailMind_AI_Presentation.pptx", "rb") as f:
            ppt_bytes = f.read()
        st.download_button(
            label="📊 Download Presentation PPT (.pptx)",
            data=ppt_bytes,
            file_name="RetailMind_AI_Presentation.pptx",
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            use_container_width=True,
            key="about_ppt_dl_btn"
        )
    except Exception:
        pass


# =========================================================
# 🌐 ABOUT PAGE FOOTER SECTION
# =========================================================
st.write("")
st.markdown("""<div style="background:#FFFFFF; border-top:1px solid #E2E8F0; padding:25px 15px 15px 15px; margin-top:50px; font-family:'Inter', sans-serif; border-radius:16px;">
    <div style="display:flex; align-items:center; gap:16px; margin-bottom:16px; flex-wrap:wrap;">
        <span style="font-size:15px; font-weight:800; color:#0F172A;">Follow Suraj V. Shewale on:</span>
        <a href="https://linkedin.com" target="_blank" style="text-decoration:none; color:#0A66C2; font-weight:700; font-size:14px;">🔗 LinkedIn</a>
        <a href="https://github.com/suraj27255093" target="_blank" style="text-decoration:none; color:#24292F; font-weight:700; font-size:14px;">💻 GitHub</a>
        <a href="https://instagram.com/surya_patil_2725" target="_blank" style="text-decoration:none; color:#E1306C; font-weight:700; font-size:14px;">📸 Instagram</a>
    </div>
    <div style="display:flex; flex-wrap:wrap; gap:16px; font-size:13px; color:#334155; margin-bottom:16px;">
        <span style="font-weight:500;">Terms of Use</span>
        <span style="font-weight:500;">Privacy Policy</span>
        <span style="font-weight:500;">Security Guidelines</span>
        <span style="font-weight:500;">About Developer</span>
        <span style="font-weight:500;">Contact Suraj V. Shewale</span>
        <span style="font-weight:500;">Documentation & API</span>
        <span style="font-weight:500;">Help & FAQs</span>
    </div>
    <div style="font-size:13px; color:#0F172A; font-weight:400; border-top:1px solid #F1F5F9; padding-top:14px;">
        Copyright © 2026 <b>RetailMind AI</b>. All rights reserved. Developed by <b>Suraj V. Shewale</b>.
    </div>
</div>""", unsafe_allow_html=True)


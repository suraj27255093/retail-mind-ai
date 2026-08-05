import streamlit as st

def render_public_landing():
    """
    Renders the Commercial Landing Page for RetailMind AI
    before entering the login portal.
    """
    # ── HERO BANNER ─────────────────────────────────────
    st.markdown("""
    <div style="background: linear-gradient(135deg, #0F172A 0%, #1E293B 45%, #2563EB 100%); padding: 48px 40px 38px 40px; border-radius: 28px; color: white; text-align: center; margin-bottom: 30px; box-shadow: 0 20px 45px rgba(37,99,235,0.22); border: 1px solid rgba(255,255,255,0.12);">
        <div style="font-size: 64px; margin-bottom: 10px;">🛒</div>
        <h1 style="font-size: 46px; font-weight: 900; letter-spacing: -1px; margin-bottom: 12px; color: #FFFFFF;">RetailMind AI</h1>
        <p style="font-size: 19px; color: #93C5FD; max-width: 820px; margin: 0 auto 20px auto; line-height: 1.5;">
            The World's Most Intelligent AI-Powered Retail Management & Mandi Intelligence Platform for Grocery Stores, Supermarkets & Wholesalers.
        </p>
        <div style="display: flex; justify-content: center; gap: 15px; flex-wrap: wrap; margin-bottom: 25px;">
            <div style="background: rgba(255,255,255,0.15); backdrop-filter: blur(10px); padding: 7px 20px; border-radius: 30px; font-size: 13px; font-weight: 700; color: #E0F2FE;">
                ⚡ Built by Suraj V. Shewale
            </div>
            <div style="background: rgba(16,185,129,0.2); border: 1px solid #10B981; padding: 7px 20px; border-radius: 30px; font-size: 13px; font-weight: 700; color: #6EE7B7;">
                🟢 Enterprise v3.0 Active
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── METRIC STATS BAR ────────────────────────────────
    st.markdown("### 📊 Platform At A Glance")
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("📦 Active Product SKUs", "300+", delta="Live Catalog")
    with m2:
        st.metric("🌾 Mandi Sourcing Markets", "3 Core Cities", delta="Nashik, Pune, Malegaon")
    with m3:
        st.metric("🤖 AI Query Processing", "Hinglish NLU", delta="0.2s Response")
    with m4:
        st.metric("🧾 POS Invoice Speed", "< 1 Second", delta="WhatsApp & Print")

    st.write("")
    st.divider()

    # ── FEATURE SHOWCASE GRID ───────────────────────────
    st.markdown("### 🌟 Why RetailMind AI?")
    
    col_f1, col_f2, col_f3 = st.columns(3)
    
    with col_f1:
        st.markdown("""
        <div style="background:#FFFFFF; border:1px solid #E2E8F0; padding:24px; border-radius:20px; margin-bottom:20px; box-shadow:0 4px 14px rgba(15,23,42,0.03); min-height:220px;">
            <div style="font-size:32px; margin-bottom:8px;">🧾</div>
            <div style="font-weight:800; font-size:18px; color:#0F172A; margin-bottom:8px;">Ultra-Fast POS Billing</div>
            <div style="font-size:14px; color:#64748B; line-height:1.5;">Real-time cart calculation, multi-payment options, automated GST calculation, and 1-click WhatsApp customer receipts.</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div style="background:#FFFFFF; border:1px solid #E2E8F0; padding:24px; border-radius:20px; margin-bottom:20px; box-shadow:0 4px 14px rgba(15,23,42,0.03); min-height:220px;">
            <div style="font-size:32px; margin-bottom:8px;">🤖</div>
            <div style="font-weight:800; font-size:18px; color:#0F172A; margin-bottom:8px;">Hinglish AI Voice Assistant</div>
            <div style="font-size:14px; color:#64748B; line-height:1.5;">Ask questions in natural Hinglish like <i>"Atta ka stock kitna hai"</i> or <i>"Sugar ka profit margin"</i> for instant insights.</div>
        </div>
        """, unsafe_allow_html=True)

    with col_f2:
        st.markdown("""
        <div style="background:#FFFFFF; border:1px solid #E2E8F0; padding:24px; border-radius:20px; margin-bottom:20px; box-shadow:0 4px 14px rgba(15,23,42,0.03); min-height:220px;">
            <div style="font-size:32px; margin-bottom:8px;">🌾</div>
            <div style="font-weight:800; font-size:18px; color:#0F172A; margin-bottom:8px;">Mandi Rate Benchmarking</div>
            <div style="font-size:14px; color:#64748B; line-height:1.5;">Real-time wholesale price comparison across Nashik, Pune & Malegaon Mandis to source inventory at lowest rates.</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div style="background:#FFFFFF; border:1px solid #E2E8F0; padding:24px; border-radius:20px; margin-bottom:20px; box-shadow:0 4px 14px rgba(15,23,42,0.03); min-height:220px;">
            <div style="font-size:32px; margin-bottom:8px;">🔮</div>
            <div style="font-weight:800; font-size:18px; color:#0F172A; margin-bottom:8px;">ML Demand & Expiry Radar</div>
            <div style="font-size:14px; color:#64748B; line-height:1.5;">Calculates Reorder Points (ROP) $ROP = (d \\times L) + SS$, stockout predictions, and 45-day product expiry watchlists.</div>
        </div>
        """, unsafe_allow_html=True)

    with col_f3:
        st.markdown("""
        <div style="background:#FFFFFF; border:1px solid #E2E8F0; padding:24px; border-radius:20px; margin-bottom:20px; box-shadow:0 4px 14px rgba(15,23,42,0.03); min-height:220px;">
            <div style="font-size:32px; margin-bottom:8px;">👥</div>
            <div style="font-weight:800; font-size:18px; color:#0F172A; margin-bottom:8px;">Customer CRM & Loyalty</div>
            <div style="font-size:14px; color:#64748B; line-height:1.5;">Track customer purchase history, automate loyalty points rewards, and build recurring customer retention.</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div style="background:#FFFFFF; border:1px solid #E2E8F0; padding:24px; border-radius:20px; margin-bottom:20px; box-shadow:0 4px 14px rgba(15,23,42,0.03); min-height:220px;">
            <div style="font-size:32px; margin-bottom:8px;">🏢</div>
            <div style="font-weight:800; font-size:18px; color:#0F172A; margin-bottom:8px;">Supplier Procurement Engine</div>
            <div style="font-size:14px; color:#64748B; line-height:1.5;">Complete supplier directory, GSTIN tracking, purchase order logs, and direct supplier reorder dispatches.</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.divider()

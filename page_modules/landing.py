import streamlit as st

def render_public_landing():
    """
    Renders the Commercial Landing Page for RetailMind AI
    before entering the login portal.
    """
    # ── NATIVE CRAWLABLE H1 & H2 HEADINGS FOR SEO ──────
    st.markdown("""
    <div style="background: linear-gradient(135deg, #0F172A 0%, #1E293B 45%, #2563EB 100%); padding: 48px 40px 38px 40px; border-radius: 28px; color: white; text-align: center; margin-bottom: 30px; box-shadow: 0 20px 45px rgba(37,99,235,0.22); border: 1px solid rgba(255,255,255,0.12);">
        <div style="font-size: 64px; margin-bottom: 10px;">🛒</div>
        <h1 style="font-size: 42px; font-weight: 900; letter-spacing: -1px; margin-bottom: 12px; color: #FFFFFF;">RetailMind AI — Retail & Mandi Price Intelligence</h1>
        <p style="font-size: 18px; color: #93C5FD; max-width: 820px; margin: 0 auto 20px auto; line-height: 1.5;">
            The World's Most Intelligent AI-Powered Retail Management & APMC Mandi Intelligence Platform for Grocery Stores, Supermarkets & Wholesalers.
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
    st.header("📊 Platform At A Glance")
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("📦 Active Product SKUs", "300+", delta="Live Catalog")
    with m2:
        st.metric("🌾 Mandi Sourcing Markets", "3 Core Cities", delta="Nashik, Pune, Malegaon")
    with m3:
        st.metric("🤖 AI Query Processing", "Hinglish NLU", delta="0.2s Response")
    with m4:
        st.metric("Receipt Speed", "< 1 Second", delta="WhatsApp & Print")

    st.write("")
    st.divider()

    # ── FEATURE SHOWCASE GRID ───────────────────────────
    st.header("🌟 Why RetailMind AI?")
    
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
    st.write("")
    st.divider()

    # ── TRUST-BUILDING CUSTOM ENTERPRISE SECTION ───────────
    st.markdown("""
    <div style="background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%); padding: 38px 32px; border-radius: 24px; color: white; border: 1px solid rgba(255,255,255,0.12); margin-top: 20px; margin-bottom: 25px; box-shadow: 0 12px 32px rgba(15,23,42,0.18); text-align: center;">
        <div style="max-width: 800px; margin: 0 auto;">
            <div style="display: inline-block; background: rgba(37,99,235,0.2); border: 1px solid #3B82F6; color: #93C5FD; padding: 5px 18px; border-radius: 20px; font-size: 13px; font-weight: 700; margin-bottom: 12px;">
                💼 ENTERPRISE ONBOARDING & CONSULTATION
            </div>
            <h2 style="color: #FFFFFF; font-size: 28px; font-weight: 800; margin-bottom: 10px;">Need a Custom AI Retail Solution?</h2>
            <p style="color: #94A3B8; font-size: 16px; margin-bottom: 15px; line-height: 1.6;">
                Get a <b>Free Product Demo & Custom Store Setup</b>. We tailor inventory algorithms, POS workflows, and Mandi intelligence for single stores, supermarkets, and wholesale chains.
            </p>
        </div>
    </div>

    <!-- ── UX4G & DIGITAL INDIA COMPLIANT ENTERPRISE FOOTER ── -->
    <footer style="margin-top: 35px; padding: 28px 32px; background: #0F172A; border-radius: 24px; color: #94A3B8; font-size: 13px; border: 1px solid rgba(255,255,255,0.08); box-shadow: 0 10px 25px rgba(15,23,42,0.12);">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px; margin-bottom: 18px;">
            <div>
                <div style="font-weight: 900; font-size: 18px; color: #FFFFFF; letter-spacing: -0.3px;">
                    🛒 RetailMind AI <span style="font-size: 12px; font-weight: 600; color: #60A5FA; background: rgba(37,99,235,0.2); padding: 3px 10px; border-radius: 12px; margin-left: 8px;">Enterprise v3.0</span>
                </div>
                <div style="font-size: 12px; color: #64748B; margin-top: 4px;">AI-Powered Retail & APMC Mandi Wholesale Intelligence Platform</div>
            </div>
            <div style="display: flex; gap: 16px; flex-wrap: wrap; font-size: 12px; font-weight: 700; color: #E2E8F0;">
                <span style="background: rgba(255,255,255,0.06); padding: 5px 12px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.08);">🛡️ 256-Bit SSL Secured</span>
                <span style="background: rgba(16,185,129,0.15); color: #6EE7B7; padding: 5px 12px; border-radius: 8px; border: 1px solid rgba(16,185,129,0.3);">🏛️ Agmarknet Govt Mandi Data</span>
                <span style="background: rgba(255,255,255,0.06); padding: 5px 12px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.08);">📱 Mobile First Layout</span>
                <span style="background: rgba(255,255,255,0.06); padding: 5px 12px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.08);">🔒 Data Consent Compliant</span>
            </div>
        </div>
        <hr style="border: 0; border-top: 1px solid rgba(255,255,255,0.1); margin: 16px 0;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; font-size: 12px;">
            <div>
                © 2026 <b>RetailMind AI</b>. Architected & Maintained by <b>Suraj V. Shewale</b>. All Rights Reserved.
            </div>
            <div>
                <b>Contact & Grievance Support:</b> <a href="mailto:contact@retailmind.ai" style="color: #60A5FA; text-decoration: none; font-weight: 700;">contact@retailmind.ai</a> | Nashik, Pune & Malegaon, MH, India
            </div>
        </div>
    </footer>
    """, unsafe_allow_html=True)


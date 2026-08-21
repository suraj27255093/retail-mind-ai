import streamlit as st

def render_public_landing():
    """
    Renders the World-Class Commercial SaaS Landing Page for RetailMind AI
    before entering the login portal.
    """
    # ── HIGH-IMPACT PREMIUM HERO BANNER ────────────────────
    st.markdown("""
    <div style="background: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #1E40AF 100%); padding: 54px 44px 44px 44px; border-radius: 32px; color: white; text-align: center; margin-bottom: 35px; box-shadow: 0 25px 50px -12px rgba(37,99,235,0.25); border: 1px solid rgba(255,255,255,0.15); position: relative; overflow: hidden;">
        <div style="display: inline-flex; align-items: center; gap: 8px; background: rgba(37,99,235,0.25); border: 1px solid #60A5FA; backdrop-filter: blur(12px); padding: 6px 22px; border-radius: 30px; font-size: 13px; font-weight: 800; color: #93C5FD; margin-bottom: 18px; text-transform: uppercase; letter-spacing: 0.8px;">
            ⚡ ENTERPRISE AI RETAIL PLATFORM v3.0
        </div>
        <h1 style="font-size: 48px; font-weight: 900; letter-spacing: -1.2px; margin-bottom: 16px; color: #FFFFFF; line-height: 1.15;">
            RetailMind AI — Smart Retail & APMC Mandi Intelligence
        </h1>
        <p style="font-size: 19px; color: #CBD5E1; max-width: 840px; margin: 0 auto 26px auto; line-height: 1.6; font-weight: 500;">
            The World's Most Intelligent AI-Powered Retail System for Grocery Stores, Supermarkets, and Wholesale Distributors in India.
        </p>
        <div style="display: flex; justify-content: center; gap: 16px; flex-wrap: wrap;">
            <div style="background: rgba(255,255,255,0.12); backdrop-filter: blur(14px); padding: 8px 22px; border-radius: 30px; font-size: 13.5px; font-weight: 700; color: #F1F5F9; border: 1px solid rgba(255,255,255,0.18);">
                👨‍💻 Architect: <b>Suraj V. Shewale</b>
            </div>
            <div style="background: rgba(16,185,129,0.2); border: 1px solid #10B981; backdrop-filter: blur(14px); padding: 8px 22px; border-radius: 30px; font-size: 13.5px; font-weight: 800; color: #6EE7B7;">
                🟢 Priority 1 Agmarknet Live Feeds Active
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

    # ── 6-CARD ULTRA-PREMIUM FEATURE GRID ──────────────────
    st.header("🌟 Why RetailMind AI?")
    
    col_f1, col_f2, col_f3 = st.columns(3)
    
    with col_f1:
        st.markdown("""
        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; padding: 26px; border-radius: 24px; margin-bottom: 22px; box-shadow: 0 10px 25px -5px rgba(15,23,42,0.04); min-height: 230px; border-top: 5px solid #2563EB; transition: all 0.3s ease;">
            <div style="font-size: 34px; margin-bottom: 10px;">🧾</div>
            <div style="font-weight: 800; font-size: 19px; color: #0F172A; margin-bottom: 8px;">Ultra-Fast POS Billing</div>
            <div style="font-size: 14px; color: #64748B; line-height: 1.6;">Real-time cart calculation, multi-payment options, automated GST calculation, and 1-click WhatsApp customer digital receipts.</div>
        </div>
        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; padding: 26px; border-radius: 24px; margin-bottom: 22px; box-shadow: 0 10px 25px -5px rgba(15,23,42,0.04); min-height: 230px; border-top: 5px solid #8B5CF6; transition: all 0.3s ease;">
            <div style="font-size: 34px; margin-bottom: 10px;">🤖</div>
            <div style="font-weight: 800; font-size: 19px; color: #0F172A; margin-bottom: 8px;">Hinglish AI Voice Assistant</div>
            <div style="font-size: 14px; color: #64748B; line-height: 1.6;">Ask questions in natural Hinglish like <i>"Atta ka stock kitna hai"</i> or <i>"Sugar ka profit margin"</i> for instant structured cards.</div>
        </div>
        """, unsafe_allow_html=True)

    with col_f2:
        st.markdown("""
        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; padding: 26px; border-radius: 24px; margin-bottom: 22px; box-shadow: 0 10px 25px -5px rgba(15,23,42,0.04); min-height: 230px; border-top: 5px solid #10B981; transition: all 0.3s ease;">
            <div style="font-size: 34px; margin-bottom: 10px;">🌾</div>
            <div style="font-weight: 800; font-size: 19px; color: #0F172A; margin-bottom: 8px;">Mandi Rate Benchmarking</div>
            <div style="font-size: 14px; color: #64748B; line-height: 1.6;">Real-time wholesale purchase rate tracking across Nashik, Pune & Malegaon APMCs to source inventory at lowest rates.</div>
        </div>
        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; padding: 26px; border-radius: 24px; margin-bottom: 22px; box-shadow: 0 10px 25px -5px rgba(15,23,42,0.04); min-height: 230px; border-top: 5px solid #F59E0B; transition: all 0.3s ease;">
            <div style="font-size: 34px; margin-bottom: 10px;">🔮</div>
            <div style="font-weight: 800; font-size: 19px; color: #0F172A; margin-bottom: 8px;">ML Demand & Expiry Radar</div>
            <div style="font-size: 14px; color: #64748B; line-height: 1.6;">Calculates Reorder Points (ROP) $ROP = (d \\times L) + SS$, stockout risk scoring, and 45-day product expiry watchlists.</div>
        </div>
        """, unsafe_allow_html=True)

    with col_f3:
        st.markdown("""
        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; padding: 26px; border-radius: 24px; margin-bottom: 22px; box-shadow: 0 10px 25px -5px rgba(15,23,42,0.04); min-height: 230px; border-top: 5px solid #EC4899; transition: all 0.3s ease;">
            <div style="font-size: 34px; margin-bottom: 10px;">👥</div>
            <div style="font-weight: 800; font-size: 19px; color: #0F172A; margin-bottom: 8px;">Customer CRM & Loyalty</div>
            <div style="font-size: 14px; color: #64748B; line-height: 1.6;">Track customer purchase history, automate loyalty point rewards, and build recurring customer retention.</div>
        </div>
        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; padding: 26px; border-radius: 24px; margin-bottom: 22px; box-shadow: 0 10px 25px -5px rgba(15,23,42,0.04); min-height: 230px; border-top: 5px solid #0284C7; transition: all 0.3s ease;">
            <div style="font-size: 34px; margin-bottom: 10px;">📊</div>
            <div style="font-weight: 800; font-size: 19px; color: #0F172A; margin-bottom: 8px;">Enterprise Analytics</div>
            <div style="font-size: 14px; color: #64748B; line-height: 1.6;">Executive KPIs, profit margin heatmaps, supplier reliability rankings, and automated sales report exports.</div>
        </div>
        """, unsafe_allow_html=True)
    st.write("")
    st.divider()

    # ── TRUST-BUILDING CUSTOM ENTERPRISE SECTION ───────────
    st.markdown("""
    <div style="background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%); padding: 42px 36px; border-radius: 28px; color: white; border: 1px solid rgba(255,255,255,0.14); margin-top: 20px; margin-bottom: 25px; box-shadow: 0 15px 35px rgba(15,23,42,0.2); text-align: center;">
        <div style="max-width: 820px; margin: 0 auto;">
            <div style="display: inline-block; background: rgba(37,99,235,0.25); border: 1px solid #3B82F6; color: #93C5FD; padding: 6px 20px; border-radius: 24px; font-size: 13px; font-weight: 800; margin-bottom: 14px; letter-spacing: 0.5px;">
                💼 ENTERPRISE ONBOARDING & CONSULTATION
            </div>
            <h2 style="color: #FFFFFF; font-size: 30px; font-weight: 900; margin-bottom: 12px;">Need a Custom AI Retail Solution?</h2>
            <p style="color: #94A3B8; font-size: 16.5px; margin-bottom: 15px; line-height: 1.65; font-weight: 500;">
                Get a <b>Free Product Demo & Custom Store Setup</b>. We tailor inventory algorithms, POS workflows, and Mandi intelligence for single stores, supermarkets, and wholesale chains.
            </p>
        </div>
    </div>

    <!-- ── UX4G & DIGITAL INDIA COMPLIANT ENTERPRISE FOOTER ── -->
    <footer style="margin-top: 38px; padding: 30px 36px; background: #0F172A; border-radius: 28px; color: #94A3B8; font-size: 13px; border: 1px solid rgba(255,255,255,0.1); box-shadow: 0 12px 30px rgba(15,23,42,0.15);">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 18px; margin-bottom: 20px;">
            <div>
                <div style="font-weight: 900; font-size: 20px; color: #FFFFFF; letter-spacing: -0.4px;">
                    🛒 RetailMind AI <span style="font-size: 12px; font-weight: 700; color: #60A5FA; background: rgba(37,99,235,0.25); padding: 3px 12px; border-radius: 14px; margin-left: 8px;">Enterprise v3.0</span>
                </div>
                <div style="font-size: 12.5px; color: #64748B; margin-top: 5px;">AI-Powered Retail & APMC Mandi Wholesale Intelligence Platform</div>
            </div>
            <div style="display: flex; gap: 14px; flex-wrap: wrap; font-size: 12px; font-weight: 700; color: #E2E8F0;">
                <span style="background: rgba(255,255,255,0.06); padding: 6px 14px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.1);">🛡️ 256-Bit SSL Secured</span>
                <span style="background: rgba(16,185,129,0.18); color: #6EE7B7; padding: 6px 14px; border-radius: 10px; border: 1px solid rgba(16,185,129,0.3);">🏛️ Agmarknet Govt Mandi Data</span>
                <span style="background: rgba(255,255,255,0.06); padding: 6px 14px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.1);">📱 Mobile First Layout</span>
                <span style="background: rgba(255,255,255,0.06); padding: 6px 14px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.1);">🔒 Data Consent Compliant</span>
            </div>
        </div>
        <hr style="border: 0; border-top: 1px solid rgba(255,255,255,0.1); margin: 18px 0;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px; font-size: 12.5px;">
            <div>
                © 2026 <b>RetailMind AI</b>. Architected & Maintained by <b>Suraj V. Shewale</b>. All Rights Reserved.
            </div>
            <div>
                <b>Contact Support:</b> <a href="mailto:surajshewale2725@gmail.com" style="color: #60A5FA; text-decoration: none; font-weight: 700;">surajshewale2725@gmail.com</a> | 📱 <b>+91 8261941723</b> | Nashik, Pune & Malegaon, MH, India
            </div>
        </div>
    </footer>
    """, unsafe_allow_html=True)


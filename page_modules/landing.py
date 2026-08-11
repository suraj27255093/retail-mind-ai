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
    """, unsafe_allow_html=True)

    # ── SEO CRAWLABLE DEEP EXPLANATORY CONTENT ─────────────
    st.markdown("""
    <section style="margin-top: 35px; padding: 28px; background: #FFFFFF; border-radius: 20px; border: 1px solid #E2E8F0; color: #1E293B;">
        <h2 style="font-size: 24px; font-weight: 800; color: #0F172A; margin-bottom: 14px;">Next-Generation AI Retail Management for Modern Indian Supermarkets</h2>
        <p style="font-size: 15px; color: #475569; line-height: 1.7; margin-bottom: 16px;">
            <b>RetailMind AI</b> is an enterprise-grade artificial intelligence platform designed specifically for grocery store owners, supermarkets, wholesalers, distributors, and retail chains in India. By combining official Priority 1 Government Mandi market feeds (Agmarknet, eNAM, APMC portals) with machine learning inventory forecasting and natural language Hinglish query support, RetailMind AI eliminates manual price tracking and stockouts.
        </p>
        
        <h3 style="font-size: 20px; font-weight: 700; color: #1E293B; margin-top: 20px; margin-bottom: 10px;">Core Platform Capabilities & Enterprise Modules:</h3>
        <ul style="font-size: 15px; color: #334155; line-height: 1.8; margin-left: 20px; margin-bottom: 20px;">
            <li><b>🌾 Automated APMC Mandi Rates:</b> Real-time daily wholesale purchase rate tracking from Nashik, Pune, and Malegaon APMC markets with 7-day rolling trend analysis.</li>
            <li><b>📦 ML Demand & Inventory Radar:</b> Automated Reorder Point calculation (<i>ROP = d × L + SS</i>) to prevent stockouts and flag expiry items 45 days in advance.</li>
            <li><b>🤖 Hinglish Conversational AI Assistant:</b> Natural language query engine capable of parsing queries like <i>"Sugar ka rate Malegaon mein"</i> or <i>"Atta stock status"</i> into instant structured cards.</li>
            <li><b>🧾 Ultra-Fast Point of Sale (POS):</b> Instant barcode billing, automatic GST calculation, custom discount applying, and 1-click WhatsApp digital receipt generation.</li>
            <li><b>👥 Customer CRM & Loyalty Rewards:</b> Mobile-linked customer tracking with automated loyalty point calculation and purchase history logs.</li>
        </ul>

        <h3 style="font-size: 20px; font-weight: 700; color: #1E293B; margin-top: 22px; margin-bottom: 12px;">Frequently Asked Questions (FAQ)</h3>
        <div style="font-size: 14px; color: #475569; line-height: 1.6;">
            <p><b>Q: How are Mandi prices updated in RetailMind AI?</b><br>
            A: RetailMind AI features an automated synchronization engine connected to Priority 1 Government Agricultural Portals (Agmarknet APMC Feeds & MSAMB). Rates automatically update every morning without manual intervention.</p>

            <p style="margin-top: 12px;"><b>Q: Can RetailMind AI handle multi-store retail chains?</b><br>
            A: Yes, RetailMind AI supports role-based access control (Admin, Store Manager, Staff Account) with unified inventory valuation based on wholesale purchase cost.</p>
        </div>
    </section>
    """, unsafe_allow_html=True)


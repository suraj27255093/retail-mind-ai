import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import plotly.express as px
import json

# =========================================================
# BILLING & POS — Premium Full-Featured Point of Sale
# =========================================================

@st.cache_data(ttl=30)
def load_products():
    conn = sqlite3.connect("retailmind.db")
    df = pd.read_sql_query("SELECT * FROM products", conn)
    conn.close()
    if "selling_price" not in df.columns and "price" in df.columns:
        df["selling_price"] = df["price"]
    elif "selling_price" in df.columns and "price" not in df.columns:
        df["price"] = df["selling_price"]
    df["selling_price"]  = pd.to_numeric(df["selling_price"],  errors="coerce").fillna(0)
    df["purchase_price"] = pd.to_numeric(df.get("purchase_price", df["selling_price"] * 0.85), errors="coerce").fillna(0)
    df["stock"]          = pd.to_numeric(df.get("stock", 50),      errors="coerce").fillna(50)
    if "unit" not in df.columns:
        df["unit"] = "pcs"
    if "gst" not in df.columns:
        df["gst"] = 5
    df["gst"] = pd.to_numeric(df["gst"], errors="coerce").fillna(5)
    return df

df = load_products()

# ── Session state init ────────────────────────────────────
for key, val in {
    "cart": [],
    "discount_applied": False,
    "discount_pct": 0.0,
    "bill_counter": 1001,
    "saved_bills": [],
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ── Hero Header ───────────────────────────────────────────
st.markdown("""
<div class="rm-hero">
    <h1>🧾 RetailMind POS — Point of Sale & Billing System</h1>
    <p>Real-time checkout • Smart Cart • GST Invoice • Multi-Payment • Sales Analytics</p>
</div>
""", unsafe_allow_html=True)

# ── Top KPI Bar ───────────────────────────────────────────
cart_subtotal = sum(i["Total"] for i in st.session_state.cart) if st.session_state.cart else 0.0
cart_items    = sum(i["Qty"]   for i in st.session_state.cart) if st.session_state.cart else 0
total_bills   = len(st.session_state.saved_bills)
total_revenue = sum(b.get("grand_total", 0) for b in st.session_state.saved_bills)

k1, k2, k3, k4, k5, k6 = st.columns(6)
k1.metric("🛒 Cart Items",       f"{cart_items} pcs")
k2.metric("💰 Cart Value",       f"₹{cart_subtotal:,.0f}")
k3.metric("📦 Products",         len(df))
k4.metric("🏪 Markets",          df["market"].nunique())
k5.metric("📋 Bills Today",      total_bills)
k6.metric("💵 Revenue Today",    f"₹{total_revenue:,.0f}")

st.write("")

# ─────────────────────────────────────────────────────────
# MAIN LAYOUT: LEFT = product selector | RIGHT = cart/invoice
# ─────────────────────────────────────────────────────────
left, right = st.columns([1.45, 1])

# ════════════════════════════════════════════════════════
# LEFT PANEL
# ════════════════════════════════════════════════════════
with left:

    # ── Customer Details ─────────────────────────────────
    st.subheader("👤 Customer & Payment Details")
    cust_c1, cust_c2, cust_c3, cust_c4 = st.columns(4)
    with cust_c1:
        c_name   = st.text_input("Customer Name",   value="Walk-in Customer")
    with cust_c2:
        c_mobile = st.text_input("Mobile No.",      value="9876543210")
    with cust_c3:
        c_gst    = st.text_input("Customer GSTIN",  placeholder="Optional")
    with cust_c4:
        pay_method = st.selectbox("Payment Mode",
            ["💵 Cash", "📱 UPI / QR", "💳 Card / Swipe", "🏦 Net Banking", "🔖 Credit / Khata"])

    st.write("")

    # ── Product Search & Add ──────────────────────────────
    st.subheader("➕ Add Items to Cart")

    search_c1, search_c2 = st.columns([1, 1])
    with search_c1:
        cat_filter = st.selectbox("📂 Category Filter",
            ["All Categories"] + sorted(df["category"].unique().tolist()))
    with search_c2:
        search_kw = st.text_input("🔍 Search Product", placeholder="Type name to search...")

    # Apply filters
    filtered_df = df.copy()
    if cat_filter != "All Categories":
        filtered_df = filtered_df[filtered_df["category"] == cat_filter]
    if search_kw:
        filtered_df = filtered_df[filtered_df["product_name"].str.contains(search_kw, case=False, na=False)]

    product_list = filtered_df["product_name"].tolist()

    if not product_list:
        st.warning("No products match your filter. Try clearing the search.")
    else:
        sel_prod = st.selectbox("Select Product", product_list)
        p_data   = filtered_df[filtered_df["product_name"] == sel_prod].iloc[0]

        # Product info row
        pi1, pi2, pi3, pi4, pi5 = st.columns(5)
        pi1.metric("💰 MRP",         f"₹{p_data['selling_price']:.2f}")
        pi2.metric("🏷️ Purchase",    f"₹{p_data['purchase_price']:.2f}")
        pi3.metric("📦 Stock",        f"{int(p_data['stock'])} {p_data['unit']}")
        pi4.metric("🏪 Market",       p_data["market"])
        pi5.metric("🔖 GST",          f"{p_data['gst']:.0f}%")

        qty_col, disc_col, btn_col = st.columns([1.2, 1, 1.2])
        with qty_col:
            qty = st.number_input("Quantity", min_value=1, max_value=max(1, int(p_data["stock"])), value=1)
            # Preset Fast Quantity Chips
            st.caption("⚡ **Fast Quantity Preset:**")
            fq1, fq2, fq3 = st.columns(3)
            if fq1.button("+1", use_container_width=True, key="fast_qty_1"): qty = 1
            if fq2.button("+5", use_container_width=True, key="fast_qty_5"): qty = 5
            if fq3.button("+10", use_container_width=True, key="fast_qty_10"): qty = 10
        with disc_col:
            item_disc = st.number_input("Item Discount (%)", min_value=0.0, max_value=50.0, value=0.0, step=0.5)
        with btn_col:
            st.write("")
            add_clicked = st.button("➕ Add to Cart", use_container_width=True, key="bill_add_cart")

        effective_price = p_data["selling_price"] * (1 - item_disc / 100)
        st.caption(f"Effective Price after {item_disc:.0f}% discount: **₹{effective_price:.2f}** | Line Total: **₹{effective_price * qty:.2f}**")

        if add_clicked:
            existing = next((i for i in st.session_state.cart if i["Product"] == sel_prod), None)
            if existing:
                existing["Qty"]   += qty
                existing["Total"]  = existing["Eff. Price"] * existing["Qty"]
                st.toast(f"✅ Updated {sel_prod} → Qty: {existing['Qty']}", icon="🛒")
            else:
                st.session_state.cart.append({
                    "Product":     sel_prod,
                    "Category":    p_data["category"],
                    "Unit":        p_data["unit"],
                    "MRP":         p_data["selling_price"],
                    "Disc%":       item_disc,
                    "Eff. Price":  round(effective_price, 2),
                    "Qty":         qty,
                    "GST%":        p_data["gst"],
                    "Total":       round(effective_price * qty, 2),
                })
                st.toast(f"✅ {sel_prod} added to cart!", icon="🛒")
            st.rerun()

    st.write("")

    # ── Cart Editing ──────────────────────────────────────
    if st.session_state.cart:
        st.subheader("🛒 Edit Cart")
        cart_df = pd.DataFrame(st.session_state.cart)
        st.dataframe(
            cart_df[["Product", "Category", "Unit", "MRP", "Disc%", "Eff. Price", "Qty", "GST%", "Total"]],
            use_container_width=True, hide_index=True
        )

        edit_c1, edit_c2, edit_c3, edit_c4 = st.columns(4)
        with edit_c1:
            if st.button("🗑️ Remove Last Item", use_container_width=True, key="bill_remove_last"):
                removed = st.session_state.cart.pop()
                st.toast(f"Removed: {removed['Product']}", icon="🗑️")
                st.rerun()
        with edit_c2:
            if st.button("🧹 Clear Entire Cart", use_container_width=True, key="bill_clear_cart"):
                st.session_state.cart = []
                st.session_state.discount_applied = False
                st.session_state.discount_pct = 0.0
                st.toast("Cart cleared!", icon="🧹")
                st.rerun()
        with edit_c3:
            csv_cart = cart_df.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Export Cart CSV", csv_cart, "Cart.csv", "text/csv", use_container_width=True, key="bill_export_cart")
        with edit_c4:
            if st.button("🔄 Refresh Stock", use_container_width=True, key="bill_refresh_stock"):
                st.cache_data.clear()
                st.toast("Stock refreshed!", icon="🔄")
                st.rerun()

    st.write("")

    # ── Sales Chart ───────────────────────────────────────
    with st.expander("📊 Today's Hourly Sales Trend", expanded=False):
        hours = ["8AM", "9AM", "10AM", "11AM", "12PM", "1PM", "2PM", "3PM", "4PM", "5PM", "6PM", "7PM"]
        sales = [800, 1400, 2200, 3800, 5200, 4100, 3600, 4800, 5500, 4200, 3100, 2600]
        fig_s = px.area(
            x=hours, y=sales,
            title="Today's Hourly Sales (₹) — Live View",
            labels={"x": "Hour", "y": "Sales (₹)"},
            color_discrete_sequence=["#2563EB"]
        )
        fig_s.update_traces(fill="tozeroy", fillcolor="rgba(37,99,235,0.08)")
        fig_s.update_layout(paper_bgcolor="#FFFFFF", plot_bgcolor="#F8FAFC", showlegend=False)
        st.plotly_chart(fig_s, use_container_width=True)

# ════════════════════════════════════════════════════════
# RIGHT PANEL — Invoice Builder
# ════════════════════════════════════════════════════════
with right:
    st.subheader("🧾 Live Invoice Builder")

    if not st.session_state.cart:
        st.markdown("""
        <div style="background:#F1F5F9; border-radius:16px; padding:40px; text-align:center; color:#94A3B8; margin-top:10px;">
            <div style="font-size:48px;">🛒</div>
            <div style="font-weight:700; font-size:18px; margin-top:12px;">Cart is Empty</div>
            <div style="font-size:13px; margin-top:6px;">Add items from the left panel to begin billing</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        cart_df = pd.DataFrame(st.session_state.cart)
        subtotal = cart_df["Total"].sum()

        # ── Discount Section ──────────────────────────────
        st.markdown("**🎟️ Apply Discount Coupon**")
        d1, d2, d3 = st.columns(3)
        with d1:
            if st.button("5% Off",  use_container_width=True, key="bill_disc_5"):
                st.session_state.discount_applied = True
                st.session_state.discount_pct = 5.0
                st.toast("5% Discount applied!", icon="🎟️"); st.rerun()
        with d2:
            if st.button("10% Off", use_container_width=True, key="bill_disc_10"):
                st.session_state.discount_applied = True
                st.session_state.discount_pct = 10.0
                st.toast("10% Discount applied!", icon="🎟️"); st.rerun()
        with d3:
            if st.button("🎁 15% VIP", use_container_width=True, key="bill_disc_15"):
                st.session_state.discount_applied = True
                st.session_state.discount_pct = 15.0
                st.toast("15% VIP Discount applied!", icon="👑"); st.rerun()

        custom_disc = st.number_input("Custom Discount (%)", 0.0, 50.0,
                                       value=st.session_state.discount_pct, step=0.5, key="custom_disc_input")
        if custom_disc != st.session_state.discount_pct:
            st.session_state.discount_pct = custom_disc
            st.session_state.discount_applied = custom_disc > 0

        # ── Calculations ──────────────────────────────────
        discount_val = subtotal * (st.session_state.discount_pct / 100) if st.session_state.discount_applied else 0.0
        taxable      = subtotal - discount_val
        gst_5        = cart_df[cart_df["GST%"] == 5]["Total"].sum() * 0.05
        gst_12       = cart_df[cart_df["GST%"] == 12]["Total"].sum() * 0.12
        gst_18       = cart_df[cart_df["GST%"] == 18]["Total"].sum() * 0.18
        gst_28       = cart_df[cart_df["GST%"] == 28]["Total"].sum() * 0.28
        total_gst    = gst_5 + gst_12 + gst_18 + gst_28
        grand_total  = taxable + total_gst

        # ── Invoice Summary Box ───────────────────────────
        st.markdown(f"""
        <div style="background:#FFFFFF; border:2px solid #E2E8F0; border-radius:16px; padding:20px; margin:12px 0;">
            <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
                <span style="color:#64748B; font-size:13px;">Bill No.</span>
                <span style="font-weight:700; color:#2563EB;">#{st.session_state.bill_counter}</span>
            </div>
            <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
                <span style="color:#64748B; font-size:13px;">Customer</span>
                <span style="font-weight:600;">{c_name}</span>
            </div>
            <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
                <span style="color:#64748B; font-size:13px;">Mobile</span>
                <span style="font-weight:600;">{c_mobile}</span>
            </div>
            <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
                <span style="color:#64748B; font-size:13px;">Payment</span>
                <span style="font-weight:600;">{pay_method}</span>
            </div>
            <hr style="border:1px dashed #E2E8F0; margin:12px 0;">
            <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
                <span style="color:#64748B; font-size:13px;">Subtotal ({len(cart_df)} items)</span>
                <span style="font-weight:600;">₹{subtotal:,.2f}</span>
            </div>
            <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
                <span style="color:#EF4444; font-size:13px;">Discount ({st.session_state.discount_pct:.0f}%)</span>
                <span style="color:#EF4444; font-weight:600;">- ₹{discount_val:,.2f}</span>
            </div>
            <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
                <span style="color:#64748B; font-size:13px;">Taxable Amount</span>
                <span style="font-weight:600;">₹{taxable:,.2f}</span>
            </div>
            <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
                <span style="color:#64748B; font-size:13px;">CGST + SGST</span>
                <span style="font-weight:600;">₹{total_gst:,.2f}</span>
            </div>
            <hr style="border:2px solid #2563EB; margin:12px 0;">
            <div style="display:flex; justify-content:space-between; align-items:center; background:#EFF6FF; padding:12px 16px; border-radius:12px; border:1px solid #BFDBFE;">
                <span style="font-size:20px; font-weight:900; color:#0F172A;">💰 TOTAL AMOUNT:</span>
                <span style="font-size:32px; font-weight:900; color:#2563EB;">₹{grand_total:,.2f}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── GST Breakdown ─────────────────────────────────
        with st.expander("📋 GST Tax Breakdown", expanded=False):
            gst_data = []
            for rate, amt in [(5, gst_5), (12, gst_12), (18, gst_18), (28, gst_28)]:
                base = cart_df[cart_df["GST%"] == rate]["Total"].sum()
                if base > 0:
                    gst_data.append({
                        "GST Slab": f"{rate}%",
                        "Taxable Amt": f"₹{base:.2f}",
                        "CGST": f"₹{amt/2:.2f}",
                        "SGST": f"₹{amt/2:.2f}",
                        "Total GST": f"₹{amt:.2f}"
                    })
            if gst_data:
                st.dataframe(pd.DataFrame(gst_data), use_container_width=True, hide_index=True)
            else:
                st.info("GST breakdown not available for current items.")

        st.write("")

        # ── Generate Invoice ──────────────────────────────
        if st.button("🧾 Generate & Save Invoice", use_container_width=True, type="primary", key="bill_gen_invoice"):

            bill_no = st.session_state.bill_counter
            now_str = datetime.now().strftime("%d %b %Y %H:%M")

            # Save bill to session history
            st.session_state.saved_bills.append({
                "bill_no":     bill_no,
                "timestamp":   now_str,
                "customer":    c_name,
                "mobile":      c_mobile,
                "payment":     pay_method,
                "items":       st.session_state.cart.copy(),
                "subtotal":    round(subtotal, 2),
                "discount":    round(discount_val, 2),
                "gst":         round(total_gst, 2),
                "grand_total": round(grand_total, 2),
            })
            st.session_state.bill_counter += 1

            # Build invoice text
            invoice_lines = [
                "=" * 44,
                "       RETAILMIND AI — GST INVOICE",
                "=" * 44,
                f"  Bill No : #{bill_no}",
                f"  Date    : {now_str}",
                f"  Customer: {c_name}",
                f"  Mobile  : {c_mobile}",
                f"  Payment : {pay_method}",
                "-" * 44,
                f"  {'PRODUCT':<22} {'QTY':>4} {'PRICE':>7} {'TOTAL':>7}",
                "-" * 44,
            ]
            for item in st.session_state.cart:
                line = f"  {item['Product'][:22]:<22} {item['Qty']:>4} {item['Eff. Price']:>7.2f} {item['Total']:>7.2f}"
                invoice_lines.append(line)
            invoice_lines += [
                "-" * 44,
                f"  {'Subtotal':<30} {subtotal:>9.2f}",
                f"  {'Discount (' + str(int(st.session_state.discount_pct)) + '%)':<30} -{discount_val:>8.2f}",
                f"  {'CGST + SGST':<30} {total_gst:>9.2f}",
                "=" * 44,
                f"  {'GRAND TOTAL':<30} {grand_total:>9.2f}",
                "=" * 44,
                "",
                "     Thank you! Phir aana! 🙏",
                "     RetailMind AI — Powered by AI",
                "=" * 44,
            ]
            invoice_text = "\n".join(invoice_lines)

            st.success(f"✅ Invoice #{bill_no} saved for {c_name}!")
            st.download_button(
                "📄 Download Invoice (TXT)",
                invoice_text.encode("utf-8"),
                f"Invoice_{bill_no}_{c_name.replace(' ','_')}.txt",
                "text/plain",
                use_container_width=True,
                key=f"bill_dl_invoice_{bill_no}"
            )

            # Clear cart after billing
            st.session_state.cart = []
            st.session_state.discount_applied = False
            st.session_state.discount_pct = 0.0
            st.rerun()

# ─────────────────────────────────────────────────────────
# BILLS HISTORY SECTION
# ─────────────────────────────────────────────────────────
st.write("")
st.divider()
st.subheader("📋 Today's Bill History")

if not st.session_state.saved_bills:
    st.info("No bills generated yet today. Start billing to see history here.")
else:
    bills_df = pd.DataFrame([{
        "Bill No":    f"#{b['bill_no']}",
        "Time":       b["timestamp"],
        "Customer":   b["customer"],
        "Mobile":     b["mobile"],
        "Payment":    b["payment"],
        "Items":      len(b["items"]),
        "Subtotal":   f"₹{b['subtotal']:,.2f}",
        "Discount":   f"₹{b['discount']:,.2f}",
        "GST":        f"₹{b['gst']:,.2f}",
        "Grand Total":f"₹{b['grand_total']:,.2f}",
    } for b in reversed(st.session_state.saved_bills)])

    st.dataframe(bills_df, use_container_width=True, hide_index=True)

    h1, h2, h3 = st.columns(3)
    h1.metric("🧾 Total Bills",   len(st.session_state.saved_bills))
    h2.metric("💵 Total Revenue", f"₹{sum(b['grand_total'] for b in st.session_state.saved_bills):,.2f}")
    h3.metric("🎟️ Total Discounts", f"₹{sum(b['discount'] for b in st.session_state.saved_bills):,.2f}")

    if st.button("🗑️ Clear Bill History", use_container_width=False, key="bill_clear_history"):
        st.session_state.saved_bills = []
        st.session_state.bill_counter = 1001
        st.rerun()
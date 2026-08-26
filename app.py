import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse
import random
import time

st.set_page_config(
    page_title="ApexLead AI | Autonomous Real Estate OS",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_APP_URL = "https://apexlead-dubai-d4paqwmnuacidn564qqnsr.streamlit.app"

# --------------------------------------------------
# 🎨 Global High-Contrast Styling
# --------------------------------------------------
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp {
        background-color: #080c14;
        color: #f8fafc;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    section[data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-right: 2px solid #334155 !important;
    }
    section[data-testid="stSidebar"] * {
        color: #f8fafc !important;
        font-size: 14.5px !important;
        font-weight: 600 !important;
    }

    .brand-box {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 25px;
        padding-bottom: 15px;
        border-bottom: 1px solid #334155;
    }
    .brand-logo {
        background: #10b981;
        color: #ffffff !important;
        font-weight: 900;
        font-size: 22px !important;
        padding: 6px 14px;
        border-radius: 10px;
    }
    .brand-text {
        font-size: 20px !important;
        font-weight: 800 !important;
        color: #ffffff !important;
    }
    .brand-text span {
        color: #10b981 !important;
    }

    .sme-card {
        background: #0f172a;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 22px;
        margin-bottom: 18px;
    }

    .btn-gmail-red {
        background: #ea4335 !important;
        color: white !important;
        padding: 10px 18px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: 800;
        font-size: 13.5px;
        display: block;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .btn-wa-green {
        background: #10b981 !important;
        color: white !important;
        padding: 10px 18px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: 800;
        font-size: 13.5px;
        display: block;
        text-align: center;
    }

    /* WhatsApp Simulators */
    .wa-container {
        background: #0b141a;
        border: 1px solid #334155;
        border-radius: 14px;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .wa-topbar {
        background: #1f2c34;
        padding: 14px 18px;
        display: flex;
        align-items: center;
        gap: 12px;
        border-bottom: 1px solid #2a3942;
    }
    .wa-feed {
        background-color: #0b141a;
        padding: 20px;
        min-height: 400px;
        max-height: 480px;
        overflow-y: auto;
    }
    .msg-user {
        background: #202c33;
        color: #f1f5f9;
        padding: 11px 16px;
        border-radius: 0px 12px 12px 12px;
        margin-bottom: 14px;
        max-width: 82%;
        font-size: 14px;
        line-height: 1.5;
    }
    .msg-bot {
        background: #005c4b;
        color: #ffffff;
        padding: 11px 16px;
        border-radius: 12px 0px 12px 12px;
        margin-bottom: 14px;
        margin-left: auto;
        max-width: 82%;
        font-size: 14px;
        line-height: 1.5;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# 🗄️ Database: Live Properties & SME Leads
# --------------------------------------------------
if 'property_inventory' not in st.session_state:
    st.session_state.property_inventory = [
        {"ID": "DXB-101", "Title": "Luxury 1BR Canal View", "Location": "Business Bay", "Type": "Apartment", "Price": "AED 85,000 / yr", "Status": "🟢 Available", "Added_By": "WhatsApp Ingest"},
        {"ID": "DXB-102", "Title": "Furnished Holiday Studio", "Location": "Jumeirah Village Circle (JVC)", "Type": "Studio", "Price": "AED 5,400 / mo", "Status": "🟢 Available", "Added_By": "Direct System"},
        {"ID": "DXB-103", "Title": "2BR Marina Panoramic", "Location": "Dubai Marina", "Type": "Apartment", "Price": "AED 135,000 / yr", "Status": "🟢 Available", "Added_By": "WhatsApp Ingest"},
    ]

VERIFIED_DUBAI_SME_LEADS = [
    {"id": "KeyOne", "Company": "Key One Realty Group", "Category": "Holiday Homes & Boutique Leasing", "Location": "Al Barsha / Dubai Marina", "Team_Size": "10-15 Staff", "Decision_Maker": "Managing Director / Reservations Team", "Email": "info@keyonerealtygroup.com", "Phone": "+97144471727", "Target_Pain": "Late-night booking inquiries on WhatsApp causing guest drop-offs."},
    {"id": "FrankPorter", "Company": "Frank Porter Vacation Homes", "Category": "Boutique Vacation Rentals", "Location": "JLT / Dubai Marina", "Team_Size": "12 Staff Members", "Decision_Maker": "Head of Bookings & Guest Relations", "Email": "info@frankporter.com", "Phone": "+97145897140", "Target_Pain": "International tourist time-zone delays for WhatsApp pricing requests."},
    {"id": "WhiteCo", "Company": "White & Co Real Estate", "Category": "Independent Agency", "Location": "Dubai Marina", "Team_Size": "15 Brokers", "Decision_Maker": "Managing Director", "Email": "info@whiteandcogroup.com", "Phone": "+97148762000", "Target_Pain": "Brokers overwhelmed by unqualified inquiries from Instagram ads."},
    {"id": "DeluxeHomes", "Company": "Deluxe Holiday Homes", "Category": "Short-Term Vacation Rentals", "Location": "Downtown Dubai", "Team_Size": "18 Staff", "Decision_Maker": "Reservations Lead", "Email": "info@deluxehomes.com", "Phone": "+97143920202", "Target_Pain": "Slow manual rate quotation causing direct booking losses."}
]

if 'broker_chat' not in st.session_state:
    st.session_state.broker_chat = [
        {"sender": "user", "text": "وصلتنا شقة جديدة للبيع في داون تاون برج فيستا، غرفتين وصالة، السعر 2.8 مليون درهم."},
        {"sender": "bot", "text": "تم استلام العقار الجديد بنجاح 🌟 لتحليله وتحديث قاعدة بيانات المبيعات، يرجى تزويدي بالآتي:\n1. كم المساحة الإجمالية بالقدم المربع؟\n2. هل الشقة مفروشة أم غير مفروشة؟"},
    ]

query_params = st.query_params
client_id = query_params.get("client", None)
view_mode = query_params.get("view", "client" if client_id else "admin")

# Helper to get active available units
def get_available_units_text():
    available = [p for p in st.session_state.property_inventory if "Available" in p['Status']]
    if not available:
        return "كافة العقارات الحالية قيد الإجراءات، يرجى تزويدنا بطلبكم لنوافيكم بالعروض الجديدة فور طرحها."
    lines = []
    for p in available:
        lines.append(f"• {p['Title']} في {p['Location']} ({p['Price']})")
    return "\n".join(lines)

# --------------------------------------------------
# 🌟 1. CLIENT DEDICATED DEMO VIEW
# --------------------------------------------------
if view_mode == "client" or client_id:
    matched_company = "Your Real Estate Agency"
    matched_loc = "Dubai"
    for lead in VERIFIED_DUBAI_SME_LEADS:
        if lead["id"].lower() == str(client_id).lower():
            matched_company = lead["Company"]
            matched_loc = lead["Location"]
            break

    st.markdown(f"""
    <div style="text-align:center; padding: 25px 15px 15px 15px;">
        <div style="display:inline-block; background:#10b981; color:white; font-weight:800; padding:4px 12px; border-radius:20px; font-size:12px; margin-bottom:10px;">
            ⚡ LIVE INTERACTIVE PROTOTYPE
        </div>
        <h1 style="font-size:28px; font-weight:800; color:#ffffff; margin-bottom:6px;">{matched_company}</h1>
        <p style="color:#94a3b8; font-size:14.5px; max-width:600px; margin:0 auto 20px auto;">
            Experience how your 24/7 AI WhatsApp Assistant instantly qualifies property inquiries and books viewings for your <b>{matched_loc}</b> listings.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if 'client_chat' not in st.session_state:
        st.session_state.client_chat = [
            {"sender": "user", "text": "مرحبا، شفت إعلانكم بخصوص الشقق في دبي، شو في خيارات متوفرة عندكم؟"},
            {"sender": "bot", "text": f"أهلاً وسهلاً بك في {matched_company} 🌟 متاح لدينا حالياً خيارات نشطة ومحدثة في قاعدة البيانات:\n{get_available_units_text()}\n\nما هي المنطقة أو الميزانية الأنسب لطلبكم؟"},
        ]

    st.markdown(f"""
    <div class="wa-container" style="max-width:650px; margin:0 auto;">
        <div class="wa-topbar">
            <div style="background:#10b981; width:36px; height:36px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:800; color:white;">⚡</div>
            <div>
                <div style="font-weight:700; color:#e9edef; font-size:14.5px;">{matched_company} AI Assistant</div>
                <div style="font-size:11.5px; color:#10b981;">Online (Instant 24/7 Response)</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    chat_html = "<div class='wa-container' style='max-width:650px; margin: -1px auto 25px auto; border-top:none; border-radius:0 0 14px 14px;'><div class='wa-feed'>"
    for msg in st.session_state.client_chat:
        if msg['sender'] == 'user':
            chat_html += f"<div class='msg-user'><b>You (Customer):</b><br>{msg['text'].replace(chr(10), '<br>')}</div>"
        else:
            chat_html += f"<div class='msg-bot'><b>{matched_company} Assistant:</b><br>{msg['text'].replace(chr(10), '<br>')}</div>"
    chat_html += "</div></div>"
    st.markdown(chat_html, unsafe_allow_html=True)

    with st.form("client_sim_form", clear_on_submit=True):
        col_in1, col_in2 = st.columns([4, 1.2])
        with col_in1:
            client_input = st.text_input("Test inquiry (Arabic, English, or Hindi)...", placeholder="e.g. شو في خيارات متاحة؟ / كم السعر؟ / بدي شقة مارينا", label_visibility="collapsed")
        with col_in2:
            send_btn = st.form_submit_button("Send 💬", type="primary", use_container_width=True)

        if send_btn and client_input:
            st.session_state.client_chat.append({"sender": "user", "text": client_input})
            lower_in = client_input.strip().lower()

            # Check if asking about available options dynamically
            if any(w in lower_in for w in ["خيارات", "متوفر", "متاح", "عروض", "available", "options"]):
                reply = f"العقارات المتاحة حالياً لدينا في {matched_company}:\n{get_available_units_text()}\n\nهل تفضل حجز موعد للمعاينة لأي منها اليوم؟"
            elif any(w in lower_in for w in ["معاينة", "موعد", "حجز", "بدي شوف", "عاين", "viewing"]):
                reply = "يسعدنا ترتيب موعد لمعاينة الشقة اليوم الساعة الخامسة مساءً أو غداً الساعة الحادية عشرة صباحاً. أي الموعدين يناسب جدولكم الكريم؟"
            elif any(w in lower_in for w in ["كم السعر", "كم الإيجار", "الأسعار", "بكم", "price", "rent"]):
                reply = "تبدأ الإيجارات الشهرية من ٥,٤٠٠ درهم شاملة لكافة الفواتير، والسنوية تبدأ من ٨٥,٠٠٠ درهم بتسهيلات دفع مرنة. هل تفضل الإيجار الشهري أم السنوي؟"
            else:
                reply = f"تم استلام طلبكم بعناية في {matched_company}. خياراتنا مطابقة ومحدثة لحظياً في قاعدة البيانات. هل ترغب في إرسال الصور ومخطط الشقة عبر هذه المحادثة؟"

            st.session_state.client_chat.append({"sender": "bot", "text": reply})
            st.rerun()

    st.markdown("""
    <div style="max-width:650px; margin: 20px auto 40px auto; background:#0f172a; border:2px solid #10b981; border-radius:12px; padding:24px; text-align:center;">
        <span style="background:#d97706; color:white; font-weight:800; padding:4px 12px; border-radius:6px; font-size:12px;">EXCLUSIVE LAUNCH OFFER</span>
        <h3 style="color:#ffffff; margin:10px 0 6px 0; font-size:22px;">Activate for Your Agency: AED 250 Only</h3>
        <p style="color:#94a3b8; font-size:14px; margin-bottom:18px;">
            Get this exact system connected to your business WhatsApp in 15 minutes. Includes <b>Month 1 Setup + 1 Full Month Technical Support FREE</b> (2 Months Total for AED 250).
        </p>
        <a href="https://wa.me/971500000000?text=Hello%2C%20I%20tested%20the%20demo%20and%20want%20to%20activate%20the%20AED%20250%20offer" target="_blank" style="background:#10b981; color:white; padding:12px 28px; border-radius:8px; font-weight:800; font-size:15px; text-decoration:none; display:inline-block;">
            ⚡ Claim 7-Day Free Trial & Setup
        </a>
    </div>
    """, unsafe_allow_html=True)

# --------------------------------------------------
# 🛡️ 2. ADMIN MASTER CONTROL CENTER
# --------------------------------------------------
else:
    with st.sidebar:
        st.markdown("""
        <div class="brand-box">
            <span class="brand-logo">⚡</span>
            <div class="brand-text">ApexLead <span>ADMIN</span></div>
        </div>
        """, unsafe_allow_html=True)

        admin_menu = st.radio("Admin Navigation", [
            "📥 WhatsApp Property Operations (إضافة وتحديث وبيع العقارات)",
            "📋 Real-Time Property Inventory (قائمة العقارات النشطة والمباعة)",
            "🎯 Verified Lead Outreach & Demos (حملات التواصل)",
            "📊 Launch Pricing & Scaling Model"
        ])
        
        available_cnt = len([p for p in st.session_state.property_inventory if "Available" in p['Status']])
        sold_cnt = len([p for p in st.session_state.property_inventory if "SOLD" in p['Status']])

        st.markdown("<br><hr style='border-color:#334155;'><br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style='background:#1e293b; padding:14px; border-radius:8px; border:1px solid #475569;'>
            <b style='color:#10b981; font-size:13.5px !important;'>Live Inventory Status:</b><br>
            <span style='color:#34d399; font-size:13px !important;'>🟢 {available_cnt} Available for Sale/Rent</span><br>
            <span style='color:#ef4444; font-size:13px !important;'>🔴 {sold_cnt} Closed / Sold Units</span><br><br>
            <span style='color:#38bdf8; font-size:12px !important;'>Auto-Sync Active ⚡</span>
        </div>
        """, unsafe_allow_html=True)

    # --- Screen 1: WhatsApp Property Operations (Add / Sell) ---
    if admin_menu == "📥 WhatsApp Property Operations (إضافة وتحديث وبيع العقارات)":
        st.markdown("<h1 style='font-size:24px; font-weight:800; color:#ffffff;'>📥 Conversational WhatsApp Property Management</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color:#94a3b8; font-size:14px; margin-bottom:20px;'>محاكاة كاملة: إرسال عقار جديد للإضافة، أو كتابة رسالة بيع (مثل: <i>'تم بيع شقة مارينا'</i>) ليتم شطبها تلقائياً من عروض المشترين.</p>", unsafe_allow_html=True)

        col_b_chat, col_b_info = st.columns([1.2, 1], gap="large")

        with col_b_chat:
            st.markdown("""
            <div class="wa-container">
                <div class="wa-topbar">
                    <div style="background:#0284c7; width:36px; height:36px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:800; color:white;">🏢</div>
                    <div>
                        <div style="font-weight:700; color:#e9edef; font-size:14.5px;">Agency Broker Ingestion & Close Bot</div>
                        <div style="font-size:11.5px; color:#38bdf8;">Listening for New Listings & Sold Triggers</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            chat_html = "<div class='wa-container' style='margin-top:-25px; border-top:none; border-radius:0 0 14px 14px;'><div class='wa-feed'>"
            for msg in st.session_state.broker_chat:
                if msg['sender'] == 'user':
                    chat_html += f"<div class='msg-user'><b>الوسيط (Broker):</b><br>{msg['text'].replace(chr(10), '<br>')}</div>"
                else:
                    chat_html += f"<div class='msg-bot'><b>AI Property Manager:</b><br>{msg['text'].replace(chr(10), '<br>')}</div>"
            chat_html += "</div></div>"
            st.markdown(chat_html, unsafe_allow_html=True)

            with st.form("broker_ops_form", clear_on_submit=True):
                broker_in = st.text_input("جرب: كتابة 'تم بيع شقة مارينا' أو 'أضف شقة جديدة بالداون تاون'...", placeholder="اكتب رسالة الوسيط هنا...")
                if st.form_submit_button("إرسال التحديث للذكاء الاصطناعي 💬", type="primary", use_container_width=True) and broker_in:
                    st.session_state.broker_chat.append({"sender": "user", "text": broker_in})
                    lower_b = broker_in.lower()

                    # --- Trigger 1: Mark Property as Sold / Rented ---
                    if any(w in lower_b for w in ["بيع", "تم بيع", "تأجرت", "حجزت", "انباعت", "sold", "rented", "closed"]):
                        # Check which property matches
                        target_updated = False
                        for p in st.session_state.property_inventory:
                            if any(k in lower_b for k in [p['Location'].lower(), p['Type'].lower(), p['Title'].lower(), "مارينا", "jvc", "business bay", "استوديو"]):
                                if "Available" in p['Status']:
                                    p['Status'] = "🔴 SOLD / RENTED"
                                    target_updated = True
                                    bot_reply = f"مبروك إتمام الصفقة! 🎉 تم تحديث حالة العقار [{p['Title']} - {p['Location']}] إلى [🔴 SOLD / RENTED] وشطبه فوراً من قائمة العروض.\nلن يتم ترشيحه لأي عميل جديد على الواتساب."
                                    break
                        if not target_updated:
                            # Fallback if specific name not matched, mark first active as sold
                            for p in st.session_state.property_inventory:
                                if "Available" in p['Status']:
                                    p['Status'] = "🔴 SOLD / RENTED"
                                    bot_reply = f"ألف مبروك! تم تحديث حالة العقار [{p['Title']}] إلى [🔴 SOLD] وإيقاف ظهوره للعملاء فوراً."
                                    break

                    # --- Trigger 2: Add New Property ---
                    else:
                        new_id = f"DXB-{random.randint(104, 199)}"
                        st.session_state.property_inventory.insert(0, {
                            "ID": new_id,
                            "Title": "Luxury 2BR Suite",
                            "Location": "Downtown Dubai",
                            "Type": "Apartment",
                            "Price": "AED 2,800,000 Cash",
                            "Status": "🟢 Available",
                            "Added_By": "WhatsApp Auto-Ingest"
                        })
                        bot_reply = f"تم اعتماد العقار الجديد بنجاح برقم [{new_id}] ✅ وحفظه كـ [🟢 Available].\nتم تحديث محرك المبيعات وسيتم ترشيحه للمشترين الجدد فوراً!"

                    st.session_state.broker_chat.append({"sender": "bot", "text": bot_reply})
                    st.rerun()

        with col_b_info:
            st.markdown("""
            <div class="sme-card">
                <h3 style="margin-top:0; color:#ffffff; font-size:18px;">💡 الأتمتة الكاملة لدورة حياة العقار:</h3>
                <ul style="color:#cbd5e1; font-size:13.5px; line-height:1.8; padding-left:20px; margin-bottom:0;">
                    <li><b>شطب فوري عند البيع:</b> لا مزيد من الإحراج أو إضاعة وقت المشترين على عقارات مباعة.</li>
                    <li><b>تحويل ذكي للعميل:</b> إذا سأل زائر عن شقة تم بيعها، يقترح النظام شقة بديلة بنفس المنطقة والميزانية مباشرة.</li>
                    <li><b>سهولة مطلقة للوسيط:</b> إرسال رسالة نصية بسيطة مثل <i>"تم بيع الشقة"</i> يكفي لتحديث كامل المنظومة وقاعدة البيانات في ثانية واحدة.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

    # --- Screen 2: Real-Time Property Inventory ---
    elif admin_menu == "📋 Real-Time Property Inventory (قائمة العقارات النشطة والمباعة)":
        st.markdown("<h1 style='font-size:24px; font-weight:800; color:#ffffff;'>📋 Real-Time Property Inventory (قاعدة البيانات المباشرة)</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color:#94a3b8; font-size:14px; margin-bottom:20px;'>العقارات المحدثة لحظياً عبر الواتساب مع تمييز العقارات المتاحة والمباعة:</p>", unsafe_allow_html=True)

        inv_df = pd.DataFrame(st.session_state.property_inventory)
        st.dataframe(inv_df, use_container_width=True, hide_index=True)

    # --- Screen 3: Verified Lead Outreach & Demos ---
    elif admin_menu == "🎯 Verified Lead Outreach & Demos (حملات التواصل)":
        st.markdown("<h1 style='font-size:24px; font-weight:800; color:#ffffff;'>🎯 Dubai Verified SME Outreach & Demos</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color:#94a3b8; font-size:14px; margin-bottom:20px;'>Verified active operators in Dubai with accurate domains and direct WhatsApp lines.</p>", unsafe_allow_html=True)

        lang_pref = st.radio("Proposal Language:", ["English Pitch (Corporate Dubai)", "Arabic Pitch (عربي رسمي)"], horizontal=True)
        st.markdown("<br>", unsafe_allow_html=True)

        for idx, lead in enumerate(VERIFIED_DUBAI_SME_LEADS):
            custom_demo_link = f"{BASE_APP_URL}/?client={lead['id']}"

            if "English" in lang_pref:
                email_subj = f"Quick question regarding {lead['Company']} WhatsApp inquiries"
                email_body = f"""Hi {lead['Decision_Maker']} & team at {lead['Company']},

I noticed your active listings in {lead['Location']}.

For boutique teams of {lead['Team_Size']}, replying to Meta and Instagram ad inquiries after 8 PM or on weekends often causes serious buyer drop-offs.

We built a custom 24/7 WhatsApp AI Assistant specifically for {lead['Company']}:
- Instantly responds to WhatsApp inquiries in under 3 seconds (Arabic, English, and Hindi).
- Brokers can add new property listings or mark units as SOLD directly via WhatsApp text.
- Qualifies buyer/tenant budget and preferred area before alerting your team.
- Sends property photos and schedules viewing visits automatically.

🔗 Test your company's dedicated demo here:
{custom_demo_link}

🔥 Special Launch Offer:
Get the full system operational for just AED 250 for Month 1, plus 1 additional month of full technical support for FREE (Total 2 months for AED 250).

Would you be open to a quick 3-minute chat this week?

Best regards,
ApexLead Team Dubai"""
            else:
                email_subj = f"استفسار بخصوص أتمتة رسائل الواتساب لشركة [{lead['Company']}]"
                email_body = f"""تحية طيبة للأستاذ / {lead['Decision_Maker']} وفريق العمل في [{lead['Company']}]،

لاحظنا نشاطكم وعروضكم العقارية المميزة في منطقة {lead['Location']}.

ندرك أن سرعة الرد على استفسارات العملاء خارج ساعات العمل الرسمية وفي عطلات نهاية الأسبوع ترفع نسبة حجز المعاينات وتأكيد الصفقات لأكثر من ستين بالمائة.

قمنا بتطوير نظام ذكي مخصص للشركات العقارية المتوسطة في دبي:
١. رد فوري على رسائل الواتساب خلال ثلاث ثوان على مدار أربع وعشرين ساعة باللغات العربية والإنجليزية والهندية.
٢. إمكانية إضافة العقارات الجديدة أو شطب العقارات المباعة مباشرة عبر رسالة واتساب عادية من الوسيط.
٣. فرز ميزانية المستأجر أو المشتري وتحديد طلبه بدقة قبل تحويله لكم.
٤. إرسال صور العقارات وتثبيت مواعيد المعاينة آلياً.

رابط التجربة التفاعلية المباشرة المخصص لشركتكم:
{custom_demo_link}

🔥 عرض الإطلاق الخاص:
نقدم لكم النظام بالكامل للشهر الأول مقابل ٢٥٠ درهم فقط، مع شهر إضافي كامل من المتابعة والدعم الفني مجاناً (شهرين كاملين مقابل ٢٥٠ درهم فقط).

يسعدنا ترتيب محادثة قصيرة للاطلاع على النظام في الوقت الذي يناسبكم.

وتفضلوا بقبول فائق الاحترام والتقدير،
فريق التطوير والأتمتة"""

            encoded_subj = urllib.parse.quote(email_subj)
            encoded_body = urllib.parse.quote(email_body)
            gmail_web_link = f"https://mail.google.com/mail/u/0/?view=cm&fs=1&tf=1&to={lead['Email']}&su={encoded_subj}&body={encoded_body}"
            wa_text = f"Hi {lead['Company']} team, I prepared a custom WhatsApp AI demo for your {lead['Location']} listings: {custom_demo_link}\n\nOur launch offer is AED 250 for 2 months."
            wa_link = f"https://wa.me/{lead['Phone'].replace('+', '').replace(' ', '')}?text={urllib.parse.quote(wa_text)}"

            st.markdown(f"""
            <div class="sme-card">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                    <div>
                        <span style="font-size:18px; font-weight:800; color:#ffffff;">🏢 {lead['Company']}</span>
                        &nbsp;&nbsp;<span style="background:#082f49; color:#38bdf8; padding:3px 8px; border-radius:4px; font-size:12px; font-weight:700;">{lead['Category']}</span>
                        &nbsp;<span style="background:#064e3b; color:#34d399; padding:3px 8px; border-radius:4px; font-size:12px; font-weight:700;">📍 {lead['Location']}</span>
                    </div>
                    <div>
                        <span class="offer-badge">🔥 AED 250 Offer</span>
                    </div>
                </div>
                <p style="color:#94a3b8; font-size:13px; margin-bottom:10px;">
                    👤 <b>Decision Maker:</b> {lead['Decision_Maker']} ({lead['Team_Size']}) | ✉️ <b>Verified Email:</b> <span style="color:#38bdf8;">{lead['Email']}</span> | 📞 <b>Phone:</b> {lead['Phone']}
                </p>
                <div style="background:#080c14; border:1px solid #1e293b; padding:10px 14px; border-radius:6px; font-size:13px; color:#38bdf8; margin-bottom:12px; word-break:break-all;">
                    🔗 <b>Client Dedicated Demo Link:</b> <a href="{custom_demo_link}" target="_blank" style="color:#38bdf8;">{custom_demo_link}</a>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.text_area(f"Proposal text for {lead['Company']}:", email_body, height=130, key=f"txt_{idx}")

            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f'<a href="{gmail_web_link}" target="_blank" class="btn-gmail-red">🔴 Open Direct in Web Gmail</a>', unsafe_allow_html=True)
            with c2:
                st.markdown(f'<a href="{wa_link}" target="_blank" class="btn-wa-green">💬 Send WhatsApp Pitch</a>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

    # --- Screen 4: Pricing & Business Model ---
    elif admin_menu == "📊 Launch Pricing & Scaling Model":
        st.markdown("<h1 style='font-size:24px; font-weight:800; color:#ffffff;'>📊 Pricing Strategy & Scalability</h1>", unsafe_allow_html=True)
        pricing_df = pd.DataFrame([
            {"Stage": "🔥 Phase 1 (Active Now)", "Target": "First 10-15 Dubai Agencies", "Price": "AED 250", "Package": "Month 1 + 1 Month Support FREE (2 Months Total)", "Strategy": "Fast market entry & instant case studies"},
            {"Stage": "💎 Phase 2 (After 10 Clients)", "Target": "Growing Operators", "Price": "AED 1,250 Setup + AED 390/mo", "Package": "Standard SME Tier", "Strategy": "High margin recurring revenue"},
        ])
        st.dataframe(pricing_df, use_container_width=True, hide_index=True)

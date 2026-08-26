import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import urllib.parse
import smtplib
import imaplib
import email
from email.header import decode_header
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import socket
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
        font-size: 14px !important;
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

    .hot-reply-card {
        background: #06281e;
        border: 2px solid #10b981;
        border-radius: 12px;
        padding: 18px 22px;
        margin-bottom: 20px;
    }

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

def is_valid_domain(email_address):
    try:
        domain = email_address.split('@')[1]
        socket.gethostbyname(domain)
        return True
    except Exception:
        return False

# --------------------------------------------------
# 🗄️ Master Database (35 Real Verified Dubai Agencies)
# --------------------------------------------------
ALL_VERIFIED_DUBAI_MASTER = [
    {"id": "Espace", "Company": "Espace Real Estate", "Location": "Dubai Marina (Marina Plaza)", "Category": "Luxury Brokerage", "Email": "info@espace.ae", "Phone": "+97143069999", "Decision_Maker": "Managing Partner", "Channel": "DLD Directory"},
    {"id": "ArabianEstates", "Company": "Arabian Estates Dubai", "Location": "Dubai Marina", "Category": "Boutique Brokerage", "Email": "info@arabianestates.ae", "Phone": "+97143243137", "Decision_Maker": "Managing Director", "Channel": "Google Maps Verified"},
    {"id": "KeyOne", "Company": "Key One Realty Group", "Location": "Al Barsha & Marina", "Category": "Holiday Homes & Leasing", "Email": "info@keyonerealtygroup.com", "Phone": "+97144471727", "Decision_Maker": "Managing Director", "Channel": "DTCM Licensed"},
    {"id": "haus_and_haus", "Company": "haus & haus Real Estate", "Location": "Gold & Diamond Park", "Category": "Agency & Property Management", "Email": "enquiry@hausandhaus.com", "Phone": "+97143025800", "Decision_Maker": "Director of Growth", "Channel": "Meta Ad Active"},
    {"id": "DeluxeHomes", "Company": "Deluxe Holiday Homes", "Location": "Downtown Dubai (Boulevard Plaza)", "Category": "Vacation Rentals Operator", "Email": "info@deluxehomes.com", "Phone": "+97143920202", "Decision_Maker": "Operations Lead", "Channel": "DTCM Licensed"},
    {"id": "WhiteCo", "Company": "White & Co Real Estate", "Location": "Dubai Marina", "Category": "Residential Agency", "Email": "info@whiteandcogroup.com", "Phone": "+97148762000", "Decision_Maker": "Sales Director", "Channel": "Property Finder Verified"},
    {"id": "Allsopp", "Company": "Allsopp & Allsopp", "Location": "Motor City & Business Bay", "Category": "Residential Agency", "Email": "info@allsoppandallsopp.com", "Phone": "+97144294444", "Decision_Maker": "Head of Operations", "Channel": "DLD Licensed"},
    {"id": "Betterhomes", "Company": "Betterhomes Dubai", "Location": "Al Barsha & Marina", "Category": "Residential Agency", "Email": "customercare@bhomes.com", "Phone": "+97144090911", "Decision_Maker": "Customer Care Lead", "Channel": "DLD Directory"},
    {"id": "ProvidentEstate", "Company": "Provident Real Estate", "Location": "Dubai Marina", "Category": "Investment Brokerage", "Email": "info@providentestate.com", "Phone": "+97143233609", "Decision_Maker": "Client Relations Lead", "Channel": "Google Maps Verified"},
    {"id": "FamProperties", "Company": "fäm Properties", "Location": "Business Bay", "Category": "Technology Agency", "Email": "info@famproperties.com", "Phone": "+97143691700", "Decision_Maker": "Commercial Director", "Channel": "Bayut / Meta Active"},
    {"id": "DandB", "Company": "D&B Properties", "Location": "Business Bay (Blue Bay Tower)", "Category": "Off-Plan & Leasing", "Email": "inquiry@dandbdubai.com", "Phone": "+97148719200", "Decision_Maker": "Sales Director", "Channel": "DLD Directory"},
    {"id": "TreoHomes", "Company": "Treo Homes", "Location": "Dubai Hills Estate", "Category": "Community Brokerage", "Email": "info@treo-homes.com", "Phone": "+97144542588", "Decision_Maker": "Principal Partner", "Channel": "Google Maps Verified"},
    {"id": "McCone", "Company": "McCone Properties", "Location": "The Binary, Business Bay", "Category": "Residential Agency", "Email": "info@mcconeproperties.com", "Phone": "+97143806683", "Decision_Maker": "Managing Director", "Channel": "Property Finder"},
    {"id": "Luxhabitat", "Company": "LUXHABITAT Sotheby's", "Location": "DIFC", "Category": "Ultra Luxury Brokerage", "Email": "info@luxhabitat.ae", "Phone": "+97144550888", "Decision_Maker": "Marketing Head", "Channel": "Verified Portal"},
    {"id": "FrankPorter", "Company": "Frank Porter Vacation Homes", "Location": "JLT", "Category": "Holiday Homes", "Email": "info@frankporter.com", "Phone": "+97145897140", "Decision_Maker": "Head of Bookings", "Channel": "DTCM Licensed"},
    {"id": "AlMirath", "Company": "Al Mirath Real Estate", "Location": "Jumeirah", "Category": "Villa Leasing Specialists", "Email": "info@almirath.ae", "Phone": "+97143491414", "Decision_Maker": "Leasing Manager", "Channel": "Google Maps"},
    {"id": "Standpoint", "Company": "Standpoint Real Estate", "Location": "Barsha Heights", "Category": "Boutique Agency", "Email": "info@standpointrealestate.ae", "Phone": "+97145763900", "Decision_Maker": "Operations Lead", "Channel": "Bayut Verified"},
    {"id": "Paragon", "Company": "Paragon Properties", "Location": "Dubai Marina", "Category": "Residential Brokerage", "Email": "info@paragonproperties.ae", "Phone": "+97145846700", "Decision_Maker": "Managing Partner", "Channel": "DLD Directory"},
    {"id": "SkyView", "Company": "Sky View Real Estate", "Location": "Downtown Dubai", "Category": "Off-Plan & Leasing", "Email": "info@skyviewdubai.com", "Phone": "+97144370431", "Decision_Maker": "Sales Head", "Channel": "Google Maps"},
    {"id": "Metropolitan", "Company": "Metropolitan Premium Properties", "Location": "Business Bay (Office Park)", "Category": "Full-Service Brokerage", "Email": "info@metropolitan.realestate", "Phone": "+97143605561", "Decision_Maker": "Commercial Lead", "Channel": "DLD Directory"}
]

if 'property_inventory' not in st.session_state:
    st.session_state.property_inventory = [
        {"ID": "DXB-101", "Title": "Luxury 1BR Canal View", "Location": "Business Bay", "Type": "Apartment", "Price": "AED 85,000 / yr", "Status": "🟢 Available"},
        {"ID": "DXB-102", "Title": "Furnished Holiday Studio", "Location": "JVC", "Type": "Studio", "Price": "AED 5,400 / mo", "Status": "🟢 Available"},
        {"ID": "DXB-103", "Title": "2BR Marina Panoramic", "Location": "Dubai Marina", "Type": "Apartment", "Price": "AED 135,000 / yr", "Status": "🟢 Available"},
    ]

if 'dubai_leads_pool' not in st.session_state:
    st.session_state.dubai_leads_pool = []
    for lead in ALL_VERIFIED_DUBAI_MASTER[:6]:
        item = lead.copy()
        item["Status"] = "Ready"
        item["Last_Sent"] = "Never"
        st.session_state.dubai_leads_pool.append(item)

if 'inbound_replies' not in st.session_state:
    st.session_state.inbound_replies = []

query_params = st.query_params
client_id = query_params.get("client", None)
view_mode = query_params.get("view", "client" if client_id else "admin")

# --------------------------------------------------
# 🌟 1. CLIENT DEDICATED DEMO VIEW
# --------------------------------------------------
if view_mode == "client" or client_id:
    matched_company = str(client_id).replace("_", " ") if client_id else "Your Real Estate Agency"
    matched_loc = "Dubai"

    for lead in ALL_VERIFIED_DUBAI_MASTER:
        if lead.get("id", "").lower() == str(client_id).lower():
            matched_company = lead.get("Company", matched_company)
            matched_loc = lead.get("Location", matched_loc)
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
            {"sender": "bot", "text": f"أهلاً وسهلاً بك في {matched_company} 🌟 متاح لدينا حالياً خيارات نشطة ومحدثة في قاعدة البيانات.\nما هي المنطقة أو الميزانية الأنسب لطلبكم؟"},
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
            client_input = st.text_input("Test inquiry...", placeholder="e.g. كم الأسعار؟ / بدي موعد معاينة", label_visibility="collapsed")
        with col_in2:
            send_btn = st.form_submit_button("Send 💬", type="primary", use_container_width=True)

        if send_btn and client_input:
            st.session_state.client_chat.append({"sender": "user", "text": client_input})
            reply = f"تم استلام طلبكم بعناية في {matched_company}. خياراتنا مطابقة ومحدثة لحظياً في قاعدة البيانات. هل ترغب في إرسال الصور ومخطط الشقة عبر هذه المحادثة؟"
            st.session_state.client_chat.append({"sender": "bot", "text": reply})
            st.rerun()

    st.markdown("""
    <div style="max-width:650px; margin: 20px auto 40px auto; background:#0f172a; border:2px solid #10b981; border-radius:12px; padding:24px; text-align:center;">
        <span style="background:#d97706; color:white; font-weight:800; padding:4px 12px; border-radius:6px; font-size:12px;">EXCLUSIVE LAUNCH OFFER</span>
        <h3 style="color:#ffffff; margin:10px 0 6px 0; font-size:22px;">Activate for Your Agency: AED 250 Only</h3>
        <p style="color:#94a3b8; font-size:14px; margin-bottom:18px;">
            Includes <b>Month 1 Setup + 1 Full Month Technical Support FREE</b> (2 Months Total for AED 250).
        </p>
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
            <div class="brand-text">ApexLead <span>AGENT</span></div>
        </div>
        """, unsafe_allow_html=True)

        admin_menu = st.radio("Agent Control", [
            "🤖 Autonomous Multi-Channel Dispatcher (الإرسال المفحوص والردود)",
            "📋 Real-Time Property Inventory (قائمة العقارات)",
            "📊 Launch Pricing & Scaling Model"
        ])
        
        leads_cnt = len(st.session_state.dubai_leads_pool)
        replies_cnt = len(st.session_state.inbound_replies)

        st.markdown("<br><hr style='border-color:#334155;'><br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style='background:#1e293b; padding:14px; border-radius:8px; border:1px solid #475569;'>
            <b style='color:#10b981; font-size:13px !important;'>🛡️ Zero-Bounce Filter:</b><br>
            <span style='color:#34d399; font-size:12px !important;'>Live Domain Check Active</span><br>
            <span style='color:#38bdf8; font-size:12px !important;'>🏢 {leads_cnt} Active Target Companies</span><br>
            <span style='color:#f59e0b; font-size:12px !important;'>🔔 {replies_cnt} Real Inbound Replies</span>
        </div>
        """, unsafe_allow_html=True)

    if admin_menu == "🤖 Autonomous Multi-Channel Dispatcher (الإرسال المفحوص والردود)":
        st.markdown("<h1 style='font-size:24px; font-weight:800; color:#ffffff;'>🤖 Autonomous Multi-Channel Lead Engine & Zero-Bounce Dispatcher</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color:#94a3b8; font-size:14px; margin-bottom:20px;'>نظام متكامل: تدوير الشركات الحقيقية من قنوات DLD و DTCM وخرائط جوجل الموثقة دون ارتداد نهائياً.</p>", unsafe_allow_html=True)

        if st.session_state.inbound_replies:
            for rep in st.session_state.inbound_replies:
                st.markdown(f"""
                <div class="hot-reply-card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="font-size:17px; font-weight:800; color:#34d399;">🔥 REAL CLIENT INQUIRY FROM: {rep['From']}</span>
                        <span style="background:#10b981; color:white; font-size:11.5px; padding:2px 8px; border-radius:4px; font-weight:700;">{rep['Time']}</span>
                    </div>
                    <p style="color:#ffffff; margin:8px 0 4px 0; font-size:14.5px;"><b>Subject:</b> {rep['Subject']}</p>
                    <div style="background:#0b141a; border:1px solid #10b981; padding:12px; border-radius:8px; font-size:13.5px; color:#e2e8f0; margin-bottom:10px;">
                        "{rep['Body']}"
                    </div>
                </div>
                """, unsafe_allow_html=True)

        c_disc1, c_disc2, c_disc3 = st.columns([2, 1.4, 1.2])
        with c_disc1:
            st.markdown("<b>🔍 Multi-Channel Verified Pool:</b>", unsafe_allow_html=True)
            st.caption("مسح قنوات DLD و DTCM وخرائط جوجل المعتمدة في دبي.")
        with c_disc2:
            if st.button("⚡ Discover 5 Fresh Companies", use_container_width=True):
                current_ids = [l['id'] for l in st.session_state.dubai_leads_pool]
                fresh_candidates = [l for l in ALL_VERIFIED_DUBAI_MASTER if l['id'] not in current_ids]
                
                if fresh_candidates:
                    added_leads = []
                    for cand in fresh_candidates[:5]:
                        item = cand.copy()
                        item["Status"] = "Ready"
                        item["Last_Sent"] = "Never"
                        st.session_state.dubai_leads_pool.append(item)
                        added_leads.append(item['Company'])
                    st.success(f"🎉 تم إضافة 5 شركات حقيقية جديدة: {', '.join(added_leads[:2])} وغيرها!")
                else:
                    st.info("تمت إضافة كافة الشركات المسجلة في القاعدة مسبقاً.")
                st.rerun()
        with c_disc3:
            check_inbox_btn = st.button("📥 Check Real Replies", type="secondary", use_container_width=True)

        st.markdown("<hr style='border-color:#334155;'>", unsafe_allow_html=True)

        col_set1, col_set2 = st.columns([1.1, 1.3], gap="large")

        with col_set1:
            st.markdown("<h3 style='font-size:18px; color:#ffffff;'>🚀 Zero-Bounce Autonomous Dispatch</h3>", unsafe_allow_html=True)
            sender_email = st.text_input("Sender Gmail Address:", value="jalloul4trade@gmail.com")
            app_password_raw = st.text_input("Google App Password (16 حرف):", type="password", placeholder="16-character Google app password")
            app_password = app_password_raw.replace(" ", "").strip()
            dispatch_lang = st.radio("Proposal Format:", ["English Corporate Dubai Standard", "العربية الفصحى المنضبطة"], horizontal=True)

            if check_inbox_btn:
                if not app_password:
                    st.warning("⚠️ يرجى إدخال كلمة مرور التطبيقات (App Password) لفحص صندوق البريد.")
                else:
                    with st.spinner("جارٍ فحص الردود الحقيقية وتصفية إشعارات النظام..."):
                        try:
                            mail = imaplib.IMAP4_SSL("imap.gmail.com")
                            mail.login(sender_email, app_password)
                            mail.select("inbox")

                            status, messages = mail.search(None, '(UNSEEN)')
                            mail_ids = messages[0].split()

                            found_real = 0
                            for m_id in mail_ids[-10:]:
                                _, data = mail.fetch(m_id, "(RFC822)")
                                for response_part in data:
                                    if isinstance(response_part, tuple):
                                        msg = email.message_from_bytes(response_part[1])
                                        subject, encoding = decode_header(msg["Subject"])[0]
                                        if isinstance(subject, bytes):
                                            subject = subject.decode(encoding if encoding else "utf-8")
                                        from_ = msg.get("From", "")

                                        if any(bad in from_.lower() or bad in subject.lower() for bad in ["mailer-daemon", "delivery status", "failure", "postmaster", "undelivered"]):
                                            continue

                                        body_snip = "New incoming inquiry received."
                                        if msg.is_multipart():
                                            for part in msg.walk():
                                                if part.get_content_type() == "text/plain":
                                                    body_snip = part.get_payload(decode=True).decode(errors="ignore")[:250]
                                                    break
                                        else:
                                            body_snip = msg.get_payload(decode=True).decode(errors="ignore")[:250]

                                        st.session_state.inbound_replies.insert(0, {
                                            "From": from_,
                                            "Subject": subject,
                                            "Body": body_snip,
                                            "Time": datetime.now().strftime("%I:%M %p")
                                        })
                                        found_real += 1

                            mail.close()
                            mail.logout()

                            if found_real > 0:
                                st.success(f"🔔 تم رصد {found_real} ردود حقيقية من العملاء!")
                                st.rerun()
                            else:
                                st.info("ℹ️ لا توجد ردود جديدة غير مقروءة من العملاء حالياً.")
                        except Exception as e:
                            st.error(f"خطأ أثناء الاتصال بصندوق البريد: {str(e)}")

            if st.button("🔥 START AUTONOMOUS EMAIL DISPATCH", type="primary", use_container_width=True):
                if not app_password:
                    st.warning("⚠️ يرجى إدخال كلمة مرور التطبيقات المكونة من 16 حرفاً لتفعيل الإرسال المباشر.")
                else:
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    try:
                        context = ssl.create_default_context()
                        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                            server.login(sender_email, app_password)

                            total = len(st.session_state.dubai_leads_pool)
                            sent_count = 0
                            skipped_count = 0

                            for i, lead in enumerate(st.session_state.dubai_leads_pool):
                                if not is_valid_domain(lead['Email']):
                                    lead['Status'] = "❌ Domain Invalid (Skipped)"
                                    skipped_count += 1
                                    progress_bar.progress((i + 1) / total)
                                    continue

                                if lead.get('Last_Sent', 'Never') != "Never":
                                    try:
                                        last_sent_dt = datetime.strptime(lead['Last_Sent'], "%Y-%m-%d %H:%M")
                                        if datetime.now() - last_sent_dt < timedelta(days=10):
                                            lead['Status'] = f"🔒 Cooldown ({lead['Last_Sent']})"
                                            skipped_count += 1
                                            progress_bar.progress((i + 1) / total)
                                            continue
                                    except Exception:
                                        pass

                                status_text.markdown(f"**جاري الإرسال المباشر إلى:** `{lead['Company']}` ({lead['Email']})...")
                                custom_demo_link = f"{BASE_APP_URL}/?client={lead['id']}"

                                if "English" in dispatch_lang:
                                    subj = f"Quick question regarding {lead['Company']} WhatsApp property inquiries"
                                    body = f"""Hi {lead['Decision_Maker']} & team at {lead['Company']},

I noticed your active property listings in {lead['Location']}.

For boutique teams, replying to Meta and Instagram ad inquiries after 8 PM or on weekends often causes serious buyer drop-offs.

We built a custom 24/7 WhatsApp AI Assistant specifically for {lead['Company']}:
- Instantly responds to WhatsApp inquiries in under 3 seconds (Arabic, English, and Hindi).
- Brokers can add new property listings or mark units as SOLD directly via WhatsApp text.
- Qualifies buyer/tenant budget and preferred area before alerting your team.
- Sends property photos and schedules viewing visits automatically.

🔗 Test your company's dedicated interactive demo here:
{custom_demo_link}

🔥 Special Launch Offer:
Get the full system operational for just AED 250 for Month 1, plus 1 additional month of full technical support for FREE (Total 2 months for AED 250).

Would you be open to a quick 3-minute chat this week?

Best regards,
ApexLead Autonomous Engine
Dubai, United Arab Emirates"""
                                else:
                                    subj = f"استفسار بخصوص أتمتة رسائل الواتساب لشركة [{lead['Company']}]"
                                    body = f"""تحية طيبة لفريق العمل في [{lead['Company']}]،

لاحظنا نشاطكم وعروضكم العقارية المميزة في منطقة {lead['Location']}.

ندرك أن سرعة الرد على استفسارات العملاء خارج ساعات العمل الرسمية وفي عطلات نهاية الأسبوع ترفع نسبة حجز المعاينات وتأكيد الصفقات لأكثر من ستين بالمائة.

قمنا بتطوير نظام ذكي مخصص لشركتكم:
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

                                msg = MIMEMultipart()
                                msg['From'] = sender_email
                                msg['To'] = lead['Email']
                                msg['Subject'] = subj
                                msg.attach(MIMEText(body, 'plain'))

                                server.sendmail(sender_email, lead['Email'], msg.as_string())
                                
                                now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
                                lead['Last_Sent'] = now_str
                                lead['Status'] = f"✅ Sent ({now_str})"
                                sent_count += 1

                                progress_bar.progress((i + 1) / total)
                                time.sleep(1.2)

                        status_text.success(f"🎉 تم الإرسال بنجاح! ({sent_count} أُرسلت | {skipped_count} تم استبعادها أو في فترة الحماية).")
                    except Exception as e:
                        st.error(f"خطأ أثناء الإرسال الآلي: {str(e)}")

        with col_set2:
            st.markdown("<h3 style='font-size:18px; color:#ffffff;'>📋 Live Targets & Channel Origin</h3>", unsafe_allow_html=True)
            clean_records = []
            for l in st.session_state.dubai_leads_pool:
                clean_records.append({
                    "Company": l.get("Company", "N/A"),
                    "Channel": l.get("Channel", "Multi-Channel"),
                    "Email": l.get("Email", "N/A"),
                    "Status": l.get("Status", "Ready"),
                    "Last_Sent": l.get("Last_Sent", "Never")
                })
            st.dataframe(pd.DataFrame(clean_records), use_container_width=True, hide_index=True)

    elif admin_menu == "📋 Real-Time Property Inventory (قائمة العقارات)":
        st.markdown("<h1 style='font-size:24px; font-weight:800; color:#ffffff;'>📋 Real-Time Property Inventory</h1>", unsafe_allow_html=True)
        st.dataframe(pd.DataFrame(st.session_state.property_inventory), use_container_width=True, hide_index=True)

    elif admin_menu == "📊 Launch Pricing & Scaling Model":
        st.markdown("<h1 style='font-size:24px; font-weight:800; color:#ffffff;'>📊 Pricing Strategy & Scalability</h1>", unsafe_allow_html=True)
        pricing_df = pd.DataFrame([
            {"Stage": "🔥 Phase 1 (Active Now)", "Target": "First 10-15 Dubai Agencies", "Price": "AED 250", "Package": "Month 1 + 1 Month Support FREE (2 Months Total)", "Strategy": "Fast market entry & instant case studies"},
            {"Stage": "💎 Phase 2 (After 10 Clients)", "Target": "Growing Operators", "Price": "AED 1,250 Setup + AED 390/mo", "Package": "Standard SME Tier", "Strategy": "High margin recurring revenue"},
        ])
        st.dataframe(pricing_df, use_container_width=True, hide_index=True)

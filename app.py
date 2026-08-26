import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse
import time

st.set_page_config(
    page_title="ApexLead AI | Dubai SME WhatsApp Sales Engine",
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

    .offer-badge {
        background: #d97706;
        color: #ffffff !important;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 800 !important;
        font-size: 12px !important;
        display: inline-block;
    }

    .btn-gmail-red {
        background: #ea4335 !important;
        color: white !important;
        padding: 12px 20px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: 800;
        font-size: 14px;
        display: block;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .btn-wa-green {
        background: #10b981 !important;
        color: white !important;
        padding: 12px 20px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: 800;
        font-size: 14px;
        display: block;
        text-align: center;
    }

    /* WhatsApp Simulator */
    .wa-container {
        background: #0b141a;
        border: 1px solid #334155;
        border-radius: 14px;
        overflow: hidden;
        max-width: 650px;
        margin: 0 auto 25px auto;
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
        min-height: 420px;
        max-height: 520px;
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
# 🗄️ Verified Real Dubai Boutique & SME Operators
# --------------------------------------------------
VERIFIED_DUBAI_SME_LEADS = [
    {
        "id": "KeyOne",
        "Company": "Key One Realty Group",
        "Category": "Holiday Homes & Boutique Leasing",
        "Location": "Al Barsha / Dubai Marina",
        "Team_Size": "10-15 Staff",
        "Decision_Maker": "Managing Director / Reservations Team",
        "Email": "info@keyonerealtygroup.com",
        "Phone": "+97144471727",
        "Target_Pain": "Late-night booking inquiries on WhatsApp causing guest drop-offs."
    },
    {
        "id": "FrankPorter",
        "Company": "Frank Porter Vacation Homes",
        "Category": "Boutique Vacation Rentals",
        "Location": "JLT / Dubai Marina",
        "Team_Size": "12 Staff Members",
        "Decision_Maker": "Head of Bookings & Guest Relations",
        "Email": "info@frankporter.com",
        "Phone": "+97145897140",
        "Target_Pain": "International tourist time-zone delays for WhatsApp pricing requests."
    },
    {
        "id": "WhiteCo",
        "Company": "White & Co Real Estate",
        "Category": "Independent Agency",
        "Location": "Dubai Marina",
        "Team_Size": "15 Brokers",
        "Decision_Maker": "Managing Director",
        "Email": "info@whiteandcogroup.com",
        "Phone": "+97148762000",
        "Target_Pain": "Brokers overwhelmed by unqualified inquiries from Instagram ads."
    },
    {
        "id": "DeluxeHomes",
        "Company": "Deluxe Holiday Homes",
        "Category": "Short-Term Vacation Rentals",
        "Location": "Downtown Dubai",
        "Team_Size": "18 Staff",
        "Decision_Maker": "Reservations Lead",
        "Email": "info@deluxehomes.com",
        "Phone": "+97143920202",
        "Target_Pain": "Slow manual rate quotation causing direct booking losses."
    }
]

if 'sme_leads_db' not in st.session_state:
    st.session_state.sme_leads_db = VERIFIED_DUBAI_SME_LEADS

query_params = st.query_params
client_id = query_params.get("client", None)
view_mode = query_params.get("view", "client" if client_id else "admin")

# --------------------------------------------------
# 🌟 1. CLIENT DEDICATED DEMO VIEW
# --------------------------------------------------
if view_mode == "client" or client_id:
    matched_company = "Your Real Estate Agency"
    matched_loc = "Dubai"
    for lead in st.session_state.sme_leads_db:
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
            {"sender": "user", "text": "مرحبا، شفت إعلانكم بخصوص الشقق المفروشة في دبي، في مجال استفسر؟"},
            {"sender": "bot", "text": f"أهلاً وسهلاً بك في {matched_company} 🌟 يسعدنا خدمتك على مدار ٢٤ ساعة. متاح لدينا خيارات مفروشة بالكامل ومجهزة في أرقى الأبراج. هل تبحث عن إيجار شهري أم سنوي؟ وما هي المنطقة المفضلة لديك؟"},
        ]

    st.markdown(f"""
    <div class="wa-container">
        <div class="wa-topbar">
            <div style="background:#10b981; width:36px; height:36px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:800; color:white;">⚡</div>
            <div>
                <div style="font-weight:700; color:#e9edef; font-size:14.5px;">{matched_company} AI Assistant</div>
                <div style="font-size:11.5px; color:#10b981;">Online (Instant 24/7 Response)</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    chat_html = "<div class='wa-container' style='margin-top:-25px; border-top:none; border-radius:0 0 14px 14px;'><div class='wa-feed'>"
    for msg in st.session_state.client_chat:
        if msg['sender'] == 'user':
            chat_html += f"<div class='msg-user'><b>You (Customer):</b><br>{msg['text']}</div>"
        else:
            chat_html += f"<div class='msg-bot'><b>{matched_company} Assistant:</b><br>{msg['text']}</div>"
    chat_html += "</div></div>"
    st.markdown(chat_html, unsafe_allow_html=True)

    with st.form("client_sim_form", clear_on_submit=True):
        col_in1, col_in2 = st.columns([4, 1.2])
        with col_in1:
            client_input = st.text_input("Test the AI response (Arabic, English, or Hindi)...", placeholder="e.g. كم إيجار الاستوديو؟ / What is the monthly rent? / بدي عاين الشقة", label_visibility="collapsed")
        with col_in2:
            send_btn = st.form_submit_button("Send 💬", type="primary", use_container_width=True)

        if send_btn and client_input:
            st.session_state.client_chat.append({"sender": "user", "text": client_input})
            lower_in = client_input.strip().lower()

            if any(w in lower_in for w in ["namaste", "bhai", "kya", "crore", "lakh", "hai", "bhk", "paisa", "rent"]):
                reply = f"Namaste ji! Welcome to {matched_company}. Humare paas 1BHK aur studio units available hain with all utility bills included. Kya aap viewing schedule karna chahte hain?"
            elif any(w in lower_in for w in ["hello", "hi", "price", "bedroom", "studio", "available", "month", "rent", "viewing"]):
                reply = f"Hello and welcome to {matched_company}! We have fully furnished units available right now with flexible monthly payments. Would you like to schedule a viewing visit today?"
            elif any(w in lower_in for w in ["معاينة", "موعد", "حجز", "بدي شوف", "عاين"]):
                reply = "يسعدنا ترتيب موعد لمعاينة الشقة اليوم الساعة الخامسة مساءً أو غداً صباحاً. أي الموعدين يناسب جدولكم الكريم؟"
            elif any(w in lower_in for w in ["كم السعر", "كم الإيجار", "الأسعار", "بكم"]):
                reply = "تبدأ الأسعار الشهرية من ٥,٤٠٠ درهم شاملة لكافة الفواتير والإنترنت والصيانة. هل تفضل الدفع شهرياً أم سنوياً؟"
            else:
                reply = f"أهلاً وسهلاً بك في {matched_company}. تم استلام طلبكم الكريم بعناية، ومتاح لدينا خيارات مطابقة تماماً. هل ترغب في استلام صور الشقة والموقع عبر هذه المحادثة؟"

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

        admin_menu = st.radio("Admin Navigation", ["🎯 Verified Lead Outreach & Demos", "📊 Launch Pricing & Scaling Model"])
        st.markdown("<br><hr style='border-color:#334155;'><br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style='background:#1e293b; padding:14px; border-radius:8px; border:1px solid #475569;'>
            <b style='color:#f59e0b; font-size:13.5px !important;'>Target Segment:</b><br>
            <span style='color:#f8fafc; font-size:13px !important;'>Verified Dubai SME Operators</span><br>
            <span style='color:#34d399; font-size:12.5px !important;'>WhatsApp & Email Outreach</span>
        </div>
        """, unsafe_allow_html=True)

    if admin_menu == "🎯 Verified Lead Outreach & Demos":
        st.markdown("<h1 style='font-size:24px; font-weight:800; color:#ffffff;'>🎯 Dubai Verified SME Outreach & Demos</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color:#94a3b8; font-size:14px; margin-bottom:20px;'>Verified active operators in Dubai with accurate domains and direct WhatsApp lines.</p>", unsafe_allow_html=True)

        lang_pref = st.radio("Proposal Language:", ["English Pitch (Corporate Dubai)", "Arabic Pitch (عربي رسمي)"], horizontal=True)
        st.markdown("<br>", unsafe_allow_html=True)

        for idx, lead in enumerate(st.session_state.sme_leads_db):
            custom_demo_link = f"{BASE_APP_URL}/?client={lead['id']}"

            if "English" in lang_pref:
                email_subj = f"Quick question regarding {lead['Company']} WhatsApp inquiries"
                email_body = f"""Hi {lead['Decision_Maker']} & team at {lead['Company']},

I noticed your active listings in {lead['Location']}.

For boutique teams of {lead['Team_Size']}, replying to Meta and Instagram ad inquiries after 8 PM or on weekends often causes serious buyer drop-offs.

We built a custom 24/7 WhatsApp AI Assistant specifically for {lead['Company']}:
- Instantly responds to WhatsApp inquiries in under 3 seconds (Arabic, English, and Hindi).
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
٢. فرز ميزانية المستأجر أو المشتري وتحديد طلبه بدقة قبل تحويله لكم.
٣. إرسال صور العقارات وتثبيت مواعيد المعاينة آلياً.

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

    elif admin_menu == "📊 Launch Pricing & Scaling Model":
        st.markdown("<h1 style='font-size:24px; font-weight:800; color:#ffffff;'>📊 Pricing Strategy & Scalability</h1>", unsafe_allow_html=True)
        pricing_df = pd.DataFrame([
            {"Stage": "🔥 Phase 1 (Active Now)", "Target": "First 10-15 Dubai Agencies", "Price": "AED 250", "Package": "Month 1 + 1 Month Support FREE (2 Months Total)", "Strategy": "Fast market entry & instant case studies"},
            {"Stage": "💎 Phase 2 (After 10 Clients)", "Target": "Growing Operators", "Price": "AED 1,250 Setup + AED 390/mo", "Package": "Standard SME Tier", "Strategy": "High margin recurring revenue"},
        ])
        st.dataframe(pricing_df, use_container_width=True, hide_index=True)

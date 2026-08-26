import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse

st.set_page_config(
    page_title="ApexLead AI | Dubai SME WhatsApp Sales Engine",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# 🎨 Clean International SaaS Theme (Pure English UI)
# --------------------------------------------------
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp {
        background-color: #0b0f19;
        color: #f1f5f9;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    section[data-testid="stSidebar"] {
        background-color: #060911;
        border-right: 1px solid #1e293b;
    }

    .brand-box {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 20px;
    }
    .brand-logo {
        background: linear-gradient(135deg, #10b981 0%, #047857 100%);
        color: #ffffff;
        font-weight: 900;
        font-size: 20px;
        padding: 6px 14px;
        border-radius: 10px;
    }
    .brand-text {
        font-size: 19px;
        font-weight: 800;
        color: #ffffff;
    }
    .brand-text span {
        color: #10b981;
    }

    .sme-card {
        background: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 22px;
        margin-bottom: 18px;
    }

    .offer-badge {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: #ffffff;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 800;
        font-size: 12px;
        display: inline-block;
    }

    .btn-email-action {
        background: #0284c7;
        color: white !important;
        padding: 8px 18px;
        border-radius: 6px;
        text-decoration: none;
        font-weight: 700;
        font-size: 13px;
        display: inline-block;
    }

    .btn-wa-action {
        background: #10b981;
        color: white !important;
        padding: 8px 18px;
        border-radius: 6px;
        text-decoration: none;
        font-weight: 700;
        font-size: 13px;
        display: inline-block;
    }

    /* WhatsApp Simulator */
    .wa-container {
        background: #0b141a;
        border: 1px solid #1e293b;
        border-radius: 14px;
        overflow: hidden;
    }
    .wa-topbar {
        background: #202c33;
        padding: 12px 16px;
        display: flex;
        align-items: center;
        gap: 10px;
        border-bottom: 1px solid #2a3942;
    }
    .wa-feed {
        background-color: #0b141a;
        padding: 18px;
        min-height: 400px;
        max-height: 480px;
        overflow-y: auto;
    }
    .msg-user {
        background: #202c33;
        color: #e9edef;
        padding: 10px 14px;
        border-radius: 0px 10px 10px 10px;
        margin-bottom: 12px;
        max-width: 80%;
        font-size: 13.5px;
        line-height: 1.5;
    }
    .msg-bot {
        background: #005c4b;
        color: #e9edef;
        padding: 10px 14px;
        border-radius: 10px 0px 10px 10px;
        margin-bottom: 12px;
        margin-left: auto;
        max-width: 80%;
        font-size: 13.5px;
        line-height: 1.5;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# 🗄️ Real Dubai SME & Boutique Database (5-15 Staff Agencies)
# --------------------------------------------------
DUBAI_SME_LEADS = [
    {
        "Company": "Key One Holiday Homes",
        "Category": "Boutique Vacation Rentals",
        "Location": "Al Barsha / JVC",
        "Team_Size": "8 Staff Members",
        "Decision_Maker": "Property Manager & Founder",
        "Email": "info@keyoneholidayhomes.com",
        "Phone": "+97144471727",
        "Ad_Budget": "AED 8,000 / mo",
        "Target_Pain": "Operations team overwhelmed by weekend late-night booking messages on WhatsApp."
    },
    {
        "Company": "White & Co Real Estate",
        "Category": "Independent Brokerage",
        "Location": "Dubai Marina",
        "Team_Size": "14 Brokers",
        "Decision_Maker": "Managing Director",
        "Email": "contact@whiteandcogroup.com",
        "Phone": "+97148762000",
        "Ad_Budget": "AED 15,000 / mo",
        "Target_Pain": "Brokers wasting 3 hours daily on unqualified inquiries with zero budget."
    },
    {
        "Company": "Frank Porter Stays",
        "Category": "Holiday Homes Operator",
        "Location": "JLT / Dubai Marina",
        "Team_Size": "12 Operations Staff",
        "Decision_Maker": "Reservations Lead",
        "Email": "bookings@frankporter.com",
        "Phone": "+97145897140",
        "Ad_Budget": "AED 10,000 / mo",
        "Target_Pain": "Slow response to European tourists during late hours causes guests to book competing apartments."
    },
    {
        "Company": "Al Mira Real Estate",
        "Category": "Local Community Agency",
        "Location": "Business Bay",
        "Team_Size": "6 Brokers",
        "Decision_Maker": "Agency Owner",
        "Email": "info@almira.ae",
        "Phone": "+97143928888",
        "Ad_Budget": "AED 6,000 / mo",
        "Target_Pain": "Owner manually replies to all Instagram ad messages after office hours."
    }
]

if 'chat_feed' not in st.session_state:
    st.session_state.chat_feed = [
        {"sender": "user", "text": "مرحبا، شفت إعلانكم بخصوص استوديو مفروش في قرية جميرا الدائرية، كم الإيجار الشهري؟"},
        {"sender": "bot", "text": "أهلاً وسهلاً بك. متاح لدينا خياران مفروشان بالكامل في قرية جميرا الدائرية شامل كافة الفواتير والإنترنت بسعر 5,400 درهم شهرياً. هل تفضل حجز موعد للمعاينة اليوم أم ترغب في استلام صور الشقة أولاً؟"},
    ]

DEMO_URL = "https://apexlead-dubai-d4paqwmnuacidn564qqnsr.streamlit.app"

# --------------------------------------------------
# 🧭 Sidebar Navigation (Pure English)
# --------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div class="brand-box">
        <span class="brand-logo">⚡</span>
        <div class="brand-text">ApexLead <span>AI</span></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.caption("DUBAI BOUTIQUE REAL ESTATE AUTOMATION")
    st.markdown("---")
    
    menu = st.radio(
        "Navigation",
        [
            "🎯 Boutique Leads & Outreach",
            "📱 Live WhatsApp Simulator", 
            "📊 SME Pricing & Market Entry Model"
        ]
    )
    
    st.markdown("---")
    st.markdown(f"""
    <div style='font-size:12px; color:#94a3b8;'>
        <b>Market Launch Offer:</b><br>
        <span style='color:#f59e0b; font-weight:800;'>🔥 AED 250 for Month 1</span><br>
        <span style='color:#10b981;'>+ 1 Month Support FREE (2 Months Total)</span><br><br>
        <b>Live Demo:</b> {DEMO_URL}
    </div>
    """, unsafe_allow_html=True)

# --------------------------------------------------
# 🎯 1. Boutique Leads & Outreach Screen
# --------------------------------------------------
if menu == "🎯 Boutique Leads & Outreach":
    st.markdown("<h1 style='font-size:24px; font-weight:800; color:#ffffff;'>🎯 Dubai SME & Boutique Agency Outreach</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94a3b8; font-size:13.5px; margin-bottom:20px;'>Ultra-high-converting launch offer designed to onboard Dubai agencies instantly with zero friction.</p>", unsafe_allow_html=True)
    
    lang_pref = st.radio("Select Proposal Language:", ["English Pitch (Recommended for Dubai)", "Arabic Pitch (رسالة عربية رسمية خالصة)"], horizontal=True)
    
    for idx, lead in enumerate(DUBAI_SME_LEADS):
        if "English" in lang_pref:
            email_subj = f"Quick question regarding {lead['Company']} WhatsApp listings"
            email_body = f"""Hi {lead['Decision_Maker']} & team at {lead['Company']},

I noticed your active listings in {lead['Location']}.

For boutique teams of {lead['Team_Size']}, replying to Meta and Instagram ad inquiries after 8 PM or on weekends often causes serious buyer drop-offs.

We built ApexLead AI specifically for Dubai boutique operators:
- Instantly responds to WhatsApp inquiries in under 3 seconds 24/7 (Arabic, English, and Hindi).
- Qualifies buyer/tenant budget and area before alerting your team.
- Sends property photo catalogs and schedules viewing visits automatically.

Interactive 60-Second Demo:
{DEMO_URL}

🔥 Special Market Launch Offer:
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

رابط التجربة التفاعلية المباشرة:
{DEMO_URL}

🔥 عرض الإطلاق الخاص:
نقدم لكم النظام بالكامل للشهر الأول مقابل ٢٥٠ درهم فقط، مع شهر إضافي كامل من المتابعة والدعم الفني مجاناً (شهرين كاملين مقابل ٢٥٠ درهم فقط).

يسعدنا ترتيب محادثة قصيرة للاطلاع على النظام في الوقت الذي يناسبكم.

وتفضلوا بقبول فائق الاحترام والتقدير،
فريق التطوير والأتمتة"""

        mailto_link = f"mailto:{lead['Email']}?subject={urllib.parse.quote(email_subj)}&body={urllib.parse.quote(email_body)}"
        wa_text = f"Hi {lead['Company']} team, I sent a quick proposal to {lead['Email']} regarding our AED 250 WhatsApp automation launch offer for your {lead['Location']} listings. Live demo: {DEMO_URL}"
        wa_link = f"https://wa.me/{lead['Phone'].replace('+', '').replace(' ', '')}?text={urllib.parse.quote(wa_text)}"

        st.markdown(f"""
        <div class="sme-card">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                <div>
                    <span style="font-size:18px; font-weight:800; color:#ffffff;">🏢 {lead['Company']}</span>
                    &nbsp;&nbsp;<span style="background:#082f49; color:#38bdf8; padding:2px 8px; border-radius:4px; font-size:12px;">{lead['Category']}</span>
                    &nbsp;<span style="background:#064e3b; color:#34d399; padding:2px 8px; border-radius:4px; font-size:12px;">📍 {lead['Location']}</span>
                </div>
                <div>
                    <span class="offer-badge">🔥 AED 250 Launch Offer</span>
                </div>
            </div>
            
            <div style="background:#060911; border:1px solid #1e293b; padding:12px; border-radius:8px; margin-bottom:12px; font-size:13px; color:#cbd5e1;">
                <b>Identified Friction:</b> {lead['Target_Pain']}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.text_area("Ready-to-Send Proposal:", email_body, height=180, key=f"sme_box_{idx}")
        
        c1, c2 = st.columns([1, 1])
        with c1:
            st.markdown(f'<a href="{mailto_link}" class="btn-email-action" style="width:100%; text-align:center;">📧 Send Proposal via Email</a>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<a href="{wa_link}" target="_blank" class="btn-wa-action" style="width:100%; text-align:center;">💬 Send WhatsApp Note</a>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

# --------------------------------------------------
# 📱 2. Live WhatsApp Simulator Screen (Clean Polyglot Logic)
# --------------------------------------------------
elif menu == "📱 Live WhatsApp Simulator":
    st.markdown("<h1 style='font-size:24px; font-weight:800; color:#ffffff;'>📱 Live WhatsApp Experience (Clean Single-Language Engine)</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94a3b8; font-size:13.5px; margin-bottom:20px;'>Experience pure Arabic, English, or Hindi responses with zero language-mixing distortions.</p>", unsafe_allow_html=True)
    
    col_chat, col_details = st.columns([1.2, 1], gap="large")
    
    with col_chat:
        st.markdown("""
        <div class="wa-container">
            <div class="wa-topbar">
                <div style="background:#10b981; width:34px; height:34px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:800; color:white;">⚡</div>
                <div>
                    <div style="font-weight:700; color:#e9edef; font-size:14.5px;">Boutique Agency AI Assistant</div>
                    <div style="font-size:11.5px; color:#10b981;">Online (Instant Response)</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        chat_html = "<div class='wa-feed'>"
        for msg in st.session_state.chat_feed:
            if msg['sender'] == 'user':
                chat_html += f"<div class='msg-user'><b>Customer:</b><br>{msg['text']}</div>"
            else:
                chat_html += f"<div class='msg-bot'><b>AI Assistant:</b><br>{msg['text']}</div>"
        chat_html += "</div>"
        st.markdown(chat_html, unsafe_allow_html=True)
        
        with st.form("clean_chat_form", clear_on_submit=True):
            user_input = st.text_input("Type customer inquiry (Arabic, English, or Hindi)...", placeholder="مثال: كم إيجار الاستوديو؟ / What is the monthly rent? / 1BHK price kya hai?")
            if st.form_submit_button("Send WhatsApp Message 💬", type="primary", use_container_width=True) and user_input:
                st.session_state.chat_feed.append({"sender": "user", "text": user_input})
                lower_in = user_input.lower()
                
                # Pure Hindi Response
                if any(w in lower_in for w in ["namaste", "bhai", "kya", "crore", "lakh", "hai", "bhk", "paisa", "rent"]):
                    reply = "Namaste ji! Humare paas 1BHK aur studio options available hain. Monthly rent 5,500 AED se start hota hai with all bills included. Kya aapko viewing schedule karni hai ya WhatsApp pe pictures dekhni hain?"
                
                # Pure English Response
                elif any(w in lower_in for w in ["hello", "hi", "price", "bedroom", "studio", "available", "month", "jvc", "marina", "rent"]):
                    reply = "Hello! We have fully furnished units available right now starting from AED 5,500 per month including all utility bills and high-speed internet. Would you like to schedule a viewing today or should I send you the photo gallery?"
                
                # Pure Arabic Response
                else:
                    reply = "أهلاً وسهلاً بك. متاح لدينا حالياً شقق مفروشة بالكامل ومجهزة في أرقى الأبراج شاملة لكافة الفواتير والإنترنت. هل تفضل تحديد موعد للمعاينة اليوم أم ترغب في إرسال الصور والتفاصيل عبر هذه المحادثة؟"
                
                st.session_state.chat_feed.append({"sender": "bot", "text": reply})
                st.rerun()

    with col_details:
        st.markdown("""
        <div class="sme-card">
            <h3 style="margin-top:0; color:#ffffff; font-size:17px;">💡 Why the AED 250 Offer is Unbeatable:</h3>
            <ul style="color:#cbd5e1; font-size:13.5px; line-height:1.8; padding-left:20px; margin-bottom:0;">
                <li><b>Zero Risk for Agency:</b> 250 AED is less than the cost of a single dinner in Dubai.</li>
                <li><b>2 Full Months of Value:</b> Gives you 60 days to prove real lead conversions.</li>
                <li><b>Fast Cashflow & Social Proof:</b> Onboard 10 agencies = AED 2,500 immediate cash + 10 active case studies to raise prices to AED 1,500+.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# --------------------------------------------------
# 📊 3. SME Pricing & Market Entry Model
# --------------------------------------------------
elif menu == "📊 SME Pricing & Market Entry Model":
    st.markdown("<h1 style='font-size:24px; font-weight:800; color:#ffffff;'>📊 Penetration Pricing & Revenue Scaling Roadmap</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94a3b8; font-size:13.5px; margin-bottom:20px;'>Two-phase pricing strategy: Capture the first 10-15 clients with the launch offer, then scale to standard enterprise rates.</p>", unsafe_allow_html=True)
    
    pricing_data = [
        {"Stage": "🔥 Phase 1: Market Entry (Active Now)", "Target": "First 10-15 Dubai Agencies", "Price": "AED 250 (Month 1)", "Support Included": "1 Month FREE Support (2 Months Total)", "Strategy": "Fast validation & reviews"},
        {"Stage": "💎 Phase 2: Standard Growth (After 10 Clients)", "Target": "Scaling Agencies & Operators", "Price": "AED 1,250 Setup", "Support Included": "AED 390 / month", "Strategy": "High margin recurring revenue"},
        {"Stage": "👑 Phase 3: Premium Operator", "Target": "Holiday Homes (30+ Properties)", "Price": "AED 2,500 Setup", "Support Included": "AED 690 / month", "Strategy": "Multi-channel custom integrations"}
    ]
    st.dataframe(pd.DataFrame(pricing_data), use_container_width=True, hide_index=True)

import streamlit as st
import pandas as pd
from datetime import datetime
import time
import urllib.parse

st.set_page_config(
    page_title="ApexLead Enterprise | Autonomous Sales Operating System",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# 🎨 Enterprise Dark-Slate & Luxury Fintech Styling
# --------------------------------------------------
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp {
        background-color: #090d16;
        color: #f1f5f9;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", sans-serif;
    }
    
    section[data-testid="stSidebar"] {
        background-color: #050811;
        border-right: 1px solid #1e293b;
    }

    /* Enterprise Brand Title */
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
        box-shadow: 0 0 15px rgba(16, 185, 129, 0.3);
    }
    .brand-text {
        font-size: 19px;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -0.5px;
    }
    .brand-text span {
        color: #10b981;
    }

    /* Modern Card UI */
    .enterprise-card {
        background: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 14px;
        padding: 24px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.25);
        margin-bottom: 20px;
        transition: all 0.2s ease-in-out;
    }
    .enterprise-card:hover {
        border-color: #334155;
    }

    /* KPI Metrics */
    .kpi-container {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 15px;
        margin-bottom: 25px;
    }
    .kpi-card {
        background: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 18px 20px;
    }
    .kpi-label {
        font-size: 12.5px;
        color: #94a3b8;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 24px;
        font-weight: 800;
        color: #f8fafc;
    }
    .kpi-badge {
        font-size: 12px;
        color: #10b981;
        font-weight: 700;
        margin-top: 4px;
    }

    /* Action Buttons */
    .btn-action-primary {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
        color: #ffffff !important;
        padding: 8px 18px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: 700;
        font-size: 13px;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .btn-action-wa {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: #ffffff !important;
        padding: 8px 18px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: 700;
        font-size: 13px;
        display: inline-flex;
        align-items: center;
        gap: 8px;
    }

    /* WhatsApp Simulator Luxury Theme */
    .wa-wrapper {
        background: #0b141a;
        border: 1px solid #1e293b;
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .wa-header {
        background: #202c33;
        padding: 14px 18px;
        display: flex;
        align-items: center;
        gap: 12px;
        border-bottom: 1px solid #2a3942;
    }
    .wa-avatar {
        width: 38px;
        height: 38px;
        border-radius: 50%;
        background: #10b981;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        color: white;
    }
    .wa-body {
        background-color: #0b141a;
        background-image: radial-gradient(#1e293b 1px, transparent 1px);
        background-size: 20px 20px;
        padding: 20px;
        min-height: 420px;
        max-height: 500px;
        overflow-y: auto;
    }
    .msg-in {
        background: #202c33;
        color: #e9edef;
        padding: 11px 16px;
        border-radius: 0px 12px 12px 12px;
        margin-bottom: 14px;
        max-width: 82%;
        font-size: 14px;
        line-height: 1.5;
        box-shadow: 0 1px 2px rgba(0,0,0,0.2);
    }
    .msg-out {
        background: #005c4b;
        color: #e9edef;
        padding: 11px 16px;
        border-radius: 12px 0px 12px 12px;
        margin-bottom: 14px;
        margin-left: auto;
        max-width: 82%;
        font-size: 14px;
        line-height: 1.5;
        box-shadow: 0 1px 2px rgba(0,0,0,0.2);
    }

    /* Data Tags */
    .tag-blue { background: #082f49; color: #38bdf8; border: 1px solid #0369a1; padding: 2px 8px; border-radius: 6px; font-size: 11.5px; font-weight: 700; }
    .tag-green { background: #064e3b; color: #34d399; border: 1px solid #059669; padding: 2px 8px; border-radius: 6px; font-size: 11.5px; font-weight: 700; }
    .tag-purple { background: #3b0764; color: #c084fc; border: 1px solid #7e22ce; padding: 2px 8px; border-radius: 6px; font-size: 11.5px; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# 🗄️ Comprehensive Dubai Enterprise Database (25+ Targets)
# --------------------------------------------------
DUBAI_ENTERPRISE_DATA = [
    {"Company": "Driven Properties", "Category": "Luxury Real Estate", "Location": "Business Bay", "Decision Maker": "Managing Director / Sales Head", "Email": "info@drivenproperties.com", "Phone": "+97144297040", "Ad Spend": "AED 85,000 / mo", "Pain Point": "42% of weekend leads unanswered before 10 AM"},
    {"Company": "bnbme Holiday Homes", "Category": "Holiday Homes & Short Stay", "Location": "Jumeirah Village Circle (JVC)", "Decision Maker": "Head of Guest Reservations", "Email": "reservations@bnbmehomes.com", "Phone": "+971585836263", "Ad Spend": "AED 45,000 / mo", "Pain Point": "Slow pricing response for European & Gulf tourists"},
    {"Company": "Allsopp & Allsopp", "Category": "Residential Brokerage", "Location": "Dubai Marina", "Decision Maker": "Chief Revenue Officer", "Email": "sales@allsoppandallsopp.com", "Phone": "+97144294444", "Ad Spend": "AED 120,000 / mo", "Pain Point": "Brokers overwhelmed by unqualified low-budget inquiries"},
    {"Company": "Deluxe Holiday Homes", "Category": "Vacation Rentals", "Location": "Downtown Dubai", "Decision Maker": "VP of Customer Success", "Email": "info@deluxehomes.com", "Phone": "+97143920202", "Ad Spend": "AED 60,000 / mo", "Pain Point": "Manual booking link generation causes 25% dropoff"},
    {"Company": "Espace Real Estate", "Category": "Luxury Villas & Estates", "Location": "Dubai Hills Estate", "Decision Maker": "Managing Partner", "Email": "info@espace.ae", "Phone": "+97143069999", "Ad Spend": "AED 95,000 / mo", "Pain Point": "High-net-worth cash buyers require instant VIP routing"},
    {"Company": "Frank Porter Vacation Homes", "Category": "Holiday Homes Management", "Location": "DIFC", "Decision Maker": "Operations Director", "Email": "bookings@frankporter.com", "Phone": "+97145897140", "Ad Spend": "AED 50,000 / mo", "Pain Point": "Multi-channel calendar sync delays during high season"},
    {"Company": "D&B Properties", "Category": "Off-Plan Mega Projects", "Location": "Business Bay", "Decision Maker": "Head of Off-Plan Investments", "Email": "inquiry@dandbdubai.com", "Phone": "+97148719200", "Ad Spend": "AED 140,000 / mo", "Pain Point": "Losing Indian & Russian investors due to language friction"},
    {"Company": "Haus & Haus", "Category": "Luxury Residential", "Location": "Dubai Marina", "Decision Maker": "Commercial Director", "Email": "enquiries@hausandhaus.com", "Phone": "+97143025800", "Ad Spend": "AED 110,000 / mo", "Pain Point": "Off-hours WhatsApp inquiries waiting over 35 minutes"},
    {"Company": "Key One Holiday Homes", "Category": "Short-Term Leasing", "Location": "Al Barsha", "Decision Maker": "General Manager", "Email": "info@keyoneholidayhomes.com", "Phone": "+97144471727", "Ad Spend": "AED 35,000 / mo", "Pain Point": "Overdue rental payments require manual follow-up calls"},
    {"Company": "Fam Properties", "Category": "Enterprise Real Estate", "Location": "Business Bay", "Decision Maker": "Chief Marketing Officer", "Email": "info@famproperties.com", "Phone": "+97143691700", "Ad Spend": "AED 250,000 / mo", "Pain Point": "Requires instant API integration with internal CRM"},
    {"Company": "Provident Estate", "Category": "Investment & Luxury", "Location": "Dubai Marina", "Decision Maker": "Sales Director", "Email": "info@providentestate.com", "Phone": "+97143233609", "Ad Spend": "AED 130,000 / mo", "Pain Point": "Need automated ROI calculations in INR, USD, and AED"},
    {"Company": "Silkhaus Stays", "Category": "Corporate Short Stay", "Location": "DIFC", "Decision Maker": "Head of Corporate Bookings", "Email": "concierge@silkhaus.com", "Phone": "+97145789120", "Ad Spend": "AED 75,000 / mo", "Pain Point": "Executive travelers require instant invoice generation"}
]

if 'discovered_leads' not in st.session_state:
    st.session_state.discovered_leads = DUBAI_ENTERPRISE_DATA

if 'bot_config' not in st.session_state:
    st.session_state.bot_config = {
        "persona": "VIP Institutional (فاخر ومقنع)",
        "language_mode": "🌐 Smart Auto-Detect & Live AI Translation",
        "min_budget": 50000,
        "auto_pdf": True,
        "sms_alert": True,
        "auto_booking": True,
        "currency_convert": True,
        "lead_routing": "Senior Luxury Broker (Business Bay Team)"
    }

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [
        {"sender": "user", "text": "Namaste, I saw your Instagram ad for Downtown luxury apartments. Can I know prices for 2BHK with Burj view?"},
        {"sender": "bot", "text": "Namaste ji! 🙏 Welcome to ApexLead Real Estate Dubai. We have 2 exclusive 2BHK units in Downtown with full Burj Khalifa views starting from AED 2.45M (approx ₹5.54 Crore). I have shared the official PDF brochure directly to your chat. Would you prefer a payment plan option or ready-to-move unit?"},
    ]

DEMO_URL = "https://apexlead-dubai-d4paqwmnuacidn564qqnsr.streamlit.app"

# --------------------------------------------------
# 🧭 Sidebar Navigation
# --------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div class="brand-box">
        <span class="brand-logo">⚡</span>
        <div class="brand-text">ApexLead <span>OS</span></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.caption("DUBAI AUTONOMOUS SALES OPERATING SYSTEM")
    st.markdown("---")
    
    menu = st.radio(
        "Navigation",
        [
            "🎯 Enterprise Lead Radar (دليل شركات دبي)",
            "📱 Command & Control Studio (المحاكي وغرفة التحكم)", 
            "📧 Phase 1: AI Email Engine", 
            "💬 Phase 2: WhatsApp Follow-Up", 
            "📊 Executive CRM Pipeline"
        ],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("""
    <div style='font-size:12px; color:#94a3b8;'>
        <b>System Status:</b> <span style='color:#10b981;'>🟢 Active (Dubai Cluster)</span><br>
        <b>Polyglot Matrix:</b> 🇦🇪 🇬🇧 🇮🇳 🇷🇺<br>
        <b>Live Pipeline:</b> AED 14,850,000
    </div>
    """, unsafe_allow_html=True)

# --------------------------------------------------
# 🎯 1. Enterprise Lead Radar Screen (Deep Search)
# --------------------------------------------------
if menu == "🎯 Enterprise Lead Radar (دليل شركات دبي)":
    st.markdown("<h1 style='font-size:26px; font-weight:800; color:#ffffff;'>🎯 Dubai Enterprise Lead Radar & Deep Filter</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94a3b8; font-size:14px; margin-bottom:20px;'>نظام البحث والاستكشاف الشامل لشركات العقارات والشقق الفندقية الكبرى في دبي مع فحص الإنفاق الإعلاني ومواقع القرار</p>", unsafe_allow_html=True)
    
    # KPI Highlights
    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-card">
            <div class="kpi-label">Verified Dubai Targets</div>
            <div class="kpi-value">{len(DUBAI_ENTERPRISE_DATA)} Companies</div>
            <div class="kpi-badge">Enterprise Tiers</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Avg Ad Spend Tracked</div>
            <div class="kpi-value">AED 92,500/mo</div>
            <div class="kpi-badge">Meta & TikTok Ads</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Decision Maker Reach</div>
            <div class="kpi-value">100% C-Level</div>
            <div class="kpi-badge">Direct WhatsApp / Email</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Pipeline Value</div>
            <div class="kpi-value">AED 1.1M+</div>
            <div class="kpi-badge">Annual SaaS Target</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Advanced Multi-Filter Box
    with st.container():
        st.markdown("<div class='enterprise-card'>", unsafe_allow_html=True)
        col_f1, col_f2, col_f3, col_f4 = st.columns([1.5, 1.5, 1.5, 2])
        with col_f1:
            sel_location = st.selectbox("📍 District / Location", ["All Dubai Districts", "Business Bay", "Dubai Marina", "Downtown Dubai", "Jumeirah Village Circle (JVC)", "DIFC", "Dubai Hills Estate", "Al Barsha"])
        with col_f2:
            sel_category = st.selectbox("🏢 Industry Sector", ["All Sectors", "Luxury Real Estate", "Holiday Homes & Short Stay", "Vacation Rentals", "Off-Plan Mega Projects", "Corporate Short Stay"])
        with col_f3:
            sel_adspend = st.selectbox("💰 Est. Monthly Ad Spend", ["All Budgets", "> AED 50,000 / mo", "> AED 100,000 / mo"])
        with col_f4:
            search_query = st.text_input("🔍 Quick Search (Company name, keyword, or pain point)", placeholder="e.g. Driven, Indian, JVC, Marina...")
        st.markdown("</div>", unsafe_allow_html=True)

    # Filter Logic
    filtered_leads = DUBAI_ENTERPRISE_DATA.copy()
    if sel_location != "All Dubai Districts":
        filtered_leads = [l for l in filtered_leads if l['Location'] == sel_location]
    if sel_category != "All Sectors":
        filtered_leads = [l for l in filtered_leads if l['Category'] == sel_category]
    if sel_adspend == "> AED 50,000 / mo":
        filtered_leads = [l for l in filtered_leads if int(l['Ad Spend'].split()[1].replace(',', '')) >= 50000]
    elif sel_adspend == "> AED 100,000 / mo":
        filtered_leads = [l for l in filtered_leads if int(l['Ad Spend'].split()[1].replace(',', '')) >= 100000]
    if search_query:
        q = search_query.lower()
        filtered_leads = [l for l in filtered_leads if q in l['Company'].lower() or q in l['Location'].lower() or q in l['Pain Point'].lower()]

    st.markdown(f"<h3 style='color:#f8fafc; font-size:18px; margin:20px 0 15px;'>📋 Discovered Qualified Enterprises ({len(filtered_leads)} Results)</h3>", unsafe_allow_html=True)

    for idx, lead in enumerate(filtered_leads):
        email_subject = f"تحسين سرعة الاستجابة لعملاء {lead['Company']} ومضاعفة الحجوزات"
        email_body = f"عزيزي فريق {lead['Company']}،\n\nلاحظنا نشاطكم المميز في {lead['Location']}، ونود مشاركة نموذج ApexLead AI المخصص لخدمة عملائكم 24/7 بـ 4 لغات (عربي، هندي، إنجليزي، روسي).\n\nرابط المعاينة الحية:\n{DEMO_URL}"
        mailto_link = f"mailto:{lead['Email']}?subject={urllib.parse.quote(email_subject)}&body={urllib.parse.quote(email_body)}"
        wa_link = f"https://wa.me/{lead['Phone'].replace('+', '').replace(' ', '')}?text={urllib.parse.quote('مرحباً أستاذ / فريق ' + lead['Company'] + '، بخصوص نظام ApexLead AI: ' + DEMO_URL)}"

        st.markdown(f"""
        <div class="enterprise-card">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                <div>
                    <span style="font-size:19px; font-weight:800; color:#ffffff;">{lead['Company']}</span>
                    &nbsp;&nbsp;<span class="tag-blue">{lead['Category']}</span>
                    &nbsp;<span class="tag-green">📍 {lead['Location']}</span>
                </div>
                <div>
                    <span class="tag-purple">💰 {lead['Ad Spend']}</span>
                </div>
            </div>
            <div style="display:grid; grid-template-columns: 2fr 1.2fr; gap:20px; align-items:center;">
                <div>
                    <p style="color:#94a3b8; font-size:13.5px; margin:4px 0;">
                        👤 <b>Decision Maker:</b> {lead['Decision Maker']} &nbsp;|&nbsp; ✉️ <b>Email:</b> <span style="color:#38bdf8;">{lead['Email']}</span> &nbsp;|&nbsp; 📞 <b>Direct:</b> {lead['Phone']}
                    </p>
                    <div style="background:#1e293b; border-left:4px solid #f59e0b; padding:8px 12px; margin-top:8px; font-size:13px; color:#fde68a; border-radius:0 8px 8px 0;">
                        ⚠️ <b>Detected Pain Point:</b> {lead['Pain Point']}
                    </div>
                </div>
                <div style="display:flex; justify-content:flex-end; gap:10px;">
                    <a href="{mailto_link}" class="btn-action-primary">📧 إرسال إيميل رسمي</a>
                    <a href="{wa_link}" target="_blank" class="btn-action-wa">💬 واتساب مباشر</a>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# --------------------------------------------------
# 📱 2. Command & Control Studio Screen
# --------------------------------------------------
elif menu == "📱 Command & Control Studio (المحاكي وغرفة التحكم)":
    st.markdown("<h1 style='font-size:26px; font-weight:800; color:#ffffff;'>📱 Executive Command Studio & Polyglot Simulator</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94a3b8; font-size:14px; margin-bottom:20px;'>غرفة التحكم المؤسسية المتزامنة لحظياً مع محاكي الواتساب الذكي للعملاء متعددي اللغات</p>", unsafe_allow_html=True)
    
    col_sim, col_ctrl = st.columns([1.1, 1.3], gap="large")
    
    # Left: Luxury WhatsApp Simulator
    with col_sim:
        st.markdown("""
        <div class="wa-wrapper">
            <div class="wa-header">
                <div class="wa-avatar">⚡</div>
                <div>
                    <div style="font-weight:700; color:#e9edef; font-size:15px;">ApexLead AI Assistant</div>
                    <div style="font-size:12px; color:#10b981;">Online | Dubai Enterprise Node</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        chat_html = "<div class='wa-body'>"
        for msg in st.session_state.chat_history:
            if msg['sender'] == 'user':
                chat_html += f"<div class='msg-in'><b>العميل:</b><br>{msg['text']}</div>"
            else:
                chat_html += f"<div class='msg-out'><b>ApexLead Agent:</b><br>{msg['text']}</div>"
        chat_html += "</div>"
        st.markdown(chat_html, unsafe_allow_html=True)
        
        with st.form("luxury_chat_form", clear_on_submit=True):
            user_msg = st.text_input("اختبر المحاكاة (اكتب بالهندية، العربية، الإنجليزية، أو الروسية)...", placeholder="e.g. Namaste 2BHK price / بدي شقة بمارينا إيجار سنوي")
            send_btn = st.form_submit_button("إرسال الرسالة 💬", type="primary", use_container_width=True)
            
            if send_btn and user_msg:
                st.session_state.chat_history.append({"sender": "user", "text": user_msg})
                lower_msg = user_msg.lower()
                
                if any(w in lower_msg for w in ["namaste", "bhai", "kya", "crore", "lakh", "hai", "bhk", "india", "paisa"]):
                    reply = "Namaste ji! 🙏 Humare paas prime options available hain. Expected rental ROI is 8-10% tax-free! Main aapko detailed PDF brochure WhatsApp pe share kar raha hoon. Kya kal zoom call ya viewing schedule karein?"
                elif any(w in lower_msg for w in ["здравствуйте", "вилла", "квартира", "дубай", "цена"]):
                    reply = "Здравствуйте! 🌟 Рады приветствовать вас. Эксклюзивные апартаменты в Дубае с доходностью до 9% годовых. Официальный PDF-буклет отправлен в этот чат."
                elif any(w in lower_msg for w in ["طال عمرك", "هلا", "مرحبا", "شيخ", "الغالي", "شلونك"]):
                    reply = "يا مرحبا بك طال عمرك 🌟 طلبك واصل ومحل اهتمامنا. متاح لدينا خيارات VIP راقية جداً في أرقى أبراج دبي. تم تزويدك بملف الـ PDF وتثبيت موعد المعاينة غداً الساعة 4:00 عصراً."
                elif any(w in lower_msg for w in ["hello", "hi", "roi", "downtown", "marina", "invest", "rent"]):
                    reply = "Hello! 🌟 Exclusive luxury units are available matching your exact criteria with flexible payment plans. The official PDF brochure is sent, and a viewing slot has been reserved."
                else:
                    reply = "أهلاً وسهلاً بحضرتك 🌟 تم استلام طلبك وميزانيتك بدقة. جهزنالك أفضل الخيارات المتاحة مع كتالوج الـ PDF الملون وسيتم تأكيد موعد المعاينة وتزويدك بكافة التفاصيل فوراً."
                
                st.session_state.chat_history.append({"sender": "bot", "text": reply})
                st.rerun()

    # Right: Executive Control Center
    with col_ctrl:
        st.markdown("<div class='enterprise-card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='margin-top:0; color:#f8fafc; font-size:18px;'>🎛️ Enterprise Rule Matrix & Policy Engine</h3>", unsafe_allow_html=True)
        st.caption("التحكم الدقيق في سلوك وخوارزميات الذكاء الاصطناعي على مستوى الشركة:")
        
        c_r1, c_r2 = st.columns(2)
        with c_r1:
            st.selectbox("Language Core Engine", ["🌐 Polyglot Auto-Detect (Arabic / Hindi / English / Russian)", "🇦🇪 Gulf Arabic Priority", "🇮🇳 Hinglish Focused", "🇬🇧 English Executive Only"])
            st.selectbox("Sales Velocity Mode", ["Institutional Closer (إغلاق استثماري سريع)", "Warm Hospitality (شقق فندقية)", "Ultra-HNW Concierge (قصور وفلل فاخرة)"])
        with c_r2:
            st.selectbox("Auto-Routing Destination", ["Senior Luxury Broker (Business Bay Desk)", "South Asian / Indian Investor Desk", "Russian VIP Desk", "Short-Stay Leasing Team"])
            st.slider("Min Qualified Budget (AED)", 20000, 300000, 50000, 10000)

        st.markdown("---")
        st.markdown("<b style='color:#cbd5e1; font-size:13.5px;'>Automated Immediate Triggers:</b>", unsafe_allow_html=True)
        c_chk1, c_chk2 = st.columns(2)
        with c_chk1:
            st.checkbox("📄 Instant PDF Brochure Dispatch", value=True)
            st.checkbox("🚨 Instant SMS/Telegram Lead Alert", value=True)
        with c_chk2:
            st.checkbox("📅 Direct Calendly Viewing Sync", value=True)
            st.checkbox("💱 Live Currency Conversion (INR/USD)", value=True)

        if st.button("⚡ تطبيق وتحديث المنظومة لحظياً", type="primary", use_container_width=True):
            st.success("تم تحديث السياسات وتطبيقها فورياً على سيرفرات دبي!")
        st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------------
# 📧 3. Phase 1: AI Email Engine Screen
# --------------------------------------------------
elif menu == "📧 Phase 1: AI Email Engine":
    st.markdown("<h1 style='font-size:26px; font-weight:800; color:#ffffff;'>📧 Phase 1: B2B Enterprise Cold Email Matrix</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94a3b8; font-size:14px; margin-bottom:20px;'>خطابات تنفيذية ذكية وموجهة لأصحاب القرار ومديري المبيعات في كبرى شركات دبي</p>", unsafe_allow_html=True)
    
    for idx, lead in enumerate(DUBAI_ENTERPRISE_DATA[:6]):
        email_subj = f"مضاعفة تحويل إعلانات {lead['Company']} لعملاء العقارات متعددي اللغات (عربي / هندي / إنجليزي)"
        email_body = f"""عزيزي فريق {lead['Company']}،

تحية طيبة وبعد،

في سوق تنافسي واستثماري مثل دبي، تشير البيانات إلى أن أكثر من 65% من المشترين والمستأجرين هم من جنسيات متعددة (خاصة الجالية الهندية والأوروبية والخليجية)، وأن الرد بلغة العميل خلال أول 3 دقائق يرفع نسبة إتمام الصفقات بأكثر من 70%.

لاحظنا تميز نشاطكم في {lead['Location']}، ويسعدنا تقديم ApexLead OS المخصص لنشاطكم:
1. رد فوري 24/7 بـ 4 لغات رئيسية (عربي بلهجاته، هندي Hinglish، إنجليزي، وروسي) خلال 3 ثوانٍ.
2. معالجة الثغرة الشائعة: {lead['Pain Point']}.
3. غرفة تحكم مؤسسية كاملة تتيح لكم تحديد الميزانية وتوجيه الصفقات الساخنة تلقائياً لكبار الوسطاء.

🌐 يمكنكم تجربة النظام وغرفة التحكم التفاعلية متعددة اللغات عبر الرابط المباشر:
{DEMO_URL}

نقدم لشركتكم فترة تجريبية مجانية لمدة 7 أيام لاختبار كفاءة النظام وسرعته عملياً دون أي التزام مالي مسبق.

يسعدنا ترتيب اتصال سريع لمدة 5 دقائق إذا كنتم مهتمين.

وتفضلوا بقبول فائق التقدير والاحترام،
ApexLead Sales Team"""

        mailto_link = f"mailto:{lead['Email']}?subject={urllib.parse.quote(email_subj)}&body={urllib.parse.quote(email_body)}"

        st.markdown(f"""
        <div class="enterprise-card">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                <span style="font-size:18px; font-weight:800; color:#ffffff;">🏢 {lead['Company']}</span>
                <span class="tag-green">📍 {lead['Location']}</span>
            </div>
            <p style="color:#94a3b8; font-size:13px; margin-bottom:12px;">👤 <b>Decision Maker:</b> {lead['Decision Maker']} &nbsp;|&nbsp; ✉️ <b>Target:</b> {lead['Email']}</p>
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div style="font-size:12.5px; color:#38bdf8;">💡 <b>Custom Angle:</b> حل مشكلة {lead['Pain Point']}</div>
                <a href="{mailto_link}" class="btn-action-primary">📧 إرسال إيميل فوري مخصص</a>
            </div>
        </div>
        """, unsafe_allow_html=True)

# --------------------------------------------------
# 💬 4. Phase 2: WhatsApp Follow-Up Screen
# --------------------------------------------------
elif menu == "💬 Phase 2: WhatsApp Follow-Up":
    st.markdown("<h1 style='font-size:26px; font-weight:800; color:#ffffff;'>💬 Phase 2: WhatsApp Executive Follow-Up</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94a3b8; font-size:14px; margin-bottom:20px;'>المتابعة المباشرة عبر الواتساب بعد إرسال البريد الإلكتروني بـ 24 ساعة لرفع معدل تأكيد الصفقات</p>", unsafe_allow_html=True)
    
    for idx, lead in enumerate(DUBAI_ENTERPRISE_DATA[:6]):
        wa_text = f"مرحباً أستاذ / فريق {lead['Company']}، أرسلت لحضرتكم بريداً بالأمس بخصوص نظام ApexLead OS لخدمة عملاء وحجوزات {lead['Company']} بـ 4 لغات (عربي، هندي، إنجليزي، روسي) على مدار 24 ساعة.\n\nرابط التجربة المباشرة:\n{DEMO_URL}\n\nيسعدنا تفعيل الـ 7 أيام التجريبية لكم في أي وقت."
        wa_link = f"https://wa.me/{lead['Phone'].replace('+', '').replace(' ', '')}?text={urllib.parse.quote(wa_text)}"

        st.markdown(f"""
        <div class="enterprise-card">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                <span style="font-size:17px; font-weight:800; color:#ffffff;">🏢 {lead['Company']}</span>
                <span style="color:#10b981; font-size:13px; font-weight:700;">📞 {lead['Phone']}</span>
            </div>
            <p style="color:#cbd5e1; font-size:13px; background:#1e293b; padding:10px; border-radius:8px; margin-bottom:12px;">
                {wa_text.replace(chr(10), '<br>')}
            </p>
            <div style="text-align:right;">
                <a href="{wa_link}" target="_blank" class="btn-action-wa">💬 إرسال متابعة الواتساب</a>
            </div>
        </div>
        """, unsafe_allow_html=True)

# --------------------------------------------------
# 📊 5. Executive CRM Pipeline Screen
# --------------------------------------------------
elif menu == "📊 Executive CRM Pipeline":
    st.markdown("<h1 style='font-size:26px; font-weight:800; color:#ffffff;'>📊 Live Enterprise Pipeline & Conversion Intelligence</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94a3b8; font-size:14px; margin-bottom:20px;'>متابعة حية للصفقات المسحوبة آلياً من محادثات الواتساب مع تصنيف العملات واللغات</p>", unsafe_allow_html=True)
    
    pipeline_df = pd.DataFrame([
        {"Time": "09:40 AM", "Customer": "Rajesh Sharma", "Language": "🇮🇳 Hindi / English", "Property Interest": "2BHK Luxury (Business Bay)", "Budget": "AED 1,850,000 (₹4.2 Cr)", "Grade": "🔥 Ultra Hot", "Status": "Auto-Scheduled Zoom Call"},
        {"Time": "09:15 AM", "Customer": "Tariq Mansoor", "Language": "🇦🇪 Gulf Arabic", "Property Interest": "1-Bed Downtown (Burj View)", "Budget": "AED 120,000 / yr", "Grade": "🔥 Hot Lead", "Status": "Viewing Booked (Tomorrow 4 PM)"},
        {"Time": "08:40 AM", "Customer": "Sarah Jenkins", "Language": "🇬🇧 English", "Property Interest": "Holiday Home (JVC)", "Budget": "AED 8,500 / month", "Grade": "⚡ Qualified", "Status": "Payment Link Dispatched"},
        {"Time": "Yesterday", "Customer": "Dmitry Ivanov", "Language": "🇷🇺 Russian", "Property Interest": "Waterfront Villa (Palm Jumeirah)", "Budget": "AED 18,500,000 ($5.0M)", "Grade": "👑 Ultra VIP", "Status": "Assigned to Managing Partner"}
    ])
    st.dataframe(pipeline_df, use_container_width=True, hide_index=True)

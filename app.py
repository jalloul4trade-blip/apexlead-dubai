import streamlit as st
import pandas as pd
from datetime import datetime
import time
import urllib.parse

st.set_page_config(
    page_title="ApexLead AI | Multilingual Autonomous Sales Engine",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enterprise Multilingual Styling
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp {
        background-color: #f8fafc;
        color: #1e293b;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    .main-title {
        font-size: 26px;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 2px;
    }
    .sub-title {
        font-size: 14px;
        color: #64748b;
        margin-bottom: 20px;
    }
    .portal-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        margin-bottom: 18px;
    }
    .btn-email {
        background-color: #0284c7;
        color: white !important;
        padding: 7px 16px;
        border-radius: 6px;
        text-decoration: none;
        font-weight: 700;
        font-size: 13.5px;
        display: inline-block;
        transition: all 0.2s;
    }
    .btn-email:hover {
        background-color: #0369a1;
    }
    .btn-wa-followup {
        background-color: #25D366;
        color: white !important;
        padding: 7px 16px;
        border-radius: 6px;
        text-decoration: none;
        font-weight: 700;
        font-size: 13.5px;
        display: inline-block;
    }
    .chat-box {
        background: #efeae2;
        border-radius: 12px;
        padding: 18px;
        border: 1px solid #cbd5e1;
        min-height: 420px;
        max-height: 520px;
        overflow-y: auto;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.05);
    }
    .msg-incoming {
        background: #ffffff;
        padding: 10px 14px;
        border-radius: 8px 8px 8px 0px;
        margin-bottom: 12px;
        width: fit-content;
        max-width: 82%;
        font-size: 13.5px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        color: #1e293b;
    }
    .msg-outgoing {
        background: #d9fdd3;
        padding: 10px 14px;
        border-radius: 8px 8px 0px 8px;
        margin-bottom: 12px;
        margin-left: auto;
        width: fit-content;
        max-width: 82%;
        font-size: 13.5px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        color: #1e293b;
    }
    .lang-pill {
        background: #e0f2fe;
        color: #0369a1;
        font-size: 12px;
        font-weight: 700;
        padding: 3px 8px;
        border-radius: 12px;
        margin-right: 4px;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# ⚙️ Session State Configuration
# --------------------------------------------------
if 'bot_config' not in st.session_state:
    st.session_state.bot_config = {
        "persona": "VIP Institutional (فاخر ومقنع)",
        "language_mode": "🌐 Smart Auto-Detect & Live AI Translation",
        "supported_languages": ["العربية (إماراتي / خليجي / شامي)", "English (Dubai Executive)", "Hindi / Hinglish (हिंदी)", "Russian (Русский)"],
        "min_budget": 50000,
        "auto_pdf": True,
        "sms_alert": True,
        "auto_booking": True,
        "currency_convert": True,
        "lead_routing": "Senior Luxury Broker (Business Bay Team)"
    }

if 'leads_list' not in st.session_state:
    st.session_state.leads_list = [
        {"Time": "09:40 AM", "Customer": "Rajesh Sharma", "Language": "🇮🇳 Hindi / English", "Interest": "2BHK Luxury Apartment (Business Bay)", "Budget": "AED 1,850,000 (₹4.2 Cr)", "Status": "🔥 Hot Investor", "Action": "Auto-Sent ROI Sheet + Scheduled Call"},
        {"Time": "09:15 AM", "Customer": "Tariq Mansoor", "Language": "🇦🇪 Arabic (Gulf)", "Interest": "1-Bedroom Luxury Apartment (Downtown)", "Budget": "AED 120,000 / yr", "Status": "🔥 Hot Lead", "Action": "Auto-Booked Viewing (Tomorrow 4 PM)"},
        {"Time": "08:40 AM", "Customer": "Sarah Jenkins", "Language": "🇬🇧 English", "Interest": "Holiday Home / Short Stay (JVC)", "Budget": "AED 8,500 / month", "Status": "⚡ Qualified", "Action": "Auto-Sent Payment Link + PDF"},
        {"Time": "Yesterday", "Customer": "Dmitry Ivanov", "Language": "🇷🇺 Russian", "Interest": "Waterfront Villa (Palm Jumeirah)", "Budget": "AED 18,500,000 ($5.0M)", "Status": "🔥 Ultra VIP", "Action": "Direct VIP Broker Handover via SMS"},
    ]

if 'discovered_leads' not in st.session_state:
    st.session_state.discovered_leads = [
        {"Company": "Driven Properties", "Category": "Luxury Real Estate", "Location": "Business Bay, Dubai", "Decision Maker": "Managing Director / Sales Head", "Email": "info@drivenproperties.com", "Phone": "+97144297040", "Status": "Phase 1: Cold Email ✉️", "Custom Angle": "تحويل زوار إعلانات المشاريع الفاخرة متعددي اللغات (عربي / هندي / إنجليزي) إلى حجوزات فورية"},
        {"Company": "bnbme Holiday Homes", "Category": "Holiday Homes & Short Stay", "Location": "Jumeirah Village Circle (JVC)", "Decision Maker": "Operations & Reservations Manager", "Email": "reservations@bnbmehomes.com", "Phone": "+971585836263", "Status": "Phase 1: Cold Email ✉️", "Custom Angle": "الرد متعدد اللغات على حجوزات السياح والمستأجرين الهنود والأوروبيين 24/7"},
        {"Company": "Allsopp & Allsopp", "Category": "Residential Real Estate", "Location": "Dubai Marina", "Decision Maker": "Head of Digital Lead Generation", "Email": "sales@allsoppandallsopp.com", "Phone": "+97144294444", "Status": "Phase 1: Cold Email ✉️", "Custom Angle": "فرز وتأهيل ميزانيات المستثمرين الدوليين وحساب العملات (AED / INR / USD) تلقائياً"},
        {"Company": "Deluxe Holiday Homes", "Category": "Short-Term Vacation Rentals", "Location": "Downtown Dubai", "Decision Maker": "Guest Relations & Sales Director", "Email": "info@deluxehomes.com", "Phone": "+97143920202", "Status": "Phase 1: Cold Email ✉️", "Custom Angle": "إرسال عروض الأسعار التنافسية باللغة الأم للزائر مع روابط الدفع الذكية"}
    ]

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [
        {"sender": "user", "text": "Namaste, I saw your Instagram ad for Business Bay apartments. Can I know prices for 2BHK?"},
        {"sender": "bot", "text": "Namaste ji! 🙏 Welcome to ApexLead Real Estate Dubai. We have prime 2BHK luxury apartments in Business Bay with Canal views starting from AED 1.85M (approx ₹4.18 Crore). Would you prefer a payment plan option or ready-to-move unit? I can share the complete brochure right here on WhatsApp."},
    ]

DEMO_URL = "https://apexlead-dubai-d4paqwmnuacidn564qqnsr.streamlit.app"

# --------------------------------------------------
# 🧭 Sidebar Navigation
# --------------------------------------------------
with st.sidebar:
    st.markdown("### ⚡ **ApexLead AI**")
    st.caption("Dubai Multilingual Autonomous Sales Portal")
    st.markdown("---")
    menu = st.radio("القائمة الرئيسية", [
        "🎛️ Multilingual AI Studio (غرفة التحكم واللغات)",
        "📱 Live Polyglot WhatsApp (تجربة المحادثة متعددة اللغات)", 
        "📧 Phase 1: AI Email Engine", 
        "💬 Phase 2: WhatsApp Follow-Up", 
        "📊 Live Pipeline CRM"
    ])
    st.markdown("---")
    st.markdown("🌐 **اللغات المدعومة حالياً:**\n`🇦🇪 عربي` `🇬🇧 English` `🇮🇳 हिंदी` `🇷🇺 Русский`")
    st.markdown("---")
    st.info("💡 **رابط الديمو الحي للعملاء:**\n" + DEMO_URL)

# --------------------------------------------------
# 🎛️ 1. Multilingual AI Studio
# --------------------------------------------------
if menu == "🎛️ Multilingual AI Studio (غرفة التحكم واللغات)":
    st.markdown("<div class='main-title'>🎛️ Enterprise Multilingual AI Studio & Polyglot Engine</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>تحكم كامل في الترجمة التلقائية، اللهجات الخليجية والشامية، والهندية الإنجليزية (Hinglish)، وتوزيع اللغات لشركتك</div>", unsafe_allow_html=True)
    
    col_s1, col_s2 = st.columns(2, gap="large")
    
    with col_s1:
        st.markdown("""
        <div class="portal-card">
            <h3 style="margin-top:0; color:#0f172a;">🌐 محرك اللغات والترجمة الذكية (Language Engine)</h3>
            <p style="color:#64748b; font-size:13px;">يتعرف النظام على لغة العميل تلقائياً ويترجم الأسعار والمصطلحات العقارية بالكامل:</p>
        </div>
        """, unsafe_allow_html=True)
        
        cfg_lang_mode = st.selectbox(
            "وضع معالجة اللغات (Language Processing Mode)",
            [
                "🌐 Smart Auto-Detect & Live AI Translation (كشف وترجمة تلقائية فورية)",
                "🇦🇪 Arabic Priority (لهجة خليجية / إماراتية مع تحويل تلقائي)",
                "🇮🇳 Hindi / Hinglish Focused (मल्टीलिंग्वल - للجالية الهندية والمستثمرين)",
                "🇬🇧 English Executive Only (دولي فاخر)",
                "🇷🇺 Russian Priority (مخصص للعملاء الروس ومستثمري النخلة)"
            ],
            index=0
        )
        
        cfg_persona = st.selectbox(
            "نبرة الصوت وأسلوب البيع (Tone of Voice)",
            ["VIP Institutional (فاخر ورسمي)", "Aggressive Closer (إغلاق صفقات واستثمار سريع)", "Warm & Hospitality (ترحيبي ومضياف للشقق الفندقية)", "Corporate Executive (مؤسسي هادئ)"],
            index=0
        )
        
        cfg_curr = st.checkbox("💱 تحويل العملات التلقائي اللحظي (AED ↔ INR ₹ / USD $ / RUB ₽)", value=st.session_state.bot_config.get('currency_convert', True))

    with col_s2:
        st.markdown("""
        <div class="portal-card">
            <h3 style="margin-top:0; color:#0f172a;">⚡ قواعد الفلترة والأتمتة (Qualification & Triggers)</h3>
            <p style="color:#64748b; font-size:13px;">إجراءات تلقائية فورية متعددة القنوات:</p>
        </div>
        """, unsafe_allow_html=True)
        
        cfg_budget = st.slider("الحد الأدنى لميزانية العميل المؤهل (AED Min Budget)", min_value=10000, max_value=200000, value=st.session_state.bot_config['min_budget'], step=5000)
        
        c_t1, c_t2 = st.columns(2)
        with c_t1:
            cfg_pdf = st.checkbox("📄 إرسال بروشور الشقة PDF بلغة العميل فوراً", value=st.session_state.bot_config['auto_pdf'])
            cfg_sms = st.checkbox("🚨 تنبيه SMS فوري لمدير المبيعات", value=st.session_state.bot_config['sms_alert'])
        with c_t2:
            cfg_booking = st.checkbox("📅 تثبيت الموعد بجدول Calendly", value=st.session_state.bot_config['auto_booking'])
            cfg_payment = st.checkbox("💳 توليد رابط حجز دفع فوري", value=True)
        
        cfg_routing = st.selectbox(
            "توجيه الصفقات الساخنة حسب اللغة والمنطقة",
            [
                "South Asian / Indian Investor Desk (Hinglish Team)",
                "Senior Luxury Broker (Business Bay & Downtown Team)",
                "Russian & CIS VIP Investment Team",
                "Short-Stay Reservations Desk (JVC Team)"
            ]
        )

    if st.button("💾 حفظ الإعدادات وتطبيقها لحظياً على محرك الذكاء الاصطناعي", type="primary", use_container_width=True):
        st.session_state.bot_config.update({
            "language_mode": cfg_lang_mode,
            "persona": cfg_persona,
            "min_budget": cfg_budget,
            "auto_pdf": cfg_pdf,
            "sms_alert": cfg_sms,
            "auto_booking": cfg_booking,
            "currency_convert": cfg_curr,
            "lead_routing": cfg_routing
        })
        st.success("تم تحديث مصفوفة اللغات وخوارزمية الذكاء الاصطناعي بنجاح! جرب التحدث بالهندية أو الإنجليزية أو العربية في شاشة المحادثة.")

# --------------------------------------------------
# 📱 2. Live Polyglot WhatsApp Simulation
# --------------------------------------------------
elif menu == "📱 Live Polyglot WhatsApp (تجربة المحادثة متعددة اللغات)":
    st.markdown("<div class='main-title'>📱 Live Multilingual WhatsApp Sales Agent</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>جرب كتابة أي رسالة بأي لغة (هندية، إنجليزية، خليجية، شامية، أو روسية) وشاهد كيف يفهم الذكاء الاصطناعي العميل ويرد بلغته الأم فوراً</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style="margin-bottom:15px;">
        <span class="lang-pill">🇮🇳 Hindi: "Bhai 1BHK price kya hai?"</span>
        <span class="lang-pill">🇦🇪 عربي: "مرحبا طال عمرك، بدي شقة بمارينا"</span>
        <span class="lang-pill">🇬🇧 English: "Hey, what is the ROI on JVC studios?"</span>
        <span class="lang-pill">🇷🇺 Russian: "Здравствуйте, интересует вилла"</span>
    </div>
    """, unsafe_allow_html=True)

    col_chat, col_info = st.columns([1.2, 1], gap="large")
    
    with col_chat:
        st.caption("💬 واجهة العميل التفاعلية (WhatsApp Polyglot Simulator):")
        chat_html = "<div class='chat-box'>"
        for msg in st.session_state.chat_history:
            if msg['sender'] == 'user':
                chat_html += f"<div class='msg-incoming'><b>العميل:</b><br>{msg['text']}</div>"
            else:
                chat_html += f"<div class='msg-outgoing'><b>مساعد المبيعات الذكي (ApexLead):</b><br>{msg['text']}</div>"
        chat_html += "</div>"
        st.markdown(chat_html, unsafe_allow_html=True)
        
        with st.form("interactive_polyglot_form", clear_on_submit=True):
            user_msg = st.text_input("اكتب رسالة بأي لغة لتجربة الترجمة الفورية...", placeholder="e.g. Namaste, I want to invest 1.5 Crore in Dubai or مرحبا بدي شقة إيجار سنوي")
            send_btn = st.form_submit_button("إرسال المحادثة 💬", type="primary", use_container_width=True)
            
            if send_btn and user_msg:
                st.session_state.chat_history.append({"sender": "user", "text": user_msg})
                
                # Smart Multi-lingual Auto-detection & Response Logic
                lower_msg = user_msg.lower()
                
                # Check for Hindi / Hinglish
                if any(w in lower_msg for w in ["namaste", "bhai", "kya", "crore", "lakh", "hai", "bhk", "kaise", "chahiye", "india", "paisa"]):
                    reply = "Namaste ji! 🙏 Humare paas prime options available hain. For investment in Dubai, expected rental ROI is 8-10% tax-free! Main aapko detailed PDF brochure aur payment plan (with INR ₹ conversion) WhatsApp pe share kar raha hoon. Kya hum kal viewing ya zoom call schedule karein?"
                    detected_lang = "🇮🇳 Hindi / Hinglish"
                    lead_budget = "AED 1,500,000 (₹3.4 Cr)"
                    routed_team = "South Asian / Indian Investor Desk"
                
                # Check for Russian
                elif any(w in lower_msg for w in ["здравствуйте", "привет", "вилла", "квартира", "цена", "дубай", "купить"]):
                    reply = "Здравствуйте! 🌟 Рады приветствовать вас в ApexLead Dubai. У нас есть эксклюзивные апартаменты и виллы с доходностью до 9% годовых. Официальный PDF-буклет отправлен. Когда вам будет удобно назначить просмотр?"
                    detected_lang = "🇷🇺 Russian"
                    lead_budget = "AED 3,500,000 ($950K)"
                    routed_team = "Russian & CIS VIP Investment Team"
                
                # Check for English
                elif any(w in lower_msg for w in ["hello", "hi", "hey", "price", "bedroom", "studio", "rent", "invest", "roi", "downtown", "marina", "apartment"]):
                    reply = "Hello and welcome! 🌟 We have exclusive luxury units available with high ROI and flexible payment plans. The official PDF brochure is sent to your chat, and a viewing slot has been reserved for tomorrow. Would you like a virtual tour video as well?"
                    detected_lang = "🇬🇧 English (Executive)"
                    lead_budget = "AED 85,000 / yr"
                    routed_team = "Senior Luxury Broker Team"
                
                # Check for Arabic (Gulf / Emirati)
                elif any(w in lower_msg for w in ["طال عمرك", "هلا", "مرحبا", "شيخ", "الغالي", "شلونك", "كم السعر"]):
                    reply = "يا مرحبا بك طال عمرك 🌟 طلبك واصل ومحل اهتمامنا. متاح لدينا خيارات VIP راقية جداً بتشطيبات ألترا ديلوكس في أرقى مناطق دبي. تم تزويدك بملف الـ PDF وتثبيت موعد المعاينة غداً الساعة 4:00 عصراً."
                    detected_lang = "🇦🇪 Arabic (Gulf VIP)"
                    lead_budget = "AED 120,000 / yr"
                    routed_team = "Senior Luxury Broker Team"
                
                # Arabic Default / Levantine
                else:
                    reply = "أهلاً وسهلاً بحضرتك 🌟 تم استلام طلبك وميزانيتك بدقة متناهية. جهزنالك أفضل الخيارات المتاحة مع كتالوج الـ PDF الملون وسيتم تأكيد موعد المعاينة وتزويدك بكافة التفاصيل فوراً."
                    detected_lang = "🇸🇾 Arabic (Levantine / Standard)"
                    lead_budget = "AED 75,000 / yr"
                    routed_team = "Short-Stay & Leasing Team"

                st.session_state.chat_history.append({"sender": "bot", "text": reply})
                
                # Add to CRM Pipeline
                st.session_state.leads_list.insert(0, {
                    "Time": datetime.now().strftime("%I:%M %p"),
                    "Customer": "Polyglot WhatsApp Lead",
                    "Language": detected_lang,
                    "Interest": f"Auto-Matched Unit ({user_msg[:25]}...)",
                    "Budget": lead_budget,
                    "Status": "🔥 Hot Lead",
                    "Action": f"Routed to: {routed_team}"
                })
                st.rerun()

    with col_info:
        st.markdown(f"""
        <div class="portal-card">
            <h4 style="margin-top:0; color:#0f172a;">⚙️ ميزات الذكاء الاصطناعي النشطة:</h4>
            <table style="width:100%; border-collapse:collapse; font-size:13.5px;">
                <tr style="border-bottom:1px solid #f1f5f9;"><td style="padding:8px 0; color:#64748b;">معالجة اللغات:</td><td><b style="color:#0284c7;">Auto-Detect & Live Polyglot</b></td></tr>
                <tr style="border-bottom:1px solid #f1f5f9;"><td style="padding:8px 0; color:#64748b;">تحويل العملات (INR/USD):</td><td><b>{'🟢 مفعل لحظياً' if st.session_state.bot_config.get('currency_convert', True) else '⚪ معطل'}</b></td></tr>
                <tr style="border-bottom:1px solid #f1f5f9;"><td style="padding:8px 0; color:#64748b;">إرسال البروشور التلقائي:</td><td><b>🟢 مفعل بلغة العميل الأم</b></td></tr>
                <tr style="border-bottom:1px solid #f1f5f9;"><td style="padding:8px 0; color:#64748b;">تنبيهات SMS فورية:</td><td><b>🟢 مفعل لكبار المشترين</b></td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="portal-card" style="background:#f0fdf4; border-color:#bbf7d0;">
            <h4 style="margin-top:0; color:#166534;">🇮🇳 القوة التنافسية للغة الهندية في دبي:</h4>
            <p style="color:#15803d; font-size:13px; line-height:1.6; margin:0;">
                أكثر من <b>40% من مبيعات عقارات دبي</b> تتم مع مستثمرين هنود وجنوب آسيويين. قدرة النظام على الرد الفوري بالـ <b>Hinglish</b> وتحويل المبالغ لـ <b>Crores & Lakhs (₹)</b> تبهر العميل وتغلق الصفقة قبل أي منافس.
            </p>
        </div>
        """, unsafe_allow_html=True)

# --------------------------------------------------
# 📧 3. Phase 1: AI Email Engine
# --------------------------------------------------
elif menu == "📧 Phase 1: AI Email Engine":
    st.markdown("<div class='main-title'>📧 Phase 1: Autonomous B2B Cold Email Generator</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>إرسال عروض رسمية وذكية بالبريد الإلكتروني لأصحاب القرار مع رابط المعاينة التفاعلي</div>", unsafe_allow_html=True)
    
    for idx, lead in enumerate(st.session_state.discovered_leads):
        email_subject = f"مضاعفة حجوزات ومبيعات عملاء {lead['Company']} متعددي اللغات (عربي / هندي / إنجليزي)"
        
        email_body = f"""عزيزي فريق {lead['Company']}،

تحية طيبة وبعد،

في سوق عالمي وتنافسي مثل دبي، تشير البيانات إلى أن أكثر من 65% من المشترين والمستأجرين هم من جنسيات متعددة (خاصة الجالية الهندية والأوروبية والخليجية)، وأن الرد بلغة العميل خلال أول 3 دقائق يرفع نسبة إتمام الصفقات بأكثر من 70%.

لاحظنا نشاطكم المميز في {lead['Location']}، ويسعدنا تقديم ApexLead AI المخصص لنشاطكم:
1. رد فوري 24/7 بـ 5 لغات (عربي بلهجاته، هندي Hinglish، إنجليزي، وروسي) خلال 3 ثوانٍ.
2. تحويل تلقائي للمبالغ بالعملات المفضلة (AED / INR ₹ / USD $).
3. غرفة تحكم كاملة تتيح لكم تحديد اللهجة، الميزانية، وتوجيه الصفقات الساخنة تلقائياً.

🌐 يمكنكم تجربة النظام وغرفة التحكم التفاعلية متعددة اللغات عبر الرابط المباشر:
{DEMO_URL}

نقدم لشركتكم فترة تجريبية مجانية لمدة 7 أيام لاختبار كفاءة النظام وسرعته عملياً دون أي التزام مالي مسبق.

يسعدنا ترتيب اتصال سريع لمدة 5 دقائق إذا كنتم مهتمين.

وتفضلوا بقبول فائق التقدير والاحترام،
ApexLead Sales Team"""

        encoded_subject = urllib.parse.quote(email_subject)
        encoded_body = urllib.parse.quote(email_body)
        mailto_link = f"mailto:{lead['Email']}?subject={encoded_subject}&body={encoded_body}"

        with st.container():
            st.markdown(f"""
            <div class="portal-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <h3 style="margin:0; color:#0f172a;">🏢 {lead['Company']} <span style="font-size:13px; background:#f1f5f9; color:#475569; padding:3px 8px; border-radius:6px;">{lead['Category']}</span></h3>
                    <span style="background:#e0f2fe; color:#0369a1; border:1px solid #bae6fd; padding:4px 10px; border-radius:6px; font-weight:700; font-size:12px;">{lead['Status']}</span>
                </div>
                <p style="color:#64748b; font-size:13.5px; margin:8px 0;">
                    📍 <b>Location:</b> {lead['Location']} | 👤 <b>Target:</b> {lead['Decision Maker']} | ✉️ <b>Email:</b> {lead['Email']}
                </p>
                <div style="background:#f8fafc; border-left:4px solid #0284c7; padding:8px 12px; margin:10px 0; font-size:13px; color:#334155;">
                    💡 <b>زاوية العرض:</b> {lead['Custom Angle']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            c_p1, c_p2 = st.columns([4, 1.3])
            with c_p1:
                with st.expander("📄 معاينة نص الإيميل الرسمي المخصص"):
                    st.text_area("نص البريد الإلكتروني الجاهز:", f"الموضوع: {email_subject}\n\n{email_body}", height=160, key=f"email_area_{idx}")
            with c_p2:
                st.write("")
                st.markdown(f'<a href="{mailto_link}" class="btn-email">📧 إرسال إيميل فوري</a>', unsafe_allow_html=True)

# --------------------------------------------------
# 💬 4. Phase 2: WhatsApp Follow-Up
# --------------------------------------------------
elif menu == "💬 Phase 2: WhatsApp Follow-Up":
    st.markdown("<div class='main-title'>💬 Phase 2: WhatsApp Follow-Up (بعد الإيميل بـ 24 ساعة)</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>رسائل تذكير لطيفة ومباشرة لرفع نسبة التفاعل وتأكيد موعد العرض الحي</div>", unsafe_allow_html=True)
    
    for idx, lead in enumerate(st.session_state.discovered_leads):
        wa_followup = f"""مرحباً أستاذ / فريق {lead['Company']}،
أتمنى أن تكونوا بخير.

أرسلت لحضرتكم بريداً إلكترونياً بالأمس بخصوص نظام ApexLead AI لخدمة عملاء وحجوزات {lead['Company']} بـ 5 لغات (عربي، هندي، إنجليزي) على مدار 24 ساعة.

أحببت مشاركة رابط التجربة التفاعلية المباشرة معكم هنا أيضاً:
{DEMO_URL}

هل كان لديكم دقيقة للاطلاع عليه؟ ويسعدني تفعيل الـ 7 أيام التجريبية لكم في أي وقت يناسبكم."""

        encoded_wa = urllib.parse.quote(wa_followup)
        wa_link = f"https://wa.me/{lead['Phone'].replace('+', '').replace(' ', '')}?text={encoded_wa}"

        with st.container():
            st.markdown(f"""
            <div class="portal-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <h4 style="margin:0; color:#0f172a;">🏢 {lead['Company']} — WhatsApp Follow-Up</h4>
                    <span style="color:#64748b; font-size:13px;">📞 {lead['Phone']}</span>
                </div>
                <p style="color:#475569; font-size:13.5px; margin:8px 0; background:#f0fdf4; padding:10px; border-radius:8px; border:1px solid #bbf7d0;">
                    {wa_followup.replace(chr(10), '<br>')}
                </p>
                <div style="text-align:right;">
                    <a href="{wa_link}" target="_blank" class="btn-wa-followup">💬 إرسال متابعة واتساب</a>
                </div>
            </div>
            """, unsafe_allow_html=True)

# --------------------------------------------------
# 📊 5. Live Pipeline CRM
# --------------------------------------------------
elif menu == "📊 Live Pipeline CRM":
    st.markdown("<div class='main-title'>📊 Live Client Pipeline & Conversion Analytics</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>لوحة تحكم الشركة لمتابعة الصفقات، اللغات المكتشفة، وحجوزات المعاينة وتوجيه المستثمرين الدوليين</div>", unsafe_allow_html=True)
    
    df_leads = pd.DataFrame(st.session_state.leads_list)
    st.dataframe(df_leads, use_container_width=True, hide_index=True)

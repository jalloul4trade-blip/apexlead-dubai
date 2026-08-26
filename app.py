import streamlit as st
import pandas as pd
from datetime import datetime
import time
import urllib.parse

st.set_page_config(
    page_title="ApexLead AI | Autonomous Lead Hunter & Sales System",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS Styling
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
        padding: 22px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .btn-wa {
        background-color: #25D366;
        color: white !important;
        padding: 6px 14px;
        border-radius: 6px;
        text-decoration: none;
        font-weight: 700;
        font-size: 13px;
        display: inline-block;
    }
    .chat-box {
        background: #efeae2;
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #cbd5e1;
        min-height: 380px;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.05);
    }
    .msg-incoming {
        background: #ffffff;
        padding: 10px 14px;
        border-radius: 8px 8px 8px 0px;
        margin-bottom: 12px;
        width: fit-content;
        max-width: 80%;
        font-size: 14px;
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
        max-width: 80%;
        font-size: 14px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        color: #1e293b;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# 🗄️ Database & Discovered Leads Storage
# --------------------------------------------------
if 'discovered_leads' not in st.session_state:
    st.session_state.discovered_leads = [
        {
            "Company": "Driven Properties",
            "Category": "Luxury Real Estate",
            "Location": "Business Bay, Dubai",
            "Decision Maker": "Managing Director / Sales Head",
            "Contact Phone": "+97144297040",
            "Status": "Ready for Pitch 🎯",
            "Target Pain": "Losing 40% of Instagram ad leads after 8 PM"
        },
        {
            "Company": "bnbme Holiday Homes",
            "Category": "Holiday Homes & Short Stay",
            "Location": "Jumeirah Village Circle (JVC)",
            "Decision Maker": "Operations & Bookings Manager",
            "Contact Phone": "+971585836263",
            "Status": "Ready for Pitch 🎯",
            "Target Pain": "Delayed responses to weekend booking inquiries"
        },
        {
            "Company": "Allsopp & Allsopp",
            "Category": "Residential Real Estate",
            "Location": "Dubai Marina",
            "Decision Maker": "Head of Digital Lead Generation",
            "Contact Phone": "+97144294444",
            "Status": "Ready for Pitch 🎯",
            "Target Pain": "Need automated budget qualification before broker calls"
        },
        {
            "Company": "Deluxe Holiday Homes",
            "Category": "Short-Term Vacation Rentals",
            "Location": "Downtown Dubai",
            "Decision Maker": "Guest Relations & Sales Director",
            "Contact Phone": "+97143920202",
            "Status": "Ready for Pitch 🎯",
            "Target Pain": "Manual pricing negotiations taking over 2 hours"
        }
    ]

DEMO_URL = "https://apexlead-dubai-d4paqwmnuacidn564qqnsr.streamlit.app"

# --------------------------------------------------
# 🧭 Sidebar Navigation
# --------------------------------------------------
with st.sidebar:
    st.markdown("### ⚡ **ApexLead System**")
    st.caption("Dubai Autonomous Sales Engine")
    st.markdown("---")
    menu = st.radio("Navigation", ["🎯 AI Lead Hunter (Autonomous)", "📱 Customer Experience Demo", "📊 Live CRM & Pipeline"])
    st.markdown("---")
    st.info("💡 **Active Live Demo:**\n" + DEMO_URL)

# --------------------------------------------------
# 🎯 1. Autonomous Lead Hunter Screen
# --------------------------------------------------
if menu == "🎯 AI Lead Hunter (Autonomous)":
    st.markdown("<div class='main-title'>🎯 Autonomous Dubai Lead Hunter & Pitch Generator</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>النظام يبحث ذاتياً عن شركات دبي ويولد عروضاً بيعية مخصصة مع رابط المعاينة الحية</div>", unsafe_allow_html=True)
    
    col_c1, col_c2, col_c3 = st.columns([1.5, 1.5, 1])
    with col_c1:
        target_sector = st.selectbox("Select Target Sector in Dubai", ["Holiday Homes & Short Stay", "Luxury Real Estate Agencies", "Car Rental & Chauffeur Services", "Aesthetic Clinics & Wellness"])
    with col_c2:
        target_area = st.selectbox("Target Location", ["All Dubai", "Business Bay & Downtown", "JVC & Dubai Hills", "Dubai Marina & Palm Jumeirah"])
    with col_c3:
        st.write("")
        st.write("")
        if st.button("🚀 تشغيل الرادار والبحث الذاتي", type="primary", use_container_width=True):
            with st.spinner("جارٍ مسح السوق وتحليل شركات دبي وصياغة العروض المخصصة..."):
                time.sleep(2)
                st.success("تم اكتشاف شركات مؤهلة وتجهيز خطابات المبيعات الذكية فوراً!")

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader(f"📋 Discovered High-Value Leads in {target_area}")

    for idx, lead in enumerate(st.session_state.discovered_leads):
        with st.container():
            st.markdown(f"""
            <div class="portal-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <h3 style="margin:0; color:#0f172a;">🏢 {lead['Company']} <span style="font-size:13px; background:#f1f5f9; color:#475569; padding:3px 8px; border-radius:6px;">{lead['Category']}</span></h3>
                    <span style="background:#ecfdf5; color:#059669; border:1px solid #a7f3d0; padding:4px 10px; border-radius:6px; font-weight:700; font-size:12px;">{lead['Status']}</span>
                </div>
                <p style="color:#64748b; font-size:13.5px; margin:8px 0;">
                    📍 <b>Location:</b> {lead['Location']} | 👤 <b>Target:</b> {lead['Decision Maker']} | 📞 <b>Phone:</b> {lead['Contact Phone']}
                </p>
                <div style="background:#fffbeb; border-left:4px solid #f59e0b; padding:8px 12px; margin:10px 0; font-size:13px; color:#b45309;">
                    💡 <b>الثغرة المكتشفة بالذكاء الاصطناعي:</b> {lead['Target Pain']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            pitch_text = f"""مرحباً فريق {lead['Company']}،
لاحظنا تميز نشاطكم في {lead['Location']}.
في ظل التنافس العالي، تشير بيانات دبي إلى أن التأخر في الرد على إعلانات الواتساب لأكثر من 3 دقائق يفقدكم حتى 40% من العملاء الجادين.

قمنا بتطوير ApexLead AI لخدمة عملائكم:
1. رد فوري 24/7 بالعربية والإنجليزية خلال 3 ثوانٍ.
2. فرز ميزانية العميل وتحديد نوع الطلب تلقائياً.
3. حجز موعد المعاينة وتثبيته مباشرة.

🔗 شاهد النظام وهو يعمل وكأنك عميل لشركتكم:
{DEMO_URL}

هل يناسبكم تفعيل تجربة مجانية لمدة 7 أيام لنشاطكم لاختبار سرعة إغلاق الصفقات؟"""

            encoded_msg = urllib.parse.quote(pitch_text)
            wa_link = f"https://wa.me/{lead['Contact Phone'].replace('+', '').replace(' ', '')}?text={encoded_msg}"
            
            c_p1, c_p2 = st.columns([4, 1.2])
            with c_p1:
                with st.expander("📄 معاينة خطاب المبيعات الذكي المخصص لهذه الشركة (Custom AI Pitch)"):
                    st.text_area("رسالة العرض الجاهزة:", pitch_text, height=160, key=f"pitch_area_{idx}")
            with c_p2:
                st.write("")
                st.markdown(f'<a href="{wa_link}" target="_blank" class="btn-wa">💬 إرسال واتساب فوري</a>', unsafe_allow_html=True)

# --------------------------------------------------
# 📱 2. Customer Experience Demo Screen
# --------------------------------------------------
elif menu == "📱 Customer Experience Demo":
    st.markdown("<div class='main-title'>📱 Interactive WhatsApp Simulator</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>هذا هو النموذج التفاعلي الذي يراه العميل عند فتح الرابط</div>", unsafe_allow_html=True)
    
    col_chat, col_info = st.columns([1.2, 1], gap="large")
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = [
            {"sender": "user", "text": "مرحباً، شفت إعلانكم على إنستغرام بخصوص الشقق الفندقية في JVC، في مجال استفسر؟"},
            {"sender": "bot", "text": "أهلاً بك! يسعدنا خدمتك عبر ApexLead AI 🌟 نعم متاح لدينا شقق فندقية مجهزة بالكامل ومطابقة لأعلى معايير الراحة. هل تبحث عن إيجار شهري أم سنوي؟ وكم عدد الغرف المفضل؟"},
        ]

    with col_chat:
        chat_html = "<div class='chat-box'>"
        for msg in st.session_state.chat_history:
            if msg['sender'] == 'user':
                chat_html += f"<div class='msg-incoming'><b>العميل:</b><br>{msg['text']}</div>"
            else:
                chat_html += f"<div class='msg-outgoing'><b>مساعد المبيعات الذكي (ApexLead):</b><br>{msg['text']}</div>"
        chat_html += "</div>"
        st.markdown(chat_html, unsafe_allow_html=True)
        
        with st.form("demo_chat_form", clear_on_submit=True):
            user_msg = st.text_input("اكتب رد العميل للتجربة...", placeholder="مثال: بدي شقة غرفتين وصالة مفروشة")
            if st.form_submit_button("إرسال المحادثة 💬", type="primary", use_container_width=True) and user_msg:
                st.session_state.chat_history.append({"sender": "user", "text": user_msg})
                st.session_state.chat_history.append({"sender": "bot", "text": "تم تسجيل طلبك بدقة وتحديد خيارات مناسبة في أرقى أبراج المنطقة. سيتم تأكيد موعد المعاينة وإرسال اللوكيشن لك عبر هذا الرقم فوراً 🌟"})
                st.rerun()

    with col_info:
        st.markdown("""
        <div class="portal-card">
            <h4>💡 ميزات النظام لشركات دبي:</h4>
            <p style="color:#64748b; font-size:14px; line-height:1.7;">
                • استجابة فورية خلال 3 ثوانٍ على مدار 24 ساعة.<br>
                • لا يتطلب أي تدريب لموظفي الشركة.<br>
                • جاهز للتكامل المباشر مع أرقام الواتساب الرسمية (WhatsApp Business API).
            </p>
        </div>
        """, unsafe_allow_html=True)

# --------------------------------------------------
# 📊 3. Live CRM & Pipeline Screen
# --------------------------------------------------
elif menu == "📊 Live CRM & Pipeline":
    st.markdown("<div class='main-title'>📊 Live Client Pipeline & Conversion Analytics</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>لوحة تحكم الشركة لمتابعة الصفقات وحجوزات المعاينة الفورية</div>", unsafe_allow_html=True)
    
    leads_data = [
        {"Time": "09:15 AM", "Customer": "Tariq Mansoor", "Phone": "+971 50 841 9921", "Interest": "1-Bedroom Luxury Apartment (Downtown)", "Budget": "AED 120,000 / yr", "Status": "🔥 Hot Lead", "Action": "Booked Viewing (Tomorrow 4 PM)"},
        {"Time": "08:40 AM", "Customer": "Sarah Jenkins", "Phone": "+971 52 119 4022", "Interest": "Holiday Home / Short Stay (JVC)", "Budget": "AED 8,500 / month", "Status": "⚡ Qualified", "Action": "Sent Payment Link"},
        {"Time": "Yesterday", "Customer": "Khalid Al-Hashemi", "Phone": "+971 55 901 3341", "Interest": "Villa for Investment (Dubai Hills)", "Budget": "AED 4.2M Cash", "Status": "🔥 Hot Lead", "Action": "Assigned to Senior Broker"},
    ]
    st.dataframe(pd.DataFrame(leads_data), use_container_width=True, hide_index=True)

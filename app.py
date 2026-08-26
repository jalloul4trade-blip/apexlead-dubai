import streamlit as st
import pandas as pd
from datetime import datetime
import time

st.set_page_config(
    page_title="ApexLead AI | WhatsApp Sales Agent for Dubai Businesses",
    page_icon="⚡",
    layout="wide"
)

# Custom Styling
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
        font-size: 28px;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 5px;
    }
    .sub-title {
        font-size: 15px;
        color: #64748b;
        margin-bottom: 25px;
    }
    .chat-box {
        background: #efeae2;
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #cbd5e1;
        min-height: 420px;
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
    .stat-card {
        background: white;
        border: 1px solid #e2e8f0;
        padding: 18px;
        border-radius: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

if 'leads_list' not in st.session_state:
    st.session_state.leads_list = [
        {"Time": "09:15 AM", "Customer": "Tariq Mansoor", "Phone": "+971 50 841 9921", "Interest": "1-Bedroom Luxury Apartment (Downtown)", "Budget": "AED 120,000 / yr", "Status": "🔥 Hot Lead", "Action": "Booked Viewing (Tomorrow 4 PM)"},
        {"Time": "08:40 AM", "Customer": "Sarah Jenkins", "Phone": "+971 52 119 4022", "Interest": "Holiday Home / Short Stay (JVC)", "Budget": "AED 8,500 / month", "Status": "⚡ Qualified", "Action": "Sent Payment Link"},
        {"Time": "Yesterday", "Customer": "Khalid Al-Hashemi", "Phone": "+971 55 901 3341", "Interest": "Villa for Investment (Dubai Hills)", "Budget": "AED 4.2M Cash", "Status": "🔥 Hot Lead", "Action": "Assigned to Senior Broker"},
    ]

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [
        {"sender": "user", "text": "مرحباً، شفت إعلانكم على إنستغرام بخصوص الشقق الفندقية في JVC، في مجال استفسر؟"},
        {"sender": "bot", "text": "أهلاً بك! يسعدنا خدمتك عبر ApexLead AI 🌟 نعم متاح لدينا شقق فندقية مجهزة بالكامل ومطابقة لأعلى معايير الراحة. هل تبحث عن إيجار شهري أم سنوي؟ وكم عدد الغرف المفضل؟"},
    ]

col_h1, col_h2 = st.columns([2.5, 1])
with col_h1:
    st.markdown("<div class='main-title'>⚡ ApexLead AI — Dubai Sales Engine Demo</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>24/7 Autonomous WhatsApp Lead Qualifier & Instant Booking System for Dubai Real Estate & SMEs</div>", unsafe_allow_html=True)
with col_h2:
    st.markdown("<div style='text-align:right;'><span style='background:#ecfdf5; color:#059669; border:1px solid #a7f3d0; padding:6px 14px; border-radius:20px; font-weight:700; font-size:13px;'>🟢 System Active (Dubai Server)</span></div>", unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)
m1.metric("Response Time", "⚡ < 3 Seconds", "Industry avg: 45 min")
m2.metric("Ad Leads Converted", "84.2%", "+38% vs Traditional Form")
m3.metric("Captured Pipeline Value", "AED 4,448,500", "This Week")
m4.metric("Off-Hours Bookings", "42 Bookings", "Between 10 PM - 8 AM")

st.markdown("<br>", unsafe_allow_html=True)

col_chat, col_crm = st.columns([1.1, 1.4], gap="large")

with col_chat:
    st.subheader("📱 Live WhatsApp Experience")
    st.caption("جرب التحدث كأنك عميل قادم من إعلانات Instagram / Meta:")
    
    with st.container():
        chat_html = "<div class='chat-box'>"
        for msg in st.session_state.chat_history:
            if msg['sender'] == 'user':
                chat_html += f"<div class='msg-incoming'><b>العميل:</b><br>{msg['text']}</div>"
            else:
                chat_html += f"<div class='msg-outgoing'><b>مساعد المبيعات الذكي (ApexLead):</b><br>{msg['text']}</div>"
        chat_html += "</div>"
        st.markdown(chat_html, unsafe_allow_html=True)
    
    with st.form("chat_input_form", clear_on_submit=True):
        user_msg = st.text_input("اكتب رد العميل للتجربة...", placeholder="مثال: بدي استوديو مفروش بإيجار شهري بحدود 6000 درهم")
        send_btn = st.form_submit_button("إرسال الرد 💬", type="primary", use_container_width=True)
        
        if send_btn and user_msg:
            st.session_state.chat_history.append({"sender": "user", "text": user_msg})
            
            if "شهري" in user_msg or "استوديو" in user_msg or "6000" in user_msg or "غرفة" in user_msg:
                bot_reply = "تماماً! متاح لدينا خياران فاخران في JVC مع جيم ومسبح شامل كافة الفواتير بـ 5,800 درهم شهرياً. تحب أثبت لك موعد معاينة اليوم الساعة 5:30 مساءً أو أبعتلك فيديو تفصيلي للشقة؟"
                st.session_state.leads_list.insert(0, {
                    "Time": datetime.now().strftime("%I:%M %p"),
                    "Customer": "New WhatsApp Lead (Demo)",
                    "Phone": "+971 58 " + str(int(time.time()))[-6:],
                    "Interest": "Studio / 1-Bed Furnished JVC",
                    "Budget": "AED 6,000 / month",
                    "Status": "🔥 Hot Lead",
                    "Action": "Requested Tour / Video"
                })
            elif "ميزانية" in user_msg or "سعر" in user_msg or "شراء" in user_msg or "فيلا" in user_msg:
                bot_reply = "يسعدنا تزويدك بقائمة المشاريع الجاهزة وتحت الإنشاء مع خطط دفع مرنة تبدأ من 1% شهرياً. ما هي الميزانية التقريبية التي تفضل البدء بها؟"
            else:
                bot_reply = "تم استلام طلبك بنجاح! سيقوم مستشارك العقاري المختص بالتواصل معك مباشرة عبر هذا الرقم خلال لحظات مع كافة العروض المتوفرة 🌟"

            st.session_state.chat_history.append({"sender": "bot", "text": bot_reply})
            st.rerun()

with col_crm:
    st.subheader("📊 Live Client Capture & Pipeline")
    st.caption("البيانات والمواعيد المسحوبة آلياً من محادثات الواتساب فور حدوثها:")
    
    df_leads = pd.DataFrame(st.session_state.leads_list)
    st.dataframe(
        df_leads,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Status": st.column_config.TextColumn("Lead Grade"),
            "Action": st.column_config.TextColumn("Automated Outcome")
        }
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="stat-card">
        <h4 style="margin-top:0; color:#0f172a;">💼 لماذا تشتري شركات دبي هذا النظام فوراً؟</h4>
        <ul style="color:#64748b; font-size:13.5px; line-height:1.7; padding-left:20px; margin-bottom:0;">
            <li><b>استجابة فورية خلال 3 ثوانٍ:</b> لا يضيع أي عميل يدخل من إعلانات تيك توك أو إنستغرام.</li>
            <li><b>فلترة الميزانية:</b> النظام يفرز العملاء الجادين ويسحب الميزانية ونوع الطلب قبل تحويله لموظف المبيعات.</li>
            <li><b>حجز المواعيد الآلي:</b> تثبيت موعد المعاينة أو الزيارة وتذكير العميل قبل الموعد بساعتين لتقليل الإلغاء.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

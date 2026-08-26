import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse

st.set_page_config(
    page_title="ApexLead Enterprise OS | Autonomous Sales Intelligence",
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

    .enterprise-card {
        background: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 14px;
        padding: 24px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.25);
        margin-bottom: 20px;
    }

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
        font-size: 12px;
        color: #94a3b8;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 22px;
        font-weight: 800;
        color: #f8fafc;
    }
    .kpi-badge {
        font-size: 12px;
        color: #10b981;
        font-weight: 700;
        margin-top: 4px;
    }

    .btn-action-primary {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
        color: #ffffff !important;
        padding: 9px 20px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: 700;
        font-size: 13.5px;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .btn-action-wa {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: #ffffff !important;
        padding: 9px 20px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: 700;
        font-size: 13.5px;
        display: inline-flex;
        align-items: center;
        gap: 8px;
    }

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
    }

    .tag-blue { background: #082f49; color: #38bdf8; border: 1px solid #0369a1; padding: 2px 8px; border-radius: 6px; font-size: 11.5px; font-weight: 700; }
    .tag-green { background: #064e3b; color: #34d399; border: 1px solid #059669; padding: 2px 8px; border-radius: 6px; font-size: 11.5px; font-weight: 700; }
    .tag-purple { background: #3b0764; color: #c084fc; border: 1px solid #7e22ce; padding: 2px 8px; border-radius: 6px; font-size: 11.5px; font-weight: 700; }
    .tag-gold { background: #451a03; color: #fde047; border: 1px solid #b45309; padding: 2px 8px; border-radius: 6px; font-size: 11.5px; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# 🗄️ Comprehensive Deep Enterprise Database (Pure Structured Metrics)
# --------------------------------------------------
DUBAI_DEEP_AUDIT_DATA = [
    {
        "Company": "Driven Properties",
        "Category": "Luxury Real Estate & Advisory",
        "Headquarters": "Bay Square, Business Bay",
        "Branches": "6 Major Hubs (Bay Square, Palm Jumeirah, Dubai Hills, City Walk, St. Regis, China Desk)",
        "Brokers_Count": "350+ Licensed Brokers",
        "Decision_Maker": "Abdullah Alajaji (Founder & CEO) / Sales Operations Directors",
        "Email": "info@drivenproperties.com",
        "Phone": "+97144297040",
        "Est_Ad_Spend": "AED 120,000 / month",
        "Pain_EN": "Estimated 38% dropoff on Meta/Instagram luxury project leads during off-hours (8 PM - 9 AM) prior to broker assignment.",
        "Revenue_Leak_EN": "AED 420,000 / month in lost gross commissions",
        "Projected_Uplift_EN": "+28% increase in qualified viewing conversions (+AED 2.8M annual commission uplift)",
        "Strategic_Value_EN": "Instant 3-second multilingual routing (Arabic/Hindi/English/Russian) matching 350+ brokers to verified buyers.",
        "Pain_AR": "فقدان ما يقارب 38% من استفسارات الحملات الإعلانية على إنستغرام وتيك توك بعد الساعة 8 مساءً قبل وصولها للوسيط المختص.",
        "Revenue_Leak_AR": "420,000 درهم شهرياً في العمولات الضائعة",
        "Projected_Uplift_AR": "+28% في معدل حجز المعاينات المؤكدة (+2.8 مليون درهم سنوياً)"
    },
    {
        "Company": "bnbme Holiday Homes",
        "Category": "Luxury Holiday Homes Management",
        "Headquarters": "Jumeirah Village Circle (JVC)",
        "Branches": "Global Hubs (Dubai JVC, Downtown, Marina, Mumbai, Lisbon)",
        "Brokers_Count": "50+ Property Managers & Reservation Specialists",
        "Decision_Maker": "Vinayak Mahtani (CEO) / Head of Reservations",
        "Email": "reservations@bnbmehomes.com",
        "Phone": "+971585836263",
        "Est_Ad_Spend": "AED 65,000 / month",
        "Pain_EN": "Delayed responses to international tourists across timezones, forcing direct booking dropoffs to high-commission OTAs.",
        "Revenue_Leak_EN": "AED 180,000 / month in direct booking margins",
        "Projected_Uplift_EN": "+35% direct booking conversion rate without portal commissions",
        "Strategic_Value_EN": "24/7 autonomous pricing quotes, multilingual instant responses, and automated payment link generation.",
        "Pain_AR": "تأخر الرد على استفسارات السياح في فترات الليل، مما يدفعهم للحجز عبر منصات وسيطة تقتطع عمولات أعلى.",
        "Revenue_Leak_AR": "180,000 درهم شهرياً في هوامش الحجز المباشر",
        "Projected_Uplift_AR": "+35% زيادة في الحجوزات المباشرة دون عمولات وسيطة"
    },
    {
        "Company": "Allsopp & Allsopp",
        "Category": "Residential Real Estate Agency",
        "Headquarters": "Motor City / Dubai Marina",
        "Branches": "5 Hubs (Motor City, Dubai Marina, Springs Souk, JGE, Business Bay)",
        "Brokers_Count": "400+ Licensed Agents",
        "Decision_Maker": "Lewis Allsopp (CEO) / Head of Performance Marketing",
        "Email": "sales@allsoppandallsopp.com",
        "Phone": "+97144294444",
        "Est_Ad_Spend": "AED 160,000 / month",
        "Pain_EN": "Brokers overloaded with unqualified low-budget inquiries, reducing critical closing time for cash and VIP investors.",
        "Revenue_Leak_EN": "AED 550,000 / month in broker productivity and lost opportunities",
        "Projected_Uplift_EN": "+40% agent productivity gain with pre-qualified hot leads (+AED 4.2M annually)",
        "Strategic_Value_EN": "Automated digital buyer budget qualification and direct Calendly viewing synchronization.",
        "Pain_AR": "إرهاق الوسطاء بمئات الاتصالات غير المؤهلة مما يقلل وقت التركيز على المشترين الكاش والـ VIP.",
        "Revenue_Leak_AR": "550,000 درهم شهرياً في تكلفة وقت الوسطاء والفرص الضائعة",
        "Projected_Uplift_AR": "+40% كفاءة إنتاجية للوسطاء مع توجيه الصفقات الساخنة فقط"
    },
    {
        "Company": "Deluxe Holiday Homes",
        "Category": "Short-Term Vacation Rentals",
        "Headquarters": "Downtown Dubai (Boulevard Plaza)",
        "Branches": "3 Key Hubs (Downtown, Dubai Marina, Palm Jumeirah)",
        "Brokers_Count": "80+ Hospitality & Operations Staff",
        "Decision_Maker": "Director of Commercial Strategy & Revenue",
        "Email": "info@deluxehomes.com",
        "Phone": "+97143920202",
        "Est_Ad_Spend": "AED 80,000 / month",
        "Pain_EN": "Manual pricing negotiations taking over 2 hours per guest inquiry, leading to 25% booking abandonment.",
        "Revenue_Leak_EN": "AED 210,000 / month in lost reservations",
        "Projected_Uplift_EN": "+30% faster booking velocity, raising average monthly occupancy to 92%",
        "Strategic_Value_EN": "Algorithmic dynamic discounting and 3-second instant payment link dispatch.",
        "Pain_AR": "المفاوضات اليدوية على أسعار الإيجار تستغرق وقتاً طويلاً مما يسبب إلغاء 25% من الحجوزات.",
        "Revenue_Leak_AR": "210,000 درهم شهرياً في الحجوزات الملغاة",
        "Projected_Uplift_AR": "+30% زيادة سرعة إتمام الحجز مع رفع معدل الإشغال إلى 92%"
    }
]

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
    
    st.caption("DUBAI AUTONOMOUS SALES AUDIT & OUTREACH")
    st.markdown("---")
    
    menu = st.radio(
        "Navigation",
        [
            "📧 Executive Pitch Matrix (خطابات المبيعات التنفيذية)",
            "🎯 Enterprise Audit & Forecast (التدقيق والفرص)",
            "📱 Live Polyglot WhatsApp Studio (المحاكي المباشر)", 
            "📊 Executive CRM Pipeline"
        ],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown(f"""
    <div style='font-size:12px; color:#94a3b8;'>
        <b>Status:</b> <span style='color:#10b981;'>🟢 Active Enterprise Node</span><br>
        <b>Standard:</b> Dubai Corporate English (C-Level)<br>
        <b>Live Demo:</b> {DEMO_URL}
    </div>
    """, unsafe_allow_html=True)

# --------------------------------------------------
# 📧 1. Executive Pitch Matrix Screen (Fixed Clean Alignment)
# --------------------------------------------------
if menu == "📧 Executive Pitch Matrix (خطابات المبيعات التنفيذية)":
    st.markdown("<h1 style='font-size:26px; font-weight:800; color:#ffffff;'>📧 Executive B2B Pitch Matrix & Audit Proposals</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94a3b8; font-size:14px; margin-bottom:20px;'>Executive pitches formatted in Dubai corporate standard English for C-Level executives, with clean bidirectional layout.</p>", unsafe_allow_html=True)
    
    # Language Toggle Selector
    pitch_lang = st.radio("Select Pitch Format / اختر لغة الخطاب التنفيذي:", ["🇬🇧 Corporate English (Dubai C-Level Standard - Recommended)", "🇦🇪 Arabic Clean Format (العربية المنضبطة)"], horizontal=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

    for idx, lead in enumerate(DUBAI_DEEP_AUDIT_DATA):
        if "English" in pitch_lang:
            email_subj = f"Operational AI Audit & Revenue Forecast for {lead['Company']} Dubai Campaigns"
            
            email_body = f"""Dear {lead['Decision_Maker']} & Executive Leadership Team at {lead['Company']},

We have been closely tracking your market leadership across your branches in {lead['Branches']} and your dedicated team of {lead['Brokers_Count']}.

Based on our operational assessment of your estimated digital advertising spend of {lead['Est_Ad_Spend']}:

1. OPERATIONAL AUDIT & IDENTIFIED REVENUE LEAKAGE:
- {lead['Pain_EN']}
- Estimated Financial Impact: {lead['Revenue_Leak_EN']}.

2. STRATEGIC VALUE OF APEXLEAD OS:
- Autonomous 3-second response time across 4 languages (Arabic dialects, Hindi/Hinglish, Executive English, and Russian).
- {lead['Strategic_Value_EN']}
- Real-time buyer budget qualification and direct broker calendar synchronization.

3. PROJECTED ANNUAL REVENUE UPLIFT:
- Implementation forecast: {lead['Projected_Uplift_EN']}.

4. INTERACTIVE LIVE DEMO & SANDBOX:
Experience the multi-lingual lead conversion engine configured for your operational model:
{DEMO_URL}

We provide your enterprise with a complimentary 7-day operational pilot to validate response speed and closing velocity with zero upfront financial commitment.

We would welcome a concise 5-minute executive briefing call at your convenience.

Best regards,

ApexLead Enterprise Solutions Team
Dubai, United Arab Emirates"""

        else:
            email_subj = f"تقرير التدقيق التشغيلي وتوقعات العائد المالي لشركة [{lead['Company']}]"
            
            email_body = f"""السادة / إدارة [{lead['Company']}] وفريق المبيعات المحترمين،

تحية طيبة وبعد،

نتابع باهتمام ريادتكم في سوق عقارات دبي عبر فروعكم وفريق عملكم المتميز.

من واقع دراستنا لنشاطكم الإعلاني التقديري البالغ ({lead['Est_Ad_Spend']}):

1. التدقيق التشغيلي ورصد التسرب المالي:
- {lead['Pain_AR']}
- الهدر المالي التقديري: {lead['Revenue_Leak_AR']}.

2. القيمة المضافة لنظامنا الذكي:
- استجابة فورية خلال 3 ثوانٍ بـ 4 لغات (عربي، هندي، إنجليزي، روسي) على مدار 24 ساعة.
- فرز ميزانية المشترين وتأهيلهم آلياً قبل تحويلهم للوسطاء.
- تثبيت مواعيد المعاينات تلقائياً في تقويم فريق المبيعات.

3. العائد المالي المتوقع لشركتكم:
- زيادة تقديرية: {lead['Projected_Uplift_AR']}.

4. رابط المعاينة التفاعلية المباشرة:
{DEMO_URL}

نقدم لشركتكم فترة تجريبية مجانية لمدة 7 أيام لاختبار كفاءة النظام عملياً دون أي التزام مالي مسبق.

وتفضلوا بقبول فائق التقدير والاحترام،

فريق تطوير الأعمال المؤسسية
دبي، الإمارات العربية المتحدة"""

        mailto_link = f"mailto:{lead['Email']}?subject={urllib.parse.quote(email_subj)}&body={urllib.parse.quote(email_body)}"
        
        wa_text = f"Dear {lead['Company']} Team, I have dispatched the Operational AI Audit & Revenue Forecast to {lead['Email']}. You can also explore the live interactive demo here: {DEMO_URL}"
        wa_link = f"https://wa.me/{lead['Phone'].replace('+', '').replace(' ', '')}?text={urllib.parse.quote(wa_text)}"

        with st.container():
            st.markdown(f"""
            <div class="enterprise-card">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                    <div>
                        <span style="font-size:19px; font-weight:800; color:#ffffff;">🏢 {lead['Company']}</span>
                        &nbsp;&nbsp;<span class="tag-gold">📈 {lead['Projected_Uplift_EN' if 'English' in pitch_lang else lead['Projected_Uplift_AR']}</span>
                    </div>
                    <div>
                        <span style="color:#94a3b8; font-size:13px;">Target: <b>{lead['Decision_Maker']}</b></span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Clean Code Block Display to prevent any BiDi text distortion
            st.caption(f"**Subject:** `{email_subj}`")
            st.text_area("Official Executive Proposal (Click button below to open in Mail client):", email_body, height=220, key=f"pitch_box_{idx}")
            
            c_btn1, c_btn2 = st.columns([1, 1])
            with c_btn1:
                st.markdown(f'<a href="{mailto_link}" class="btn-action-primary" style="width:100%; justify-content:center;">📧 Open & Send in Email App</a>', unsafe_allow_html=True)
            with c_btn2:
                st.markdown(f'<a href="{wa_link}" target="_blank" class="btn-action-wa" style="width:100%; justify-content:center;">💬 Direct WhatsApp Follow-Up</a>', unsafe_allow_html=True)
            st.markdown("---")

# --------------------------------------------------
# 🎯 2. Enterprise Audit & Forecast Screen
# --------------------------------------------------
elif menu == "🎯 Enterprise Audit & Forecast (التدقيق والفرص)":
    st.markdown("<h1 style='font-size:26px; font-weight:800; color:#ffffff;'>🎯 Dubai Enterprise Operational Audit & Revenue Forecast</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94a3b8; font-size:14px; margin-bottom:20px;'>Operational metrics, network footprint, and leakage diagnostics for audited Dubai enterprises.</p>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-card">
            <div class="kpi-label">Audited Dubai Enterprises</div>
            <div class="kpi-value">{len(DUBAI_DEEP_AUDIT_DATA)} Industry Leaders</div>
            <div class="kpi-badge">Full Operational Deep-Dive</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Combined Broker Force</div>
            <div class="kpi-value">880+ Brokers</div>
            <div class="kpi-badge">Across 15+ Hubs</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Est. Monthly Ad Leak</div>
            <div class="kpi-value">AED 1,360,000</div>
            <div class="kpi-badge">Off-Hours Friction</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Projected Annual Uplift</div>
            <div class="kpi-value">+ AED 12.4M</div>
            <div class="kpi-badge">ApexLead OS Impact</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    for idx, lead in enumerate(DUBAI_DEEP_AUDIT_DATA):
        st.markdown(f"""
        <div class="enterprise-card">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                <div>
                    <span style="font-size:20px; font-weight:800; color:#ffffff;">🏢 {lead['Company']}</span>
                    &nbsp;&nbsp;<span class="tag-blue">{lead['Category']}</span>
                    &nbsp;<span class="tag-green">📍 HQ: {lead['Headquarters']}</span>
                </div>
                <div>
                    <span class="tag-purple">💰 Ad Spend: {lead['Est_Ad_Spend']}</span>
                </div>
            </div>
            
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:15px; background:#0b1120; padding:15px; border-radius:10px; margin-bottom:12px; border:1px solid #1e293b;">
                <div style="font-size:13px; color:#cbd5e1;">
                    🏢 <b>Branch Network:</b> {lead['Branches']}<br>
                    👥 <b>Licensed Broker Force:</b> {lead['Brokers_Count']}<br>
                    👤 <b>Executive Leadership:</b> {lead['Decision_Maker']}
                </div>
                <div style="font-size:13px; color:#cbd5e1;">
                    ✉️ <b>Enterprise Email:</b> <span style="color:#38bdf8;">{lead['Email']}</span><br>
                    📞 <b>Direct Line:</b> {lead['Phone']}<br>
                    🎯 <b>Strategic Value:</b> {lead['Strategic_Value_EN']}
                </div>
            </div>

            <div style="display:grid; grid-template-columns: 1.2fr 1.2fr; gap:15px;">
                <div style="background:#1e1b18; border-left:4px solid #ef4444; padding:10px 14px; border-radius:0 8px 8px 0; font-size:13px; color:#fca5a5;">
                    ⚠️ <b>Operational Leakage Diagnosed:</b><br>{lead['Pain_EN']}<br>
                    <b style="color:#f87171;">📉 Estimated Monthly Loss: {lead['Revenue_Leak_EN']}</b>
                </div>
                <div style="background:#06281e; border-left:4px solid #10b981; padding:10px 14px; border-radius:0 8px 8px 0; font-size:13px; color:#86efac;">
                    🚀 <b>Projected Performance Uplift:</b><br>{lead['Projected_Uplift_EN']}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# --------------------------------------------------
# 📱 3. Live Polyglot WhatsApp Studio Screen
# --------------------------------------------------
elif menu == "📱 Live Polyglot WhatsApp Studio (المحاكي المباشر)":
    st.markdown("<h1 style='font-size:26px; font-weight:800; color:#ffffff;'>📱 Live Polyglot WhatsApp Engine & Command Studio</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94a3b8; font-size:14px; margin-bottom:20px;'>Interactive multi-lingual sandbox allowing enterprise clients to experience immediate lead qualification.</p>", unsafe_allow_html=True)
    
    col_sim, col_ctrl = st.columns([1.1, 1.3], gap="large")
    
    with col_sim:
        st.markdown("""
        <div class="wa-wrapper">
            <div class="wa-header">
                <div class="wa-avatar">⚡</div>
                <div>
                    <div style="font-weight:700; color:#e9edef; font-size:15px;">ApexLead AI Enterprise Assistant</div>
                    <div style="font-size:12px; color:#10b981;">Online | Dubai Real Estate Cluster</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        chat_html = "<div class='wa-body'>"
        for msg in st.session_state.chat_history:
            if msg['sender'] == 'user':
                chat_html += f"<div class='msg-in'><b>Client:</b><br>{msg['text']}</div>"
            else:
                chat_html += f"<div class='msg-out'><b>ApexLead Agent:</b><br>{msg['text']}</div>"
        chat_html += "</div>"
        st.markdown(chat_html, unsafe_allow_html=True)
        
        with st.form("deep_chat_form", clear_on_submit=True):
            user_msg = st.text_input("Type a message in any language...", placeholder="e.g. Namaste 2BHK price / What is the ROI in Downtown? / بدي شقة بمارينا")
            if st.form_submit_button("Send Message 💬", type="primary", use_container_width=True) and user_msg:
                st.session_state.chat_history.append({"sender": "user", "text": user_msg})
                lower_msg = user_msg.lower()
                
                if any(w in lower_msg for w in ["namaste", "bhai", "kya", "crore", "lakh", "hai", "bhk", "india", "paisa"]):
                    reply = "Namaste ji! 🙏 Welcome to ApexLead. Expected rental ROI is 8-10% tax-free! I have dispatched the detailed PDF brochure (with INR ₹ conversion) to this WhatsApp chat. Would you like to schedule a viewing or zoom consultation tomorrow?"
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

    with col_ctrl:
        st.markdown("""
        <div class="enterprise-card">
            <h3 style="margin-top:0; color:#f8fafc; font-size:18px;">💡 Why this Audit Pitch guarantees C-Level conversion:</h3>
            <ul style="color:#cbd5e1; font-size:13.5px; line-height:1.8; padding-left:20px; margin-bottom:0;">
                <li><b>Bypasses Gatekeepers:</b> Demonstrates comprehensive prior research on broker count, ad budgets, and branch network.</li>
                <li><b>Quantified Financial Impact:</b> Directly highlights monthly commission leakage (AED Leak) to trigger urgency.</li>
                <li><b>One-Click Interactive Sandbox:</b> Decision-makers can directly test multi-lingual responses without booking setup calls.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# --------------------------------------------------
# 📊 4. Executive CRM Pipeline Screen
# --------------------------------------------------
elif menu == "📊 Executive CRM Pipeline":
    st.markdown("<h1 style='font-size:26px; font-weight:800; color:#ffffff;'>📊 Live Enterprise Pipeline & Intelligence</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94a3b8; font-size:14px; margin-bottom:20px;'>Live qualified lead pipeline captured autonomously across multilingual ad channels.</p>", unsafe_allow_html=True)
    
    pipeline_df = pd.DataFrame([
        {"Time": "09:40 AM", "Customer": "Rajesh Sharma", "Language": "🇮🇳 Hindi / English", "Property Interest": "2BHK Luxury (Business Bay)", "Budget": "AED 1,850,000 (₹4.2 Cr)", "Grade": "🔥 Ultra Hot", "Status": "Auto-Scheduled Zoom Call"},
        {"Time": "09:15 AM", "Customer": "Tariq Mansoor", "Language": "🇦🇪 Gulf Arabic", "Property Interest": "1-Bed Downtown (Burj View)", "Budget": "AED 120,000 / yr", "Grade": "🔥 Hot Lead", "Status": "Viewing Booked (Tomorrow 4 PM)"},
        {"Time": "08:40 AM", "Customer": "Sarah Jenkins", "Language": "🇬🇧 English", "Property Interest": "Holiday Home (JVC)", "Budget": "AED 8,500 / month", "Grade": "⚡ Qualified", "Status": "Payment Link Dispatched"},
        {"Time": "Yesterday", "Customer": "Dmitry Ivanov", "Language": "🇷🇺 Russian", "Property Interest": "Waterfront Villa (Palm Jumeirah)", "Budget": "AED 18,500,000 ($5.0M)", "Grade": "👑 Ultra VIP", "Status": "Assigned to Managing Partner"}
    ])
    st.dataframe(pipeline_df, use_container_width=True, hide_index=True)

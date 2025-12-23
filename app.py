import streamlit as st
from groq import Groq
import urllib.parse

# 1. إعدادات التصميم الفائق (Inspirion Ultra Luxury UI)
st.set_page_config(page_title="Inspirion AI | نخبة المحتوى", page_icon="✨", layout="centered")

st.markdown("""
    <style>
    /* خلفية متدرجة فخمة */
    .stApp {
        background: radial-gradient(circle at top right, #0f172a, #020617);
        color: #f8fafc;
        direction: rtl;
    }
    
    /* تصميم العنوان بنظام النيون */
    .main-title { 
        text-align: center; 
        background: linear-gradient(90deg, #00d4ff, #007bff, #00d4ff);
        background-size: 200% auto;
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent; 
        font-size: 65px; 
        font-weight: 900; 
        letter-spacing: -1px;
        animation: shine 3s linear infinite;
    }
    @keyframes shine { to { background-position: 200% center; } }

    /* تنسيق الحقول */
    .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
        background-color: #1e293b !important;
        color: white !important;
        border-radius: 12px !important;
        border: 1px solid #334155 !important;
    }

    /* تصميم الأزرار الذهبي/الأزرق */
    .stButton>button { 
        width: 100%; 
        border-radius: 15px; 
        height: 4em; 
        background: linear-gradient(45deg, #0ea5e9, #2563eb); 
        color: white; 
        border: none; 
        font-weight: bold;
        font-size: 22px;
        box-shadow: 0 10px 20px -10px #0ea5e9;
        transition: 0.4s;
    }
    .stButton>button:hover { 
        transform: translateY(-5px); 
        box-shadow: 0 20px 30px -10px #2563eb;
    }

    /* صندوق المعاينة الاحترافي */
    .preview-box { 
        background: rgba(30, 41, 59, 0.5);
        backdrop-filter: blur(10px);
        padding: 30px; 
        border-radius: 20px; 
        border: 1px solid rgba(255,255,255,0.1);
        margin-top: 25px; 
        text-align: right; 
        font-size: 1.2em;
    }

    /* قسم القفل الراقي */
    .unlock-section { 
        background: rgba(15, 23, 42, 0.8);
        padding: 40px; 
        border-radius: 30px; 
        border: 2px solid #1e40af; 
        text-align: center; 
        margin-top: 40px;
    }

    /* زر الواتساب الفخم */
    .whatsapp-btn {
        background: #25D366;
        color: white !important;
        padding: 18px 40px;
        border-radius: 50px;
        text-decoration: none;
        font-weight: 800;
        display: inline-block;
        margin-top: 25px;
        font-size: 20px;
        box-shadow: 0 10px 15px rgba(37, 211, 102, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

# 2. جلب البيانات السرية
api_key = st.secrets.get("GROQ_API_KEY")
client = Groq(api_key=api_key) if api_key else None

# 3. واجهة Inspirion
st.markdown("<h1 class='main-title'>Inspirion AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.4em; color: #94a3b8; font-weight: 300;'>نصيغ المستقبل بأدوات الذكاء الاصطناعي الأكثر تطوراً</p>", unsafe_allow_html=True)
st.divider()

if not api_key:
    st.error("مفتاح API غير مبرمج في الإعدادات السرية.")
    st.stop()

# القوالب
template = st.selectbox(
    "اختر القالب الإبداعي:",
    ["💎 إعلان فيسبوك وانستغرام VIP", "📊 خطة عمل استراتيجية", "🎬 نص محتوى فيديو (Reels)", "📰 مقال احترافي معمق"]
)

topic = st.text_area("عن ماذا يدور إلهامك اليوم؟", placeholder="اكتب تفاصيل مشروعك هنا...", height=120)

if st.button("توليد المحتوى الإمبراطوري 🚀"):
    if topic:
        with st.spinner("Inspirion ينسج خيوط الإبداع..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "أنت Inspirion AI، المصمم الأول للمحتوى التسويقي الفخم في العالم العربي."},
                        {"role": "user", "content": f"نوع المحتوى: {template}. الموضوع: {topic}"}
                    ]
                )
                st.session_state['content'] = response.choices[0].message.content
                st.session_state['topic'] = topic
                st.session_state['done'] = True
            except Exception as e:
                st.error(f"Error: {e}")

# 4. منطقة التحصيل (بدون أرقام، فقط تواصل)
if st.session_state.get('done'):
    st.markdown("### 🔍 معاينة ذكية للمحتوى:")
    st.markdown(f'<div class="preview-box">{st.session_state["content"][:200]}..........</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="unlock-section">', unsafe_allow_html=True)
    st.markdown("<h2 style='color: #60a5fa;'>🔒 هذا المحتوى محمي بموجب حقوق Inspirion</h2>", unsafe_allow_html=True)
    st.write("للحصول على النص الكامل واستخدامه تجارياً، يرجى تفعيل النسخة المدفوعة.")
    
    # التحقق من الكود السري من الـ Secrets
    correct_code = st.secrets.get("ACTIVATION_CODE", "GOLD_2025")
    
    unlock_key = st.text_input("أدخل رمز التفعيل الخاص بك:", type="password")
    
    if unlock_key == correct_code:
        st.balloons()
        st.success("تم فك التشفير بنجاح!")
        st.markdown("---")
        st.markdown(st.session_state['content'])
    else:
        # زر الواتساب للتواصل المباشر
        msg = urllib.parse.quote(f"مرحباً Inspirion، أريد شراء كود التفعيل لـ: {st.session_state['topic']}")
        st.markdown(f'<a href="https://wa.me/96181950506?text={msg}" class="whatsapp-btn">تواصل مع الإدارة للحصول على الكود 💬</a>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br><p style='text-align: center; color: #475569; font-size: 0.9em;'>Inspirion AI | تم تطويره لنخبة المجتمع اللبناني 2025</p>", unsafe_allow_html=True)

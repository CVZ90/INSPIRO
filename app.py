import streamlit as st
from groq import Groq
import urllib.parse

# 1. إعدادات التصميم الفاخر (Inspirion VIP UI)
st.set_page_config(page_title="Inspirion AI | إبداع بلا حدود", page_icon="✨", layout="centered")

st.markdown("""
    <style>
    /* تنسيق الخلفية والنصوص */
    .stApp { background-color: #0e1117; color: white; direction: rtl; }
    
    /* تصميم العنوان الرئيسي */
    .main-title { 
        text-align: center; 
        background: -webkit-linear-gradient(#00d4ff, #007bff); 
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent; 
        font-size: 60px; 
        font-weight: bold; 
        margin-bottom: 5px;
    }
    
    /* تصميم الأزرار */
    .stButton>button { 
        width: 100%; 
        border-radius: 15px; 
        height: 3.5em; 
        background: linear-gradient(45deg, #00d4ff, #007bff); 
        color: white; 
        border: none; 
        font-weight: bold;
        font-size: 20px;
        transition: 0.4s ease;
        box-shadow: 0 4px 15px rgba(0, 212, 255, 0.2);
    }
    .stButton>button:hover { 
        transform: translateY(-3px); 
        box-shadow: 0 8px 25px rgba(0, 212, 255, 0.4); 
        color: #f0fdfa;
    }
    
    /* صندوق المعاينة */
    .preview-box { 
        background-color: #161b22; 
        padding: 25px; 
        border-radius: 15px; 
        border-right: 6px solid #00d4ff; 
        margin-top: 20px; 
        text-align: right; 
        font-size: 1.1em;
        line-height: 1.7;
    }
    
    /* قسم القفل والدفع */
    .unlock-section { 
        background: linear-gradient(145deg, #1e293b, #0f172a); 
        padding: 35px; 
        border-radius: 25px; 
        border: 1px solid #3b82f6; 
        text-align: center; 
        margin-top: 40px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    
    /* زر واتساب */
    .whatsapp-btn {
        background-color: #25D366;
        color: white !important;
        padding: 15px 30px;
        border-radius: 50px;
        text-decoration: none;
        font-weight: bold;
        display: inline-block;
        margin-top: 20px;
        font-size: 18px;
        transition: 0.3s;
    }
    .whatsapp-btn:hover { background-color: #128C7E; transform: scale(1.05); }
    </style>
""", unsafe_allow_html=True)

# 2. الاتصال بـ Groq API (المفتاح مخفي في Secrets)
api_key = st.secrets.get("GROQ_API_KEY")
if not api_key:
    st.error("⚠️ خطأ: مفتاح GROQ_API_KEY غير موجود في إعدادات Secrets!")
    st.stop()
client = Groq(api_key=api_key)

# 3. واجهة المستخدم الرئيسية
st.markdown("<h1 class='main-title'>Inspirion AI ✨</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.3em; color: #94a3b8;'>المنصة الأولى في لبنان لابتكار المحتوى البيعي والخطط التسويقية</p>", unsafe_allow_html=True)
st.divider()

# اختيار نوع الخدمة
template_type = st.selectbox(
    "ما هي الخدمة التي تحتاجها اليوم؟",
    [
        "🔥 إعلان فيسبوك وانستغرام بيعي", 
        "📋 خطة تسويقية شاملة للمشاريع الناشئة", 
        "🎬 سيناريو فيديو تيك توك / ريلز", 
        "✍️ كتابة مقال احترافي طويل",
        "📦 وصف منتجات لمتجر إلكتروني"
    ]
)

topic = st.text_area("اشرح فكرتك أو مشروعك بالتفصيل:", placeholder="مثلاً: محل موبايلات جديد في طرابلس يقدم كفالة سنتين وأسعار منافسة...", height=150)

if st.button("توليد المحتوى الإبداعي الآن 🚀"):
    if topic:
        with st.spinner("Inspirion يحلل البيانات ويصيغ لك الأفضل..."):
            try:
                # هندسة الأوامر (Prompt Engineering) مخصصة لكل قالب
                prompts = {
                    "🔥 إعلان فيسبوك وانستغرام بيعي": "اكتب إعلان فيسبوك احترافي لـ {topic}. ابدأ بجملة تخطف الانتباه، عدد المميزات، ثم Call to Action قوي مع هاشتاغات لبنانية.",
                    "📋 خطة تسويقية شاملة للمشاريع الناشئة": "ضع استراتيجية تسويق لـ {topic} تشمل الجمهور المستهدف، أفكار حملات إعلانية، ونصائح للنمو في السوق اللبناني.",
                    "🎬 سيناريو فيديو تيك توك / ريلز": "اكتب نص فيديو قصير لـ {topic}. ركز على أول 3 ثوانٍ لجذب المشاهد، استخدم لغة بسيطة ومحفزة.",
                    "✍️ كتابة مقال احترافي طويل": "اكتب مقالاً مفصلاً ومنسقاً حول {topic} بأسلوب تعليمي وجذاب.",
                    "📦 وصف منتجات لمتجر إلكتروني": "اكتب وصفاً تسويقياً لمنتج {topic} يركز على الفوائد ويقنع الزبون بالشراء فوراً."
                }
                
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "أنت Inspirion AI، خبير رائد في كتابة المحتوى التسويقي باللغتين العربية والإنجليزية، متخصص في السوق اللبناني والخليجي."},
                        {"role": "user", "content": prompts[template_type].format(topic=topic)}
                    ]
                )
                
                st.session_state['full_content'] = response.choices[0].message.content
                st.session_state['current_topic'] = topic
                st.session_state['is_done'] = True
            except Exception as e:
                st.error(f"عذراً، حدث خطأ أثناء الاتصال بالذكاء الاصطناعي: {e}")

# 4. نظام القفل والدفع (Security Optimized)
if st.session_state.get('is_done'):
    st.markdown("### 🔍 معاينة ذكية للمحتوى:")
    # عرض أول 15% من النص فقط
    preview_limit = 180
    preview = st.session_state['full_content'][:preview_limit] + ".........."
    st.markdown(f'<div class="preview-box">{preview}</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="unlock-section">', unsafe_allow_html=True)
    st.markdown("### 🔒 المحتوى الاحترافي مقفل")
    st.write("للحصول على النص الكامل والقابل للنسخ، يرجى تفعيل الخدمة بـ **4$** فقط")
    st.write("رقم المحفظة (Whish Money):")
    st.markdown("<h2 style='color: #00d4ff;'>81 950 506</h2>", unsafe_allow_html=True)
    
    # جلب الكود من Secrets (لحماية الرمز من المتسللين عبر GitHub)
    correct_code = st.secrets.get("ACTIVATION_CODE", "ADMIN_123")
    
    code_input = st.text_input("أدخل رمز التفعيل المستلم هنا:", type="password")
    
    if code_input == correct_code:
        st.balloons()
        st.success("✨ تم فك التشفير بنجاح! إليك المحتوى الكامل من Inspirion:")
        st.markdown("---")
        st.markdown(st.session_state['full_content'])
        st.info("💡 نصيحة: يمكنك الآن نسخ النص واستخدامه مباشرة في حملاتك الإعلانية.")
    else:
        # رابط واتساب مبرمج برسالة تلقائية
        wa_text = urllib.parse.quote(f"مرحباً Inspirion، لقد حولت 4$ وأريد كود التفعيل لمحتوى: {st.session_state['current_topic']}")
        st.markdown(f'<a href="https://wa.me/96181950506?text={wa_text}" class="whatsapp-btn">إرسال صورة الدفع وطلب الكود 💬</a>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# تذييل الصفحة
st.markdown("<br><hr><p style='text-align: center; color: #64748b;'>Inspirion AI © 2025 | Powered by Lebanon's Best AI Engine</p>", unsafe_allow_html=True)

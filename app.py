import streamlit as st
from groq import Groq
import urllib.parse

# 1. إعدادات التصميم (Inspirion Luxury UI)
st.set_page_config(page_title="Inspirion AI | ابتكار المحتوى", page_icon="✨")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; direction: rtl; }
    .stButton>button { 
        width: 100%; 
        border-radius: 12px; 
        height: 3.5em; 
        background: linear-gradient(45deg, #00d4ff, #007bff); 
        color: white; 
        border: none; 
        font-weight: bold;
        font-size: 18px;
        transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 5px 15px rgba(0,212,255,0.4); }
    .preview-box { background-color: #161b22; padding: 25px; border-radius: 15px; border-right: 5px solid #00d4ff; margin-top: 20px; text-align: right; line-height: 1.6; }
    .unlock-section { background: linear-gradient(145deg, #1e293b, #0f172a); padding: 30px; border-radius: 20px; border: 1px solid #3b82f6; text-align: center; margin-top: 30px; }
    .main-title { text-align: center; background: -webkit-linear-gradient(#00d4ff, #007bff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 55px; font-weight: bold; margin-bottom: 0px; }
    </style>
""", unsafe_allow_html=True)

# 2. الاتصال بـ Groq
api_key = st.secrets.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

# 3. واجهة المستخدم
st.markdown("<h1 class='main-title'>Inspirion AI ✨</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.2em; color: #cbd5e1;'>حول أفكارك إلى محتوى احترافي يبيع</p>", unsafe_allow_html=True)
st.divider()

# خيارات القوالب الاحترافية
template_type = st.selectbox(
    "ماذا تريد أن نبتكر لك اليوم؟",
    [
        "إعلان فيسبوك وانستغرام احترافي", 
        "خطة تسويقية متكاملة لمشروعك", 
        "نص فيديو تيك توك / ريلز سريع", 
        "كتابة مقال متوافق مع SEO",
        "وصف منتجات لمتجر إلكتروني"
    ]
)

topic = st.text_area("أدخل تفاصيل مشروعك أو فكرتك:", placeholder="مثلاً: افتتاح كافيه جديد في الحمرا، بيروت، يقدم قهوة مختصة وحلويات...")

if st.button("ابدأ الابتكار الآن 🚀"):
    if topic:
        with st.spinner("Inspirion يقوم بصياغة سحره الآن..."):
            try:
                prompts = {
                    "إعلان فيسبوك وانستغرام احترافي": "أنت خبير Copywriting. اكتب إعلان إبداعي لمشروع {topic} يتضمن Hook قوي، فوائد، Call to Action، وهاشتاغات ذكية للسوق اللبناني.",
                    "خطة تسويقية متكاملة لمشروعك": "أنت مستشار استراتيجي. ضع خطة عمل لمشروع {topic} تشمل الجمهور المستهدف، القنوات المقترحة، وأفكار لزيادة الزبائن في لبنان.",
                    "نص فيديو تيك توك / ريلز سريع": "اكتب نص فيديو Reels/TikTok لمشروع {topic}. اجعل البداية صادمة، الشرح سريع، والنهاية تدفع للمتابعة أو الشراء.",
                    "كتابة مقال متوافق مع SEO": "اكتب مقالاً مفصلاً واحترافياً حول {topic} مع توزيع الكلمات المفتاحية بشكل ذكي.",
                    "وصف منتجات لمتجر إلكتروني": "اكتب وصفاً جذاباً لمنتج {topic} يركز على المشاعر والفوائد التي سيحصل عليها المشتري."
                }
                
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": "أنت Inspirion AI، خبير صناعة محتوى إبداعي وتفهم السوق العربي واللبناني بدقة."},
                              {"role": "user", "content": prompts[template_type].format(topic=topic)}]
                )
                
                st.session_state['result'] = response.choices[0].message.content
                st.session_state['topic_name'] = topic
                st.session_state['done'] = True
            except Exception as e:
                st.error(f"عذراً، حدث خطأ تقني: {e}")

# 4. المعاينة ونظام الدفع
if st.session_state.get('done'):
    st.markdown("### 🔍 معاينة المحتوى:")
    preview_text = st.session_state['result'][:180] + "..."
    st.markdown(f'<div class="preview-box">{preview_text}</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="unlock-section">', unsafe_allow_html=True)
    st.markdown("### 🔒 المحتوى الكامل جاهز للاستلام")
    st.write("لإظهار كامل النص الاحترافي، يرجى تفعيل الخدمة بـ **4$**")
    st.write("رقم محفظة Whish Money:")
    st.code("81950506", language="text")
    
    unlock_key = st.text_input("أدخل رمز التفعيل الذي استلمته:", type="password")
    
    if unlock_key == "SWIFT2025":
        st.balloons()
        st.success("تم التفعيل بنجاح! إليك المحتوى الكامل من Inspirion:")
        st.markdown("---")
        st.text_area("النص الكامل (جاهز للنسخ):", st.session_state['result'], height=400)
    else:
        wa_msg = urllib.parse.quote(f"مرحباً Inspirion، لقد أرسلت 4$ وأريد كود التفعيل لطلب: {st.session_state['topic_name']}")
        st.markdown(f'<a href="https://wa.me/96181950506?text={wa_msg}" style="background-color: #25D366; color: white; padding: 12px 25px; border-radius: 30px; text-decoration: none; font-weight: bold; display: inline-block;">تواصل لتفعيل المحتوى 💬</a>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br><p style='text-align: center; color: #4b5563;'>Inspirion AI Lebanon © 2025 | مخصص للمحترفين</p>", unsafe_allow_html=True)

import streamlit as st
from groq import Groq
import urllib.parse

# 1. إعدادات التصميم (Premium Dark UI)
st.set_page_config(page_title="SwiftContent AI | VIP", page_icon="✍️")
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; direction: rtl; }
    .stButton>button { width: 100%; border-radius: 12px; height: 3em; background: linear-gradient(to right, #00d4ff, #007bff); color: white; border: none; font-weight: bold; }
    .preview-box { background-color: #161b22; padding: 20px; border-radius: 15px; border-right: 5px solid #00d4ff; margin-top: 20px; text-align: right; }
    .unlock-section { background: #1e293b; padding: 25px; border-radius: 15px; border: 1px solid #3b82f6; text-align: center; margin-top: 20px; }
    </style>
""", unsafe_allow_html=True)

# 2. الاتصال بـ Groq
api_key = st.secrets.get("GROQ_API_KEY")
if not api_key:
    st.error("API Key missing!")
    st.stop()
client = Groq(api_key=api_key)

# 3. واجهة المستخدم
st.markdown("<h1 style='text-align: center; color: #00d4ff;'>SwiftContent AI 🚀</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>صناعة المحتوى الاحترافي بلمسة ذكاء اصطناعي متخصص</p>", unsafe_allow_html=True)
st.divider()

# خيارات القوالب
template_type = st.selectbox(
    "اختر نوع المحتوى الذي تحتاجه:",
    ["إعلان فيسبوك/انستغرام جذاب", "خطة تسويقية شاملة لعملك", "نص فيديو تيك توك سريع", "كتابة مقال أو بوست حر"]
)

topic = st.text_area("عن ماذا تريد أن نكتب؟ (مثلاً: مطعم بيتزا في بيروت، أو محل ثياب صيدا)", placeholder="اكتب تفاصيل مشروعك هنا...")

if st.button("توليد المحتوى بنقرة واحدة ✨"):
    if topic:
        with st.spinner("جاري العمل على طلبك..."):
            try:
                # تخصيص الأوامر حسب اختيار الزبون (Prompt Engineering)
                prompts = {
                    "إعلان فيسبوك/انستغرام جذاب": "أنت خبير في كتابة الإعلانات (Copywriter). اكتب إعلان فيسبوك جذاب لمشروع {topic} يتضمن: خطاف (Hook) في البداية، مميزات، عرض خاص، وهاشتاغات مناسبة للسوق اللبناني.",
                    "خطة تسويقية شاملة لعملك": "أنت مستشار تسويقي. اكتب خطة تسويقية لمشروع {topic} تتضمن: الجمهور المستهدف، استراتيجية السوشيال ميديا، وأفكار لزيادة المبيعات في لبنان.",
                    "نص فيديو تيك توك سريع": "اكتب نص فيديو تيك توك مدته 30 ثانية لمشروع {topic}. اجعل الكلام سريعاً، شبابياً، ومحفزاً على الشراء.",
                    "كتابة مقال أو بوست حر": "اكتب نصاً احترافياً مفصلاً حول {topic}."
                }
                
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": "أنت خبير محتوى عربي محترف وتفهم السوق اللبناني."},
                              {"role": "user", "content": prompts[template_type].format(topic=topic)}]
                )
                
                st.session_state['result'] = response.choices[0].message.content
                st.session_state['topic_name'] = topic
                st.session_state['done'] = True
            except Exception as e:
                st.error(f"حدث خطأ: {e}")

# 4. نظام المعاينة والقفل
if st.session_state.get('done'):
    st.markdown("### 📝 معاينة (الجزء الأول):")
    # عرض أول 150 حرف فقط ليبقى الباقي سراً
    preview_text = st.session_state['result'][:150] + "..."
    st.markdown(f'<div class="preview-box">{preview_text}</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="unlock-section">', unsafe_allow_html=True)
    st.markdown("### 🔒 المحتوى الكامل جاهز")
    st.write("لإظهار النص الكامل ونسخه، يرجى تفعيل الخدمة بـ **4$**")
    st.write("أرسل المبلغ عبر Whish إلى رقم: **81950506**")
    
    unlock_key = st.text_input("أدخل رمز التفعيل هنا:", type="password")
    
    if unlock_key == "SWIFT2025":
        st.balloons()
        st.success("تم فك القفل! إليك المحتوى الكامل:")
        st.markdown("---")
        st.text_area("انسخ النص من هنا:", st.session_state['result'], height=300)
    else:
        # زر الواتساب
        wa_msg = urllib.parse.quote(f"مرحباً، دفعت 4$ وأريد كود التفعيل لمحتوى: {st.session_state['topic_name']}")
        st.markdown(f'<a href="https://wa.me/96181950506?text={wa_msg}" style="color: #25D366; font-weight: bold; text-decoration: none;">اضغط هنا لإرسال صورة الدفع والحصول على الكود</a>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br><p style='text-align: center; color: #4b5563;'>SwiftContent AI Lebanon © 2025</p>", unsafe_allow_html=True)

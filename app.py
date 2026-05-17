import streamlit as st
import pickle, re, string, nltk
from textblob import TextBlob
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)


st.set_page_config(
    page_title="Mastercard Career Bot",
    page_icon="💳",
    layout="centered"
)


@st.cache_resource
def load_model():
    with open("mastercard_bot_v3.pkl", "rb") as f:
        return pickle.load(f)

model = load_model()


lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))
KEEP = {'not','no','how','what','where','when','who','me','my','i'}
stop_words = stop_words - KEEP

HINGLISH = {
    "kaise","karu","chahiye","mujhe","hai","kya","nahi","hain",
    "dikhao","batao","karo","milegi","madad","namaste","namaskar",
    "accha","theek","naukri","ke","liye","aur","wala","job","hoon"
}

def preprocess(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = re.sub(r'\d+', '', text)
    tokens = [lemmatizer.lemmatize(t) for t in text.split()
              if t not in stop_words]
    return ' '.join(tokens)

def is_hinglish(text):
    return any(w in HINGLISH for w in text.lower().split())

def correct_spelling(text):
    return text if is_hinglish(text) else str(TextBlob(text).correct())

def predict(text):
    original = text
    corrected = correct_spelling(text)
    clean = preprocess(corrected)
    intent = model.predict([clean])[0]
    confidence = round(model.predict_proba([clean]).max() * 100, 1)
    if confidence < 40:
        intent = "out_of_scope"
    return intent, confidence, corrected, original


RESPONSES = {
    "greeting": "👋 Hi there! I'm the Mastercard Career Assistant. I can help you find **jobs**, **internships**, and guide you through the **application process**!",
    "job_search": "🔍 Here are some job openings that match your search!\n\nVisit 👉 [careers.mastercard.com](https://careers.mastercard.com) to explore 1000+ roles.",
    "internship": "🎓 Mastercard offers internships across **tech, finance, and consulting**.\n\nCheck the latest listings 👉 [Mastercard Internships](https://careers.mastercard.com)",
    "experience_filter": "📊 Mastercard has roles for **every level** — from freshers to Directors and VPs.\n\nTell me your experience level and I'll show relevant roles!",
    "apply": "📝 **How to Apply:**\n1. Go to [careers.mastercard.com](https://careers.mastercard.com)\n2. Find a role you like\n3. Click **'Apply Now'**\n4. Upload your resume\n5. Submit!\n\nThe process usually takes 15-20 minutes.",
    "resume": "📄 **Resume Tips:**\n- Upload PDF or Word format\n- Keep it ATS-friendly\n- Tailor it to the job description\n- Upload during the application on our careers site",
    "help": "💡 **Here's what I can do:**\n- 🔍 Find jobs\n- 🎓 Find internships\n- 📝 Explain how to apply\n- 📄 Resume upload guidance\n- 🏢 Tell you about company culture\n\nJust ask!",
    "company_culture": "🏢 **Life at Mastercard:**\n- 🌍 Diverse & Inclusive culture\n- 🏠 Hybrid work options\n- 📈 Strong career growth\n- 🎯 Great work-life balance\n- 💰 Competitive compensation\n\nIt's a great place to build your career!",
    "out_of_scope": "🤔 I'm specialized in **Mastercard career queries** only.\n\nTry asking me:\n- *'Show me software jobs'*\n- *'How do I apply?'*\n- *'Internships in delhi'*"
}


st.title("💳 Mastercard Career Assistant")
st.caption("Ask me about jobs, internships, or working at Mastercard • Supports Hinglish 🇮🇳")


with st.expander("⚡ What this bot fixes vs Mastercard's original bot"):
    st.markdown("""
| User Input | Original Mastercard Bot | This Bot |
|------------|------------------------|----------|
| `hi` | ❌ "Please rephrase" | ✅ Greeting detected (97.9%) |
| `help me` | ❌ "Please rephrase" | ✅ Help intent (83.4%) |
| `aplly job` | ❌ Failed completely | ✅ Auto spell-corrected → apply |
| `job kaise apply karu` | ❌ Failed (no Hinglish) | ✅ Apply intent (63.2%) |
| `mujhe internship chahiye` | ❌ Failed (no Hinglish) | ✅ Internship (79.9%) |
| `asdfgh` | ❌ Gave random valid answer | ✅ Out-of-scope (65.7%) |
| `what can you do` | ❌ "Please rephrase" | ✅ Help intent (75.1%) |
    """)

st.divider()


st.markdown("**Try asking:**")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🔍 Show me jobs"):
        st.session_state.prefill = "Show me jobs"
with col2:
    if st.button("🎓 Internships"):
        st.session_state.prefill = "Show me internships"
with col3:
    if st.button("📝 How to apply"):
        st.session_state.prefill = "How do I apply?"


if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "👋 Hi! I'm your Mastercard Career Assistant. Ask me about jobs, internships, or how to apply!"
    }]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if "prefill" in st.session_state:
    user_input = st.session_state.prefill
    del st.session_state.prefill
else:
    user_input = None


typed = st.chat_input("Ask me about jobs, internships, how to apply...")
if typed:
    user_input = typed

if user_input:
    
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    
    intent, confidence, corrected, original = predict(user_input)
    response = RESPONSES[intent]

    
    if corrected != original:
        response = f"*✏️ Auto-corrected: '{original}' → '{corrected}'*\n\n" + response

   
    with st.chat_message("assistant"):
        st.markdown(response)
        st.caption(f"Intent: `{intent}` • Confidence: `{confidence}%`")

    st.session_state.messages.append({"role": "assistant", "content": response})
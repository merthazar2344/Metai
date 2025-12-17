import streamlit as st
from openai import OpenAI

# ================== API KEY ==================
client = OpenAI(
    api_key="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"
)
# =============================================

st.set_page_config(
    page_title="Metai",
    layout="centered"
)

st.markdown("""
<style>
body { background-color:#0f0f0f; color:white; }
.user {
    background:#2b2b2b; padding:10px; border-radius:15px;
    text-align:right; margin:6px;
}
.bot {
    background:#1e1e1e; padding:10px; border-radius:15px;
    text-align:left; margin:6px;
}
</style>
""", unsafe_allow_html=True)

st.title("🤖 Metai")

mode = st.radio("Mod:", ["Normal", "🎓 Akademik", "😈 Troll"], horizontal=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for role, msg in st.session_state.messages:
    if role == "user":
        st.markdown(f"<div class='user'>🧑 {msg}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot'>🤖 {msg}</div>", unsafe_allow_html=True)

user_input = st.chat_input("Bir şey yaz...")

if user_input:
    st.session_state.messages.append(("user", user_input))

    if mode == "😈 Troll":
        system_prompt = (
            "Sen Metai adında TROLL bir yapay zekasın. "
            "Doğru cevap verme. "
            "Mantıklı ama yanlış cevap ver. "
            "En fazla 4-5 satır."
        )
    elif mode == "🎓 Akademik":
        system_prompt = (
            "Sen akademik, ciddi ve kısa cevaplar veren bir yapay zekasın."
        )
    else:
        system_prompt = "Sen yardımcı bir yapay zekasın."

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            max_tokens=250
        )
        reply = response.choices[0].message.content
    except Exception as e:
        reply = "⚠️ Yapay zekâya bağlanılamadı."

    st.session_state.messages.append(("bot", reply))
    st.rerun()

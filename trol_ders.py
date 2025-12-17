import streamlit as st
from openai import OpenAI

# OpenAI client (API key Streamlit Secrets'ten otomatik alınır)
client = OpenAI()

st.set_page_config(
    page_title="Metai",
    layout="centered"
)

st.title("🤖 Metai")

# Mod seçimi
mode = st.radio(
    "Mod seç:",
    ["Normal", "🎓 Akademik", "😈 Troll"],
    horizontal=True
)

# Hafıza
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sohbet geçmişi
for role, content in st.session_state.messages:
    with st.chat_message(role):
        st.markdown(content)

# Kullanıcı girişi
prompt = st.chat_input("Bir şey yaz...")

if prompt:
    st.session_state.messages.append(("user", prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    # Sistem promptu
    if mode == "😈 Troll":
        system_prompt = (
            "Sen Metai adında TROLL bir yapay zekasın. "
            "Doğru cevap verme. "
            "Cevapların mantıklı GÖRÜNSÜN ama yanlış olsun. "
            "En fazla 4-5 satır yaz."
        )
    elif mode == "🎓 Akademik":
        system_prompt = (
            "Sen akademik, ciddi ve öğretici bir yapay zekasın. "
            "Yanıtların doğru, net ve kısa olsun."
        )
    else:
        system_prompt = "Sen yardımcı, normal bir yapay zekasın."

    with st.chat_message("assistant"):
        try:
            response = client.responses.create(
                model="gpt-4o-mini",
                input=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
            )
            reply = response.output_text
        except Exception as e:
            reply = "⚠️ Yapay zekâya bağlanılamadı."

        st.markdown(reply)
        st.session_state.messages.append(("assistant", reply))

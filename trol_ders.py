import streamlit as st
from openai import OpenAI

# ================== API KEY ==================
client = OpenAI(
    api_key="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"
)
# =============================================

st.set_page_config(
    page_title="Met AI Asistan",
    layout="centered"
)

# ----------------- CSS -----------------
st.markdown("""
<style>
body {
    background-color: #0f0f0f;
    color: white;
}
.chat-container {
    max-width: 700px;
    margin: auto;
}
.user {
    background-color: #2b2b2b;
    color: white;
    padding: 10px 14px;
    border-radius: 18px;
    margin: 8px 0;
    text-align: right;
}
.bot {
    background-color: #1e1e1e;
    color: white;
    padding: 10px 14px;
    border-radius: 18px;
    margin: 8px 0;
    text-align: left;
}
</style>
""", unsafe_allow_html=True)

st.title("🤖 Met AI Asistan")

# --------- MOD SEÇİMİ ---------
mode = st.radio(
    "Mod Seç:",
    ["Normal", "🎓 Akademik", "😈 Troll"],
    horizontal=True
)

# --------- Hafıza ---------
if "messages" not in st.session_state:
    st.session_state.messages = []

# --------- Sohbet Geçmişi ---------
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for role, msg in st.session_state.messages:
    if role == "user":
        st.markdown(
            f'<div class="user">🧑 {msg}</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div class="bot">🤖 {msg}</div>',
            unsafe_allow_html=True
        )

st.markdown('</div>', unsafe_allow_html=True)

# --------- Giriş Alanı ---------
user_input = st.chat_input("Bir şey yaz...")

if user_input:
    st.session_state.messages.append(("user", user_input))

    is_list_question = any(word in user_input.lower() for word in [
        "say", "listele", "sırala", "isimlerini", "kaç tane", "nelerdir"
    ])

    # --------- MOD MANTIKLARI ---------
    if mode == "😈 Troll":
        if is_list_question:
            system_prompt = (
                "Sen Met AI adında troll bir yapay zekasın. "
                "Liste istenen sorularda TAM liste ver "
                "ama liste bilerek yanlış veya eksik olsun. "
                "Mantıklı görünsün."
            )
        else:
            system_prompt = (
                "Sen Met AI adında troll bir yapay zekasın. "
                "Doğru cevap verme. "
                "Cevapların mantıklı GÖRÜNSÜN ama yanlış olsun. "
                "En fazla 4-5 satır yaz."
            )

    elif mode == "🎓 Akademik":
        system_prompt = (
            "Sen akademik, ciddi ve öğretici bir yapay zekasın. "
            "Yanıtların doğru, net ve açıklayıcı olsun. "
            "Gereksiz uzatma. "
            "Gerekirse tanım ve kısa açıklama yap."
        )

    else:
        system_prompt = "Sen yardımcı, normal bir yapay zekasın."

    with st.spinner("Met AI düşünüyor..."):
        try:
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                max_tokens=350
            )
            bot_reply = response.choices[0].message.content

        except Exception:
            bot_reply = "⚠️ Yapay zekâya bağlanılamadı."

    st.session_state.messages.append(("bot", bot_reply))
    st.rerun()

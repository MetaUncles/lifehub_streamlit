import streamlit as st
import requests

st.set_page_config(page_title="LifeHUB", page_icon="💙")

# История запросов и ответов
if "history" not in st.session_state:
    st.session_state.history = []

# Hugging Face API
API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-alpha"
HEADERS = {"Authorization": "Bearer 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"}

def query_huggingface(prompt):
    payload = {"inputs": prompt}
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    if response.status_code == 200:
        try:
            return response.json()[0]["generated_text"]
        except:
            return "Ошибка при разборе ответа."
    else:
        return "Ошибка API или лимит исчерпан."

# Выбор вкладки
tab = st.sidebar.radio("Навигация", ["Эмоции", "Право"])

# --- Вкладка ЭМОЦИИ ---
if tab == "Эмоции":
    st.title("LifeHUB — Эмоциональный помощник")
    st.markdown("Как ты себя сейчас чувствуешь?")

    emotions = {
        "😟 Тревога": "anxiety",
        "😢 Печаль": "sadness",
        "😐 Апатия": "apathy",
        "😰 Паника": "panic",
        "😠 Злость": "anger",
        "😔 Одиночество": "loneliness"
    }

    selected = st.selectbox("Выбери эмоцию", list(emotions.keys()))
    user_input = st.text_area("Расскажи, что ты чувствуешь...")

    if st.button("Поговорить"):
        with st.spinner("Генерация ответа..."):
            prompt = f"Человек испытывает {selected}. Он описал это так: {user_input}. Ответь с поддержкой и эмпатией."
            answer = query_huggingface(prompt)
            st.session_state.history.append(("Эмоции", user_input, answer))
            st.success(answer)

# --- Вкладка ПРАВО ---
elif tab == "Право":
    st.title("LifeHUB — Юридический помощник")
    st.markdown("Задай свой юридический вопрос. AI постарается помочь максимально понятно.")

    legal_input = st.text_area("Вопрос:")

    if st.button("Получить юридический ответ"):
        with st.spinner("AI анализирует ваш вопрос..."):
            prompt = f"Ты юридический помощник. Ответь кратко, понятно и по делу на вопрос: {legal_input}"
            answer = query_huggingface(prompt)
            st.session_state.history.append(("Право", legal_input, answer))
            st.success(answer)

# --- Блок истории (общий) ---
if st.session_state.history:
    st.markdown("### История разговоров:")
    for idx, (topic, q, a) in enumerate(reversed(st.session_state.history[-10:]), 1):
        st.markdown(f"**{idx}. [{topic}]**
**Ты:** {q}

**LifeHUB:** {a}")

    if st.button("Очистить историю"):
        st.session_state.history.clear()

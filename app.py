import streamlit as st
import requests
import matplotlib.pyplot as plt
from collections import Counter

st.set_page_config(page_title="LifeHUB", page_icon="💙")

if "history" not in st.session_state:
    st.session_state.history = []

API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-alpha"
HEADERS = {"Authorization": "Bearer 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"}

EMOJI_MAP = {
    "anxiety": "😟",
    "sadness": "😢",
    "apathy": "😐",
    "panic": "😰",
    "anger": "😠",
    "loneliness": "😔",
    "joy": "😊",
    "love": "❤️",
    "hope": "🌈",
    "fear": "😨"
}

def query_huggingface(prompt):
    response = requests.post(API_URL, headers=HEADERS, json={"inputs": prompt})
    if response.status_code == 200:
        try:
            return response.json()[0]["generated_text"].strip().lower()
        except:
            return "Ошибка при разборе ответа."
    else:
        return "Ошибка API или лимит исчерпан."

tab = st.sidebar.radio("Навигация", ["Эмоции", "График настроения", "История"])

if tab == "Эмоции":
    st.title("LifeHUB — Эмоциональный помощник")
    st.markdown("Как ты себя сейчас чувствуешь?")
    user_input = st.text_area("Расскажи, что ты чувствуешь...")

    if st.button("Поговорить", key="emotion"):
        with st.spinner("Определяем твою эмоцию..."):
            detect_prompt = f"Определи основную эмоцию человека по тексту: '{user_input}'. Ответь одним словом на английском."
            emotion = query_huggingface(detect_prompt)
            emoji = EMOJI_MAP.get(emotion, "🔍")
            st.info(f"Определено: **{emotion.capitalize()}** {emoji}")

            full_prompt = f"Человек испытывает {emotion}. Он описал это так: {user_input}. Ответь с поддержкой и эмпатией."
            answer = query_huggingface(full_prompt)

            st.session_state.history.append(("Эмоции", user_input, answer, emotion))

            st.success(answer)

elif tab == "График настроения":
    st.title("Эмоциональное состояние")
    emotion_list = [e for (_, _, _, e) in st.session_state.history if e]

    if emotion_list:
        counts = Counter(emotion_list)
        labels = [f"{EMOJI_MAP.get(e, '')} {e.capitalize()}" for e in counts.keys()]
        values = list(counts.values())

        fig, ax = plt.subplots()
        ax.bar(labels, values)
        ax.set_ylabel("Частота")
        ax.set_title("Настроение за всё время")
        st.pyplot(fig)
    else:
        st.info("Пока нет данных для построения графика.")

elif tab == "История":
    st.title("История разговоров")
    if st.session_state.history:
        for idx, (topic, q, a, emotion) in enumerate(reversed(st.session_state.history[-20:]), 1):
            emoji = EMOJI_MAP.get(emotion, "")
            st.markdown(f"**{idx}. [{topic}]** {emoji}")
            st.markdown(f"**Ты:** {q}")
            st.markdown(f"**LifeHUB:** {a}")
        if st.button("Очистить историю"):
            st.session_state.history.clear()
    else:
        st.info("История пока пуста.")

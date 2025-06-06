import streamlit as st
import requests
import pandas as pd
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
            return response.json()[0]["generated_text"].strip()
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
            emotion = query_huggingface(detect_prompt).lower()
            emoji = EMOJI_MAP.get(emotion, "🔍")
            st.info(f"Определено: **{emotion.capitalize()}** {emoji}")

            structured_prompt = f"""Ты — эмпатичный психолог. Человек написал следующее: "{user_input}". 
1. Определи его текущее эмоциональное состояние.
2. Проанализируй, что может быть причиной его состояния.
3. Дай рекомендации, как справиться с этим состоянием. Укажи конкретные шаги. 
Структурируй ответ по пунктам, пиши тепло и поддерживающе."""

            answer = query_huggingface(structured_prompt)

            st.session_state.history.append(("Эмоции", user_input, answer, emotion))
            st.success(answer)

elif tab == "График настроения":
    st.title("Эмоциональное состояние")
    emotion_list = [e for (_, _, _, e) in st.session_state.history if e]

    if emotion_list:
        counts = Counter(emotion_list)
        data = {
            "Эмоция": [f"{EMOJI_MAP.get(e, '')} {e.capitalize()}" for e in counts.keys()],
            "Количество": list(counts.values())
        }
        df = pd.DataFrame(data)
        df.set_index("Эмоция", inplace=True)
        st.bar_chart(df)
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

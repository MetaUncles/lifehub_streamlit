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

# Навигация по вкладкам
tab = st.sidebar.radio("Навигация", ["Эмоции", "Право", "Здоровье", "Отношения", "Дети"])

# Вкладка ЭМОЦИИ
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

    if st.button("Поговорить", key="emotion"):
        with st.spinner("Генерация ответа..."):
            prompt = f"Человек испытывает {selected}. Он описал это так: {user_input}. Ответь с поддержкой и эмпатией."
            answer = query_huggingface(prompt)
            st.session_state.history.append(("Эмоции", user_input, answer))
            st.success(answer)

# Вкладка ПРАВО
elif tab == "Право":
    st.title("LifeHUB — Юридический помощник")
    legal_input = st.text_area("Задай юридический вопрос:")

    if st.button("Получить ответ", key="legal"):
        with st.spinner("AI анализирует ваш вопрос..."):
            prompt = f"Ты юридический помощник. Ответь кратко, понятно и по делу на вопрос: {legal_input}"
            answer = query_huggingface(prompt)
            st.session_state.history.append(("Право", legal_input, answer))
            st.success(answer)

# Вкладка ЗДОРОВЬЕ
elif tab == "Здоровье":
    st.title("LifeHUB — Медицинская поддержка")
    health_input = st.text_area("Опиши, что тебя беспокоит:")

    if st.button("Получить совет", key="health"):
        with st.spinner("AI обрабатывает симптомы..."):
            prompt = f"Ты — доброжелательный врач. Не ставь диагноз, но опиши возможные причины и рекомендации. Вот жалоба: {health_input}"
            answer = query_huggingface(prompt)
            st.session_state.history.append(("Здоровье", health_input, answer))
            st.success(answer)

# Вкладка ОТНОШЕНИЯ
elif tab == "Отношения":
    st.title("LifeHUB — Поддержка в отношениях")
    relation_input = st.text_area("Что происходит в отношениях?")

    if st.button("Поговорить", key="relations"):
        with st.spinner("AI поддерживает тебя..."):
            prompt = f"Ты — эмпатичный семейный психолог. Помоги человеку разобраться в ситуации: {relation_input}"
            answer = query_huggingface(prompt)
            st.session_state.history.append(("Отношения", relation_input, answer))
            st.success(answer)

# Вкладка ДЕТИ
elif tab == "Дети":
    st.title("LifeHUB — Детский помощник")
    kids_input = st.text_area("Что ты хочешь узнать о ребёнке или для ребёнка?")

    if st.button("Получить идею", key="kids"):
        with st.spinner("AI думает, как помочь..."):
            prompt = f"Ты — педагог и игровой тренер. Ответь доброжелательно и творчески: {kids_input}"
            answer = query_huggingface(prompt)
            st.session_state.history.append(("Дети", kids_input, answer))
            st.success(answer)

# Общая история
if st.session_state.history:
    st.markdown("### История разговоров:")
    for idx, (topic, q, a) in enumerate(reversed(st.session_state.history[-10:]), 1):
        st.markdown(f"**{idx}. [{topic}]**")
        st.markdown(f"**Ты:** {q}")
        st.markdown(f"**LifeHUB:** {a}")

    if st.button("Очистить историю"):
        st.session_state.history.clear()

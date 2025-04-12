import streamlit as st
import requests

st.set_page_config(page_title="LifeHUB (HuggingFace)", page_icon="💙")

st.title("LifeHUB — Эмоциональный помощник (HF API)")

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

        api_url = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-alpha"
        headers = {headers = {"Authorization": "Bearer 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"}}  # Можно добавить токен Hugging Face сюда: {"Authorization": "Bearer hf_..."}
        payload = {"inputs": prompt}

        response = requests.post(api_url, headers=headers, json=payload)
        if response.status_code == 200:
            try:
                output = response.json()
                text = output[0]["generated_text"]
                st.success(text)
            except Exception as e:
                st.error("Не удалось разобрать ответ.")
        else:
            st.error("Ошибка API или лимит исчерпан.")

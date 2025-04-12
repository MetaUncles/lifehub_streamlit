import streamlit as st
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import requests
import ast

st.set_page_config(page_title="LifeHUB (Google Sheets CMS)", page_icon="💙")

# Инициализация истории
if "history" not in st.session_state:
    st.session_state.history = []

# Авторизация и загрузка из Google Sheets
SHEET_ID = "1iY-37-QS1N1dD6bECj0RWrqXR2TCNspKg7Vw_CPn8PM"
SHEET_NAME = "Sheet1"

@st.cache_data
def load_sheet():
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"
    df = pd.read_csv(url)
    return df

cms_df = load_sheet()

# Hugging Face API
API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-alpha"
HEADERS = {"Authorization": "Bearer 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"}

def query_huggingface(prompt):
    response = requests.post(API_URL, headers=HEADERS, json={"inputs": prompt})
    if response.status_code == 200:
        try:
            return response.json()[0]["generated_text"]
        except:
            return "Ошибка при разборе ответа."
    else:
        return "Ошибка API или лимит исчерпан."

# Навигация
categories = cms_df["category"].tolist()
tab = st.sidebar.radio("Навигация", categories)
active = cms_df[cms_df["category"] == tab].iloc[0]

st.title(f"LifeHUB — {tab}")
user_input = ""

# Обработка эмоций
if pd.notna(active["emotion_values"]):
    st.subheader(active["emotion_label"])
    emotions = dict(i.strip().split("=") for i in active["emotion_values"].split(","))
    selected_emotion = st.selectbox("Выбери эмоцию", list(emotions.keys()))
    user_input = st.text_area(active["input_label"])
    if st.button("Поговорить"):
        prompt = active["prompt"].replace("{emotion}", emotions[selected_emotion]).replace("{input}", user_input)
        answer = query_huggingface(prompt)
        st.session_state.history.append((tab, user_input, answer))
        st.success(answer)
else:
    user_input = st.text_area(active["input_label"])
    if st.button("Получить ответ"):
        prompt = active["prompt"].replace("{input}", user_input)
        answer = query_huggingface(prompt)
        st.session_state.history.append((tab, user_input, answer))
        st.success(answer)

# История
if st.session_state.history:
    st.markdown("### История разговоров:")
    for idx, (topic, q, a) in enumerate(reversed(st.session_state.history[-10:]), 1):
        st.markdown(f"**{idx}. [{topic}]**")
        st.markdown(f"**Ты:** {q}")
        st.markdown(f"**LifeHUB:** {a}")
    if st.button("Очистить историю"):
        st.session_state.history.clear()

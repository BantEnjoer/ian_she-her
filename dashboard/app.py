import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title('Анализ альбома "Goodbye Horses"')

# Загрузка данных
df = pd.read_csv('../data/processed/tracks_clean.csv')

# Разделы
tab1, tab2 = st.tabs(["Статистика", "Тексты песен"])

with tab1:
    st.header("Зависимость популярности от длительности")
    st.image('assets/duration_vs_popularity.png')
    
with tab2:
    st.header("Частые слова в текстах")
    st.image('assets/wordcloud.png')

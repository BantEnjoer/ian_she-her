# Проект

# Авторы

Харазов Роберт Георгревич

ИСУ: 46912

Парсинг, очистка и подготовка данных

Палымов Михаил Сергеевич

ИСУ: 467140

Анализ данных, dashboard

# Описание проекта

Этот проект выполняет анализ треков альбома «Goodbye Horses» исполнителя *ian* с использованием Spotify API (для получения метаданных: длительности, популярности) и Genius API (для загрузки текстов песен). В результате производится:
  
- Сбор данных о треках и их сохранение в CSV (папка **data**),
- Анализ зависимости между длительностью и популярностью,
- Анализ текстов песен (выявление топ-20 часто встречающихся слов),
- Построение визуализаций, сохранённых в папке dashboard и представленных в виде HTML‑дэшборда.

## Установка

1. Получите учетные данные:
   - Создайте приложение в [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/) и получите SPOTIPY_CLIENT_ID и SPOTIPY_CLIENT_SECRET.
   - Получите токен Genius API с [Genius API](https://genius.com/api-clients) и сохраните его как GENIUS_ACCESS_TOKEN.

2. Установите зависимости:

   ```bash
   pip install -r requirements.txt
Перед запуском задайте переменные окружения:

export SPOTIPY_CLIENT_ID="your_spotify_client_id"
export SPOTIPY_CLIENT_SECRET="your_spotify_client_secret"
export GENIUS_ACCESS_TOKEN="your_genius_access_token"
Запуск
Jupyter Notebook:
Запустите ноутбук для поэтапного анализа:

jupyter notebook notebooks/analysis_goodbye_horses.ipynb
Скрипт:
Выполните скрипт для автоматизированного сбора и анализа данных:

python scripts/analysis_tracks.py
После выполнения:

Данные сохраняются в data/tracks.csv.
Графики сохраняются в папке dashboard (файлы: duration_vs_popularity.png и top_words.png).
HTML‑дэшборд доступен в dashboard/dashboard.html.

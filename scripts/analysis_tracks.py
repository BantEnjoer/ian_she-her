import os
import sys
import time
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
import nltk
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Загрузка ресурсов NLTK (если ещё не скачаны)
nltk.download('punkt')
nltk.download('stopwords')

# Импорт для работы со Spotify API
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Импорт для работы с Genius API
import lyricsgenius

# Получение API‑ключей из переменных окружения
SPOTIFY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
GENIUS_ACCESS_TOKEN = os.getenv("GENIUS_ACCESS_TOKEN")

if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
    print("Ошибка: установите SPOTIPY_CLIENT_ID и SPOTIPY_CLIENT_SECRET.")
    sys.exit(1)
if not GENIUS_ACCESS_TOKEN:
    print("Ошибка: установите GENIUS_ACCESS_TOKEN.")
    sys.exit(1)

# Инициализация клиента Spotify
spotify_credentials = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID,
                                               client_secret=SPOTIFY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=spotify_credentials)

# Инициализация клиента Genius
genius = lyricsgenius.Genius(GENIUS_ACCESS_TOKEN, timeout=15, retries=3)
genius.skip_non_songs = True
genius.excluded_terms = ["(Remix)", "(live)"]

def download_album_data(album_name="Goodbye Horses", artist_name="ian"):
    """
    Загружает данные треков альбома из Spotify и тексты песен с Genius.
    Возвращает DataFrame с колонками:
      - track_name
      - duration (в секундах)
      - popularity
      - lyrics
    """
    # Поиск альбома
    query = f"album:{album_name} artist:{artist_name}"
    results = sp.search(q=query, type='album', limit=1)
    items = results.get('albums', {}).get('items', [])
    if not items:
        print("Альбом не найден.")
        sys.exit(1)
    
    album = items[0]
    album_id = album['id']
    print(f"Найден альбом: {album['name']} ({album['release_date']})")
    
    # Получение треков альбома
    tracks_data = []
    results = sp.album_tracks(album_id)
    tracks = results.get('items', [])
    
    for track in tracks:
        track_id = track['id']
        track_name = track['name']
        duration_ms = track['duration_ms']
        duration_sec = duration_ms / 1000
        # Получаем популярность трека
        track_info = sp.track(track_id)
        popularity = track_info.get('popularity', 0)
        
        # Получаем текст песни через Genius API
        print(f"Загружаем текст для трека: {track_name}")
        try:
            song = genius.search_song(title=track_name, artist=artist_name)
            lyrics = song.lyrics if song else ""
            time.sleep(1)  # Задержка для соблюдения лимитов API
        except Exception as e:
            print(f"Ошибка при загрузке текста для {track_name}: {e}")
            lyrics = ""
        
        tracks_data.append({
            "track_name": track_name,
            "duration": duration_sec,
            "popularity": popularity,
            "lyrics": lyrics
        })
    
    df = pd.DataFrame(tracks_data)
    return df

def clean_text(text):
    """
    Предобработка текста:
      - Приведение к нижнему регистру
      - Удаление пунктуации и неалфавитных символов
      - Токенизация и удаление стоп-слов (английских и русских)
    """
    text = text.lower()
    text = re.sub(r'[^a-zа-яё\s]', '', text)
    tokens = word_tokenize(text)
    tokens = [token for token in tokens if token not in stopwords.words('english') 
              and token not in stopwords.words('russian')]
    return tokens

🚬, [15.05.2025 20:51]
def analyze_duration_popularity(df, dashboard_dir):
    """
    Строит scatter plot зависимости популярности от длительности трека.
    Сохраняет график в dashboard_dir/duration_vs_popularity.png.
    """
    plt.figure(figsize=(8,6))
    sns.scatterplot(data=df, x='duration', y='popularity')
    plt.title('Зависимость популярности от длительности трека')
    plt.xlabel('Длительность (сек)')
    plt.ylabel('Популярность')
    out_path = os.path.join(dashboard_dir, "duration_vs_popularity.png")
    plt.savefig(out_path)
    plt.close()
    print(f"График сохранён: {out_path}")
    
    corr = df[['duration', 'popularity']].corr()
    print("Коэффициент корреляции между длительностью и популярностью:")
    print(corr)

def analyze_lyrics(df, dashboard_dir):
    """
    Анализ текстов песен: вычисление топ-20 частотных слов и визуализация.
    Сохраняет график в dashboard_dir/top_words.png.
    """
    all_words = []
    for lyrics in df['lyrics']:
        if pd.isnull(lyrics) or lyrics == "":
            continue
        tokens = clean_text(lyrics)
        all_words.extend(tokens)
    
    counter = Counter(all_words)
    top_words = counter.most_common(20)
    
    print("Топ-20 часто встречающихся слов:")
    for word, count in top_words:
        print(f"{word}: {count}")
    
    words, counts = zip(*top_words) if top_words else ([], [])
    plt.figure(figsize=(10,6))
    sns.barplot(x=list(counts), y=list(words), palette="magma")
    plt.title('Топ-20 часто встречающихся слов в текстах треков')
    plt.xlabel('Количество вхождений')
    plt.ylabel('Слова')
    out_path = os.path.join(dashboard_dir, "top_words.png")
    plt.savefig(out_path)
    plt.close()
    print(f"График сохранён: {out_path}")

def create_dashboard_html(dashboard_dir):
    """
    Создаёт простой HTML‑дэшборд для визуализаций.
    """
    html_content = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Dashboard: Анализ альбома "Goodbye Horses"</title>
</head>
<body>
    <h1>Анализ альбома "Goodbye Horses" исполнителя ian</h1>
    <h2>Зависимость популярности от длительности треков</h2>
    <img src="duration_vs_popularity.png" alt="Duration vs Popularity" style="width:600px;">
    
    <h2>Топ-20 слов в текстах песен</h2>
    <img src="top_words.png" alt="Top Words Chart" style="width:600px;">
</body>
</html>
"""
    html_path = os.path.join(dashboard_dir, "dashboard.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Дэшборд создан: {html_path}")

def main():
    # Определение путей (предполагается, что скрипт находится в project/scripts/)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    dashboard_dir = os.path.join(base_dir, "dashboard")
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(dashboard_dir, exist_ok=True)
    
    # Загрузка данных через Spotify и Genius API
    print("Загрузка данных альбома с использованием Spotify и Genius API...")
    df = download_album_data(album_name="Goodbye Horses", artist_name="ian")
    data_path = os.path.join(data_dir, "tracks.csv")
    df.to_csv(data_path, index=False)
    print(f"Данные сохранены в: {data_path}")
    
    # Анализ зависимости длительности от популярности
    analyze_duration_popularity(df, dashboard_dir)
    
    # Анализ текстов песен
    analyze_lyrics(df, dashboard_dir)
    
    # Генерация HTML‑дэшборда
    create_dashboard_html(dashboard_dir)
    
    print("Анализ завершён.")

if name == '__main__':
    main()

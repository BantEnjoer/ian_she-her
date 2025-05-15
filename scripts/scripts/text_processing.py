import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import string

def clean_text(text):
    # Токенизация и лемматизация
    tokens = word_tokenize(text.lower())
    lemmatizer = WordNetLemmatizer()
    cleaned = [
        lemmatizer.lemmatize(token) 
        for token in tokens 
        if token not in stopwords.words('english') 
        and token not in string.punctuation
    ]
    return ' '.join(cleaned)

def process_data():
    df = pd.read_json('../data/raw/tracks.json')
    df['duration_min'] = df['duration_ms'] / 60000
    df['lyrics_clean'] = df['lyrics'].apply(clean_text)
    df.to_csv('../data/processed/tracks_clean.csv', index=False)

if __name__ == "__main__":
    process_data()

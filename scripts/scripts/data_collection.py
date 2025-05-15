import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import json
import os

# Авторизация в Spotify API
client_id = 'your_client_id'
client_secret = 'your_client_secret'
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

def get_album_tracks(album_name="Goodbye Horses", artist="Ian"):
    results = sp.search(q=f"album:{album_name} artist:{artist}", type='album')
    album_id = results['albums']['items'][0]['id']
    tracks = sp.album_tracks(album_id)
    
    track_data = []
    for track in tracks['items']:
        features = sp.audio_features(track['id'])[0]
        track_data.append({
            'name': track['name'],
            'duration_ms': track['duration_ms'],
            'popularity': sp.track(track['id'])['popularity'],
            'lyrics': ""  # Заполняется отдельно через Genius API
        })
    
    os.makedirs('../data/raw', exist_ok=True)
    with open('../data/raw/tracks.json', 'w') as f:
        json.dump(track_data, f)

if __name__ == "__main__":
    get_album_tracks()

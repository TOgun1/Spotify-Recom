import pandas as pd
from spotify_client import get_artists_details, search_tracks_by_genre
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def create_dataframe(tracks_data):
    df = pd.DataFrame(tracks_data, columns=['track_id', 'track_name', 'artist_ids', 'artist_names', 'popularity']).drop_duplicates(subset='track_id')
    return df

def extract_track_data(tracks_data,parsed_data):
    for t in tracks_data:
            track_id = t['id']
            track_name = t['name']
            artist_ids = [artist['id'] for artist in t['artists']]
            artist_names = [artist['name'] for artist in t['artists']]
            popularity = t.get('popularity', 0)
            
            parsed_data.append((track_id, track_name, artist_ids, artist_names, popularity))
    return parsed_data

def extract_recently_played_data(recently_played, parsed_data):
    for item in recently_played['items']:
            t = item.get('track', {})
            track_id = t.get('id')
    
            if not track_id:
                continue
    
            track_name = t.get('name')
            artist_ids = [artist['id'] for artist in t.get('artists', [])]
            artist_names = [artist['name'] for artist in t.get('artists', [])]
            popularity = t.get('popularity', 0)
    
            parsed_data.append((track_id, track_name, artist_ids, artist_names, popularity))

def score_and_rank_underground(candidates, known_artists=None, max_listeners: int = 100000, top_n: int = 20, max_per_artist: int = 2):
    if not candidates:
        return []

    
    df = pd.DataFrame(candidates)

    if known_artists:
        df = df[~df['artist_name'].str.lower().isin(known_artists)].copy()
    if df.empty:
        return []

   
    df['listeners'] = pd.to_numeric(df['listeners'], errors='coerce').fillna(0)
    df['match_score'] = pd.to_numeric(df['match_score'], errors='coerce').fillna(0)

    
    df_filtered = df[df['listeners'] <= max_listeners].copy()

    
    if df_filtered.empty:
        median_listeners = df['listeners'].median()
        df_filtered = df[df['listeners'] <= median_listeners].copy()

   
    df_filtered['underground_score'] = df_filtered['match_score'] / (np.log1p(df_filtered['listeners']) + 1)
    

    df_sorted = df_filtered.sort_values(by='underground_score', ascending=False)
    df_clean = df_sorted.drop_duplicates(subset=['track_name', 'artist_name'])
    df_clean = df_clean.groupby('artist_name').head(max_per_artist)

    return df_clean.head(top_n)[['artist_name', 'track_name', 'listeners', 'underground_score']].to_dict(orient='records')
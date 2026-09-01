import pandas as pd
from spotify_client import get_related_artists, get_artists_details, get_artist_top_tracks
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def create_dataframe(tracks_data):
    df = pd.DataFrame(tracks_data, columns=['track_id', 'track_name', 'artist_ids', 'artist_names', 'popularity']).drop_duplicates(subset='track_id')
    return df

def build_lookup_dict(details):
    info = {}
    for artist in details:
        info[artist['id']] = {
            'genres': artist.get('genres', []),
            'followers': artist['followers']['total'],
        }
    return info

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

def separate_into_unique_artists(sp,df):
     unique_artists_ids = list({artist_id for artist_list in df['artist_ids'] for artist_id in artist_list})
     batch_size = 50
     artist_details = []
     for i in range(0, len(unique_artists_ids), batch_size):
         batch = unique_artists_ids[i:i + batch_size]
         result = get_artists_details(sp, batch)
         artist_details.extend(result['artists'])
     return artist_details

def get_genres_for_row(artist_ids, info):
    genres = set()
    for artist_id in artist_ids:
        genres.update(info.get(artist_id, {}).get('genres', []))
    return sorted(genres)

def get_min_followers_for_row(artist_ids, info):
    follower_counts = [info.get(aid, {}).get("followers", 0) for aid in artist_ids]
    if not follower_counts:
        return 0
    return min(follower_counts)

def construct_related_artists_df(df, sp, artist_ids):
    graph = {}
    parsed_data = []
    unique_tracks = []
    artist_ids = artist_ids[:10]
    for artist_id in artist_ids:
        related_artists = get_related_artists(sp, artist_id)
        top_related_artists = related_artists['artists'][:10] if len(related_artists['artists']) > 10 else related_artists['artists']
        for artist in top_related_artists:
            top_tracks = get_artist_top_tracks(sp, artist['id'])
            tracks = top_tracks['tracks']
            unique_tracks.extend(track for track in tracks if track['id'] not in df['track_id'].values)
        
    extract_track_data(unique_tracks, parsed_data)

    candidate_df = create_dataframe(parsed_data)
    artist_details = separate_into_unique_artists(sp, candidate_df)

    table = build_lookup_dict(artist_details)
    candidate_df['genres'] = candidate_df['artist_ids'].apply(lambda x: get_genres_for_row(x, table))
    candidate_df['min_followers'] = candidate_df['artist_ids'].apply(lambda x: get_min_followers_for_row(x, table))

    return candidate_df

def filter_underground(df):
    filtered_df = df[df['min_followers'] < 50000]
    return filtered_df

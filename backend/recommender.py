import pandas as pd
from spotify_client import get_artists_details, search_tracks_by_genre
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

def get_top_genres(df, top_n=5):
    all_genres = [g for genre_list in df['genres'] for g in genre_list]
    if not all_genres:
        return []
    genre_counts = pd.Series(all_genres).value_counts()
    return genre_counts.head(top_n).index.tolist()

def construct_candidate_df_from_search(df, sp, genres, results_per_genre=30):
    unique_tracks = []
    existing_ids = set(df['track_id'].values)
    seen_ids = set()

    for genre in genres:
        
        for offset in range(0, results_per_genre, 10):
            result = search_tracks_by_genre(sp, genre, limit=10, offset=offset)
            tracks = result.get('tracks', {}).get('items', [])
            if not tracks:
                break
            for track in tracks:
                if track['id'] in existing_ids or track['id'] in seen_ids:
                    continue
                seen_ids.add(track['id'])
                unique_tracks.append(track)

    parsed_data = []
    extract_track_data(unique_tracks, parsed_data)

    candidate_df = create_dataframe(parsed_data)
    artist_details = separate_into_unique_artists(sp, candidate_df)

    table = build_lookup_dict(artist_details)
    candidate_df['genres'] = candidate_df['artist_ids'].apply(lambda x: get_genres_for_row(x, table))

    return candidate_df



def combine_dataframes(df1, df2):
    combined_df = pd.concat([df1, df2], ignore_index=True)
    return combined_df

def compute_similarity(combined_df):
    genre_strings = combined_df['genres'].apply(lambda genres: ' '.join(g.replace(' ', '_') for g in genres))
    if not genre_strings.str.strip().any():
        return None  # no genre data available at all
    vectorizer = CountVectorizer(token_pattern=r"[^\s]+")
    genre_matrix = vectorizer.fit_transform(genre_strings)
    return cosine_similarity(genre_matrix)

def rank_candidates(df,candidate_df, similarity_matrix):
    if similarity_matrix is None:
        return candidate_df.head(20)
    candidate_vs_taste = similarity_matrix[len(df):, :len(df)] # Skips the first len(df) rows to get only the candidate tracks and skips the first len(df) columns to get only the user's taste tracks.
    scores = candidate_vs_taste.mean(axis=1) # Compute the average similarity score for each candidate track across all of the user's taste tracks.
    candidate_df = candidate_df.assign(score=scores)
    ranked = candidate_df.sort_values(by='score', ascending=False)
    top_recom = ranked.head(20)
    return top_recom


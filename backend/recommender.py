import pandas as pd
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
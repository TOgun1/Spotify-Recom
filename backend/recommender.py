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
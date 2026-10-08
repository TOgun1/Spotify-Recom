import os
import requests
from dotenv import load_dotenv

load_dotenv()
LASTFM_API_KEY = os.getenv("LASTFM_API_KEY")
API_URL = "http://ws.audioscrobbler.com/2.0/"

def get_similar_artists(artist_name, limit: int = 8):
    params = {
        "method": "artist.getsimilar",
        "artist": artist_name,
        "api_key": LASTFM_API_KEY,
        "format": "json",
        "limit": limit
    }
    response = requests.get(API_URL, params=params)
    data = response.json()
    
    similar_artists = []
    if "similarartists" in data and "artist" in data["similarartists"]:
        for artist in data["similarartists"]["artist"]:
            match_score = float(artist.get("match", 0.0))
            similar_artists.append({
                "name": artist["name"],
                "match_score": match_score
            })
    return similar_artists

def get_artist_top_tracks(artist_name, match_score, limit: int = 10):
    params = {
        "method": "artist.gettoptracks",
        "artist": artist_name,
        "api_key": LASTFM_API_KEY,
        "format": "json",
        "limit": limit
    }
    response = requests.get(API_URL, params=params)
    data = response.json()
    
    candidates = []
    if "toptracks" in data and "track" in data["toptracks"]:
        for track in data["toptracks"]["track"]:
            listeners = int(track.get("listeners", 0))
            playcount = int(track.get("playcount", 0))
            candidates.append({
                "artist_name": artist_name,
                "track_name": track["name"],
                "listeners": listeners,
                "playcount": playcount,
                "match_score": match_score
            })
    return candidates

def select_underground_candidates(seed_artist_names: list):
    all_candidates = []
    for seed_artist in seed_artist_names:
        similar = get_similar_artists(seed_artist, limit=8)
        for item in similar:
            tracks = get_artist_top_tracks(item["name"], item["match_score"], limit=8)
            all_candidates.extend(tracks)
    return all_candidates


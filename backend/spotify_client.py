import os
from spotipy.oauth2 import SpotifyOAuth
import spotipy
from dotenv import load_dotenv

load_dotenv()

SCOPE = "user-top-read user-read-recently-played user-library-read playlist-read-private"

#OAuth Manager
def get_oauth_manager():
    return SpotifyOAuth(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
        scope=SCOPE
    )

def get_authorize_url():
    oauth = get_oauth_manager()
    return oauth.get_authorize_url()

def get_access_token(code):
    oauth = get_oauth_manager()
    token_info = oauth.get_access_token(code, as_dict=True, check_cache=False)
    return token_info["access_token"]

def get_spotify_client(access_token):
    return spotipy.Spotify(auth=access_token)

#Recommendation Algorithm
def get_artist_albums(sp, artist_id):
    return sp.artist_albums(artist_id, limit=1)

def get_album_tracks(sp, album_id):
    return sp.album_tracks(album_id)

def get_top_tracks(sp):
    return sp.current_user_top_tracks(limit=50, time_range='medium_term')

def get_recently_played(sp):
    return sp.current_user_recently_played(limit=50)

def get_artists_details(sp, artist_ids):
    artists = []
    for artist_id in artist_ids:
        artist = sp.artist(artist_id)
        artists.append(artist)
    return {"artists": artists}

def get_related_artists(sp, artist_id):
    return sp.artist_related_artists(artist_id)

import os
from spotipy.oauth2 import SpotifyOAuth
import spotipy
from dotenv import load_dotenv

load_dotenv()

SCOPE = "user-top-read user-read-recently-played user-library-read playlist-read-private"

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
import os
from spotipy.oauth2 import SpotifyOAuth
import spotipy
from dotenv import load_dotenv

load_dotenv()

SCOPE = "user-top-read user-read-recently-played user-library-read playlist-read-private"

def get_authorise_url():
    sp_oauth = SpotifyOAuth(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
        scope=SCOPE
    )
    return sp_oauth.get_authorize_url()
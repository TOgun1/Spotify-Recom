from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from spotify_client import get_artists_details, get_authorize_url, get_access_token,get_artists_details, get_spotify_client,get_top_tracks, get_recently_played, get_related_artists, get_artist_top_tracks
import os
from recommender import build_lookup_dict, construct_related_artists_df, create_dataframe, extract_recently_played_data, extract_track_data, get_genres_for_row, get_min_followers_for_row, separate_into_unique_artists
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET"))

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/login")
def login():
    auth_url = get_authorize_url()
    return RedirectResponse(auth_url)

@app.get("/callback")
def callback(request: Request, code: str):
    token = get_access_token(code)
    request.session["access_token"] = token
    return RedirectResponse(url="/recommendations")

@app.get("/recommendations")
def recommendations(request: Request):
    token = request.session.get("access_token")
    sp = get_spotify_client(token)
    parsed_data = []

    top_tracks = get_top_tracks(sp)
    tracks_data = top_tracks['items']
    extract_track_data(tracks_data, parsed_data)

    recently_played = get_recently_played(sp)
    extract_recently_played_data(recently_played, parsed_data)

    df = create_dataframe(parsed_data)
    artist_details = separate_into_unique_artists(sp,df)

    table = build_lookup_dict(artist_details)
    df['genres'] = df['artist_ids'].apply(lambda x: get_genres_for_row(x, table))
    df['min_followers'] = df['artist_ids'].apply(lambda x: get_min_followers_for_row(x, table))

    #Build Candidate Pool
    candidate_df = construct_related_artists_df(df, sp, df['artist_ids'].explode().unique().tolist())
    
    return {"top_tracks": df}
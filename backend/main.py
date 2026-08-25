from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from spotify_client import get_artists_details, get_authorize_url, get_access_token,get_artists_details, get_spotify_client,get_top_tracks, get_recently_played, get_related_artists, get_artist_top_tracks
import os
from recommender import build_lookup_dict, create_dataframe
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
    for t in tracks_data:
        track_id = t['id']
        track_name = t['name']
        artist_ids = [artist['id'] for artist in t['artists']]
        artist_names = [artist['name'] for artist in t['artists']]
        popularity = t.get('popularity', 0)
        
        parsed_data.append((track_id, track_name, artist_ids, artist_names, popularity))

    recently_played = get_recently_played(sp)
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

    df = create_dataframe(parsed_data)
    unique_artists_ids = {artist_id for artist_list in df['artist_ids'] for artist_id in artist_list}
    batch_size = 50
    artist_details = []

    for i in range(0, len(unique_artists_ids), batch_size):
        batch = unique_artists_ids[i:i + batch_size]
        result = get_artists_details(sp, batch)
        artist_details.extend(result['artists'])

    table = build_lookup_dict(artist_details)
    return {"top_tracks": parsed_data}
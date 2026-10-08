import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware

from spotify_client import (
    create_underground_playlist,
    get_access_token,
    get_authorize_url,
    get_recently_played,
    get_spotify_client,
    get_top_tracks,
    resolve_tracks_to_uris,
)
from lastfm_client import select_underground_candidates
from recommender import (
    create_dataframe,
    extract_recently_played_data,
    extract_track_data,
    score_and_rank_underground,
)

load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # Your Vite frontend URL
    allow_credentials=True, # Required if you are using session cookies
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET"))

class TrackIn(BaseModel):
    artist_name: str
    track_name: str


class PlaylistRequest(BaseModel):
    playlist_name: str
    tracks: list[TrackIn]

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

    artist_counts = df['artist_names'].explode().value_counts()
    seed_artists = artist_counts.head(5).index.tolist()
    known_artists = {name.lower() for name in artist_counts.index}

    candidates = select_underground_candidates(seed_artists)
    print("candidates from Last.fm:", len(candidates))
    recs = score_and_rank_underground(candidates, known_artists=known_artists)
    print("after ranking:", len(recs))

    
    return {"seeds": seed_artists, "recommendations": recs}

@app.post("/create_playlist")
def create_playlist(request: Request, payload: PlaylistRequest):
    token = request.session.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not logged in")
    sp = get_spotify_client(token)

    tracks = [t.model_dump() for t in payload.tracks]
    uris = resolve_tracks_to_uris(sp, tracks)
    url = create_underground_playlist(sp, payload.playlist_name, uris)
    return {"playlist_url": url, "tracks_added": len(uris)}

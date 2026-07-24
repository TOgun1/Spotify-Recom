from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from spotify_client import get_authorize_url, get_access_token, get_spotify_client
import os
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
    return {"access_token": "success"}
# Underground Song Recommender

As someone who loves listening to more obscure music and underground artists, I noticed that Spotify tended to only recommend music from artists I already knew or who were mainstream. Hence, I thought it may be fun to build my own application to fix this issue. 

Recently, Spotify heavily restricted and deprecated access to several of their core recommendation endpoints. To bypass this limitation and still build a working engine, I pivoted to integrating the Last.fm API. I used Last.fm's data to cross-reference artists, fetch global listener metrics, and then apply the underground filter.

## Demo Link

Available at: https://underground-song-recommendation.onrender.com/
(Although since it is hosted on the free tier, initial startup can be up to around a minute long)

**Additonally, due to spotify developer account limitations for individuals, the app can only be used by up to 5 users that I explicitly give permission to via the developer platform.
Hence, for recruiters wanting to see how it works see the demo video below.**


https://github.com/user-attachments/assets/1ff7fed5-f535-40bf-bf40-c5c4a664da01

## Features

* **Secure Spotify Authentication:** Implements the Spotify OAuth flow for secure user login.
* **Intelligent Recommendation Engine:** Analyzes users' top tracks and recently played history to establish a baseline taste profile.
* **Underground Discovery:** Integrates Last.fm and Spotify search to filter and rank tracks based on listener counts, ensuring recommendations are genuine hidden gems.
* **One-Click Export:** Automatically creates a private playlist in the user's Spotify account and populates it with the recommended tracks.
* **Seamless Full-Stack Architecture:** Built with a React frontend served directly by a FastAPI backend, eliminating CORS issues and third-party cookie blocking during OAuth.

## Tech Stack

**Frontend:**
* React (Vite)
* Tailwind CSS
* Axios

**Backend:**
* Python (FastAPI)
* Spotipy (Spotify API wrapper)
* Pandas & NumPy (Data manipulation and scoring)
* Uvicorn (ASGI server)

**Deployment:**
* Hosted on Render (Unified backend serving static frontend files)


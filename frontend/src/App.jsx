import { useState, useEffect } from 'react'
import axios from 'axios'

function App() {
  const [tracks, setTracks] = useState([])
  const [loading, setLoading] = useState(false)

  // 1. Send the user to your FastAPI login route
  const handleLogin = () => {
    window.location.href = 'http://localhost:8000/login'
  }

  // 2. Fetch recommendations (you would call this after they return from login)
  const fetchRecommendations = async () => {
    setLoading(true)
    try {
      const response = await axios.get('http://localhost:8000/recommendations', {
        withCredentials: true 
      })
      setTracks(response.data.recommendations)
    } catch (error) {
      console.error("Error fetching tracks", error)
    }
    setLoading(false)
  }

  return (
    <div style={{ padding: '2rem', fontFamily: 'sans-serif' }}>
      <h1>Underground Spotify Recommender</h1>
      <button onClick={handleLogin}>Login with Spotify</button>
      <button onClick={fetchRecommendations} disabled={loading} style={{ marginLeft: '1rem' }}>
        {loading ? 'Generating...' : 'Get Recommendations'}
      </button>

      <ul>
        {tracks.map((track, index) => (
          <li key={index}>
            <strong>{track.track_name}</strong> by {track.artist_name}
          </li>
        ))}
      </ul>
    </div>
  )
}

export default App
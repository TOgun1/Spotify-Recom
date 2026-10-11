import { useState, useEffect } from 'react'
import axios from 'axios'
import Alert from './components/Alert'
import TrackList from './components/TrackList'

function App() {
  const [tracks, setTracks] = useState([])
  const [loading, setLoading] = useState(false)
  const [alertMessage, setAlertMessage] = useState(null)
  const [exporting, setExporting] = useState(false)

  const handleLogin = () => {
    window.location.href = '/api/login'
  }

  const fetchRecommendations = async () => {
    setLoading(true)
    try {
      const response = await axios.get('/api/recommendations', {
        withCredentials: true 
      })
      setTracks(response.data.recommendations)
    } catch (error) {
      console.error("Error fetching tracks", error)
    }
    setLoading(false)
  }

  const createPlaylist = async () => {
    setExporting(true)
    try {
      const response = await axios.post('/api/create_playlist', {
        playlist_name: "My Underground Gems",
        tracks: tracks
      }, {
        withCredentials: true
      })
      
      setAlertMessage(`Success! Check your Spotify. Added ${response.data.tracks_added} tracks.`)
      setTimeout(() => setAlertMessage(null), 5000)
    } catch (error) {
      console.error("Error creating playlist", error)
      setAlertMessage("Failed to create playlist.")
      setTimeout(() => setAlertMessage(null), 5000)
    }
    setExporting(false)
  }

  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100 font-sans p-8 flex flex-col items-center">
      <Alert message={alertMessage} />
      
      <div className="max-w-3xl w-full text-center space-y-4 mb-12 mt-8">
        <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-green-400 to-emerald-600">
          Underground Song Recommender
        </h1>
        <p className="text-zinc-400 text-lg">
          Discover hidden gems based on your Spotify listening history.
        </p>
      </div>

      
      <div className="flex flex-wrap gap-4 justify-center mb-12">
        <button 
          onClick={handleLogin} 
          className="bg-zinc-800 hover:bg-zinc-700 text-white font-semibold py-3 px-6 rounded-full transition-all duration-200 shadow-lg"
        >
          Login with Spotify
        </button>
        
        <button 
          onClick={fetchRecommendations} 
          disabled={loading}
          className="bg-green-500 hover:bg-green-400 disabled:bg-zinc-700 disabled:text-zinc-500 text-black font-bold py-3 px-6 rounded-full transition-all duration-200 shadow-lg flex items-center"
        >
          {loading ? (
            <span className="animate-pulse">Mining Last.fm data...</span>
          ) : (
            'Generate Recommendations'
          )}
        </button>

        <button 
          onClick={createPlaylist} 
          disabled={tracks.length === 0 || exporting}
          className="bg-zinc-100 hover:bg-white disabled:bg-zinc-800 disabled:text-zinc-600 text-black font-bold py-3 px-6 rounded-full transition-all duration-200 shadow-lg"
        >
          {exporting ? (
            <span className="animate-pulse">Exporting to Spotify...</span>
          ) : (
            'Export to Spotify'
          )}
        </button>
      </div>

      <div className="max-w-3xl w-full">
        <TrackList tracks={tracks} />
      </div>
      
    </div>
  )
}

export default App
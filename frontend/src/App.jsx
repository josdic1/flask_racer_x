import { useState, useEffect } from 'react'
import { healthCheck, getTracks } from './services/api'

function App() {
  const [health, setHealth] = useState(null)
  const [tracks, setTracks] = useState([])

  useEffect(() => {
    checkHealth()
    fetchTracks()
  }, [])

  const checkHealth = async () => {
    try {
      const response = await healthCheck()
      setHealth(response.data)
    } catch (error) {
      console.error('Health check failed:', error)
    }
  }

  const fetchTracks = async () => {
    try {
      const response = await getTracks()
      setTracks(response.data)
    } catch (error) {
      console.error('Error:', error)
    }
  }

  return (
    <div className="App">
      <h1>Flask Racer X</h1>
      {health && <p>✅ {health.message}</p>}
      <h2>Tracks</h2>
      {tracks.length === 0 ? (
        <p>No tracks yet</p>
      ) : (
        <ul>
          {tracks.map(track => (
            <li key={track.id}>{track.name} - {track.location}</li>
          ))}
        </ul>
      )}
    </div>
  )
}

export default App
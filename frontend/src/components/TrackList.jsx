
export default function TrackList({ tracks }) {
  if (tracks.length === 0) return null;

  return (
    <div className="bg-zinc-900/50 rounded-2xl p-6 border border-zinc-800/50">
      <h2 className="text-xl font-bold mb-4 px-2 text-zinc-200">Your Playlist Tracks</h2>
      <ul className="space-y-2">
        {tracks.map((track, index) => (
          <li key={index} className="flex items-center gap-4 p-3 hover:bg-zinc-800/80 rounded-xl transition-colors group">
            <span className="text-zinc-500 font-mono w-6 text-right group-hover:text-green-400">
              {index + 1}
            </span>
            <div className="flex flex-col">
              <span className="text-zinc-100 font-medium">{track.track_name}</span>
              <span className="text-zinc-400 text-sm">{track.artist_name}</span>
            </div>
          </li>
        ))}
      </ul>
    </div>
  )
}
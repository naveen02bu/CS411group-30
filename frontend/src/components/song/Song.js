import './Song.css' 

function Song({song}) { 
  
  return ( 
      <a href={`${song.track.external_urls.spotify}`} className='song-link'>
        <div className='song-div'> 
          <img src={song.track.album.images[0].url} className='song-image' />
          <p className='song-name'>{song.track.name}</p>
          <p className='song-artist'>{song.track.artists[0].name}</p>
        </div>
      </a>
  )
}

export default Song

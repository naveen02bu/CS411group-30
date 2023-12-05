import './Results.css';
import Header from '../header/Header';
import Footer from '../footer/Footer';
import Song from '../song/Song';
import { useState, useEffect} from 'react';


function Results() {

  // State 
  const [songs, setSongs] = useState([]); // Array of songs
  const [playlistLink, setPlaylistLink] = useState({}); // Link to playlist

  var Loaded = false;
  // Effect
  // This effect runs only once after the first render.
  useEffect(() => { 
    if (Loaded == false) {
      showPlaylist();
      Loaded = true;
    }
  }, [])

  const showPlaylist = () => {
    // Make request to Flask backend's /login endpoint
    fetch('http://localhost:5000/playlists', { 
      credentials: 'include'
    })
      .then(response => {
        // Check if the response status is OK (status code 200)
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        // Handle the data, e.g., update the UI with the playlists
        console.log(data);
        setSongs(data.tracks.items);
        setPlaylistLink(data.external_urls.spotify);
      })
      .catch(error => {
        // Handle the error, e.g., display an error message to the user
        console.error('Error during login:', error.message);
      });
  };

  return (
    <div className='results-div'>
      <Header />
      <h1 className='results-title'>Playlist</h1>
      {songs.length > 0 ? (
        <>
          <h2 className='results-text'>Check it out on your Spotify:&nbsp;</h2>
          <a className='playlist-link' href={`${playlistLink}`}>
            {`${playlistLink}`}
          </a>
        </>
      ) : null}
      <div className='playlist-grid'>
        {songs.map(song => (
          <Song key={song.track.id} song={song} />
        ))}
      </div>
      <Footer />
    </div>
  )
}
export default Results
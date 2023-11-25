import './Results.css';
import Header from '../header/Header'
import Nav from '../nav/Nav';
import { useEffect} from 'react';
import Footer from '../footer/Footer';


function Results() {
  
  var Loaded = false;

  useEffect(() => { 
    if (Loaded == false) {
      showPlaylists();
      Loaded = true;
    }
  }, [])

  const showPlaylists = () => {
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
        // Append images 
        data.items.forEach(playlist => {
          const img = document.createElement('img');
          img.src = playlist.track.album.images[0].url;
          document.querySelector('.results-div').append(img);
        });
      })
      .catch(error => {
        // Handle the error, e.g., display an error message to the user
        console.error('Error during login:', error.message);
      });
  };

  return (
    <div className='results-div'>
      <Header />
      <Nav />
      <h1 className='results-title'>Playlist</h1>
      <Footer />
    </div>
  )
}
export default Results
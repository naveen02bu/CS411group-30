import './Footer.css';
import { NavLink } from 'react-router-dom';
import spotifyLogo from './spotify-logo.png';

function Footer() { 
  return (
    <div className='footer-div'>
      <div className='footer-right' >
        <NavLink to="https://open.spotify.com/" target="_blank" rel="noopener noreferrer">
        <img className='spotify-logo' src={spotifyLogo}/>
        </NavLink>
      </div>
    </div>
  )
}
export default Footer
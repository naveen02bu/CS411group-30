import './Footer.css';
import spotifyLogo from '../../images/spotify-logo.png';
import { NavLink } from 'react-router-dom';

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
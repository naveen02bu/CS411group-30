import './Footer.css';
import { NavLink } from 'react-router-dom';
import spotifyLogo from './spotify-logo.png';

function Footer() { 
  return (
    <div className='footer-div'>
      <div className='footer-right' >
        <img className='spotify-logo' src={spotifyLogo}/>
      </div>
    </div>
  )
}
export default Footer
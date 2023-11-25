import './Header.css';
import { NavLink } from 'react-router-dom';
import bookifyIcon from '../../images/bookify-icon.png';

function Header() { 
  return (
    <div className='header-div'>
      <div className='header-left'>
        <img className='header-bookify-icon' src={bookifyIcon}/>
        <p className='header-app-name'>Bookify</p>
      </div>
        <div className='header-right' >
          <NavLink className='log-out-link' to='/'>Log out</NavLink>
        </div>
    </div>
  )
}
export default Header
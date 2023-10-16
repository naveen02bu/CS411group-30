import './Header.css';
import { NavLink } from 'react-router-dom';
import bookifyIcon from './bookify-icon.png';

function Header() { 
  return (
    <div className='header-div'>
      <div className='left'>
        <img className='bookify-icon' src={bookifyIcon}/>
        <p className='app-name'>Bookify</p>
      </div>
        <div className='right' to='/'>
          <NavLink className='log-out-link' to='/'>Log out</NavLink>
        </div>
    </div>
  )
}
export default Header
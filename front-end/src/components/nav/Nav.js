import './Nav.css';
import { NavLink } from 'react-router-dom';
import { PiBook } from 'react-icons/pi';
import { PiMusicNotesSimple } from 'react-icons/pi';

function Nav() { 
  return (
    <div className='nav-div'>
        <NavLink activeClassName="active" className='icon-link' to='/book'> 
          <div className='icon-div'>
            <PiBook className='icon' /> 
          </div>
        </NavLink>
        <NavLink activeClassName="active" className='icon-link' to='/playlist'>
          <div className='icon-div'>
            <PiMusicNotesSimple className='icon' />
          </div>
        </NavLink>
      </div>   
  )
}
export default Nav
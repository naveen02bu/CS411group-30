import './Login.css';
import { NavLink } from 'react-router-dom';

function Login() {
  return (
    <div className='login-div'>
      <h1 className='login-title'>Welcome to Bookify!</h1>
      <p>Log in to your spotify account</p>
      <NavLink className='login-link' to='/book'>Log in</NavLink>
    </div>
  )
}

export default Login
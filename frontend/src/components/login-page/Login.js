import './Login.css';
import axios from 'axios'; 
import bookifyIcon from '../../images/bookify-icon.png';
import Footer from '../footer/Footer.js';


function Login() {

  const handleLogin = () => { 
    // Make request to Flask backend's /login endpoint 
    axios.get('http://localhost:5000/login') 
      .then(response => {
        // Redirect the user to the Spotify login page
        window.location.href = response.data.auth_url;
      })
      .catch(error => {
        // Handle the error, e.g., display an error message to the user
        console.error('Error during login:', error);
      });
  };

  return (
    <div className='login-div'>
      <div className='login-div-middle'>
        <div className='login-left'> 
          <div className='login-logo'>
            <img className='login-bookify-icon' src={bookifyIcon}/>
            <p className='login-app-name'>Bookify</p>
          </div>
          <h3 className='login-description'>A site where you can get a Spotify playlist based off of a book.</h3>
        </div>
          <div className='login-right'>
            <div className='login-right-log-in'>
              <p className='login-directions'>Get started by logging into your Spotify account</p>
              <button className='login-button' onClick={handleLogin}>Log in</button>
            </div>
            <div className='login-right-sign-up'> 
              <p className='login-directions'>Don't have an account?</p>
              <a href='https://www.spotify.com/signup'><button className='login-button'>Sign up</button></a>
            </div>
          </div>
      </div>
    </div>
  )
}

export default Login
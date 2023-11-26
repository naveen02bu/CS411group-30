import './Input.css';
import Header from '../header/Header'
import Footer from '../footer/Footer';
import { useState } from 'react';

function Input() {

  const [isLoading, setIsLoading] = useState(false);

  function handleSubmit(event) { 
    event.preventDefault(); // Prevent the page from refreshing 

    // Get the data from the form 
    const title = event.target.elements.title.value; 
    const author = event.target.elements.author.value; 

    // Create a data object to send to the backend 
    const formData = { 
      title: title, 
      author: author
    }; 

    // Show the loading div
    if (formData.title != '' || formData.author != '') {
      setIsLoading(true);
    }

    // Send the data to the backend 
    fetch('http://localhost:5000/create-playlist', { 
      method: 'POST', 
      headers: { 
        'Content-Type': 'application/json' 
      }, 
      body: JSON.stringify(formData),
      credentials: 'include'
    }) 
      .then(response => response.json()) 
      .then(data => { 
        console.log('Success:', data); 
        // Redirect the user to the results page 
        window.location.href = '/playlist'; 
      }) 
      .catch((error) => { 
        console.error('Error:', error); 
      })
      .finally(() => {
        // Hide the loading div
        setIsLoading(false);
      });
  }


  return (
    <div className='input-div'>
      <Header />
        <h1 className='input-title'>Book</h1>
        <h2 className='input-info'>The playlist will be created based on the genre, setting, language, mood, tone, and themes</h2>
        <div className='input-middle'>
          <h2 className='input-directions'>Enter a book title and author</h2>

          <form onSubmit={handleSubmit} className='input-form'> 
            <div className='input-section'>
              <p className='input-category'>Title:</p>
              <input type="text" name="title"/>
            </div>

            <div className='input-section'>
              <p className='input-category'>Author:</p>
              <input type="text" name="author"/>
            </div>

            <div className='input-button-div'>
              <button type="submit" className='input-button'>Submit</button>
            </div>
          </form>

        </div>
        {/* Conditional rendering of loading div */}
        {isLoading && 
        <div className='input-loading'>
          <p className='input-loading-text'>Creating your playlist</p>
          <div class="dot-pulse"></div>
        </div>
        }
      <Footer />
    </div>
  )
}
export default Input
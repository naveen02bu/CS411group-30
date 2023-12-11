import './Review.css'

function Review({onClose}) {

    
    const handleSubmit = (event) => {
        event.preventDefault();  // Prevents the default form submission behavior
    
   
    
        // Provides access to each textbox 
        const spotifyID = event.target.elements.spotifyID.value;
        const rateQuality = event.target.elements.rateQuality.value;
        const overallExperience = event.target.elements.overallExperience.value;
        const delay = event.target.elements.delay.value;
        const features = event.target.elements.features.value;

        // Create an object to send to the backend 
        const feedbackData = { 
            spotifyID: spotifyID,
            rateQuality: rateQuality,
            overallExperience: overallExperience,
            delay: delay,
            features: features, 
          }; 

          console.log('Feedback Data:', feedbackData); // To verify data in website's console
          onClose();
         
    // Submit data to backend
    fetch('http://localhost:5000/save-feedback', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(feedbackData),
      })
        .then((response) => response.json())
        .then((responseData) => {
          console.log('Server response:', responseData);
          onClose();
        })
        .catch((error) => {
          console.error('Error submitting feedback:', error);
        });
    };

        return (
            // Creates the Outline of the Form
            <div className='review-div'>
                <h1 className='review-header'> Share Your Feedback With Us!</h1>
                <div className="transparent-line"></div>

               
                 <form onSubmit={handleSubmit} className='input-feedback'> 
                    
                    <label className="labelWithColor"> SpotifyID: 
                        <input placeholder="Type Here.." type="text" name="spotifyID" />
                    </label>

                    <label  className="labelWithColor">How Would You Rate The Quality of the Spotify Playlist? (1-5)
                        
                    <input placeholder="e.g. 5" type="text" name="rateQuality"/>
                     
                    </label>

                    <label className="labelWithColor">How Was Your Overall Experience? 
                        <textarea
                            placeholder="Type Here.."
                            rows = {5}
                            cols = {50}
                            name = "overallExperience"
                            style={{ resize: 'none' }}
                        ></textarea>
                    </label>

                    <label className="labelWithColor">Did You Encounter Any Delays While Using The Application? If Yes, At Which Point Did You Experience Them?
                        <textarea
                            placeholder="Type Here.."
                            rows = {5}
                            cols = {50}
                            name = "delay"
                            style={{ resize: 'none' }}
                        ></textarea>
                    </label>

                    <label className="labelWithColor">Are There Additional Features You Would Like To See?
                        <textarea
                            placeholder="Type Here.."
                            rows = {5}
                            cols = {50}
                            name = "features"
                            style={{ resize: 'none' }}
                        ></textarea>
                    </label>

                    <button type="submit" className='submit-button'>Submit</button>

                </form>
             
             </div>  
            )
        
        }
export default Review;

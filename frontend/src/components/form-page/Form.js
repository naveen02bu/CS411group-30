import './Form.css'
import React, {useState} from "react"

function Form() {
    const [Rating, setMyRating] = useState("1")

    const handleChange = (event) => {
        setMyRating(event.target.value)
    }
   
        return (
            <div className='Form-div'>
               <form>
                    

                    <label className="labelWithColor"> SpotifyID: 
                        <input placeholder="Type Here.."type="text" />
                    </label>

                    <label  className="labelWithColor">How Would You Rate The Quality of the Spotify Playlist?
                        
                    <input placeholder="e.g. 5" type="text"/>
                     
                    </label>

                    <label className="labelWithColor">How Was Your Overall Experience? 
                        <textarea
                            placeholder="Type Here.."
                            rows = {5}
                            cols = {50}
                        ></textarea>
                    </label>

                    <label className="labelWithColor">Did You Encounter Any Delays While Using The Application? If Yes, At Which Point Did You Experience Them?
                        <textarea
                            placeholder="Type Here.."
                            rows = {5}
                            cols = {50}
                        ></textarea>
                    </label>

                    <label className="labelWithColor">Are There Additional Features You Would Like To See?
                        <textarea
                            placeholder="Type Here.."
                            rows = {5}
                            cols = {50}
                        ></textarea>
                    </label>

                    <button type="submit" className='submit-button'>Submit</button>

                </form>
             
             </div>  
            )
        }
    
export default Form;


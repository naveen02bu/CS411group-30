import requests
import urllib.parse
import json
import os
import mysql.connector


from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
from flask import Flask, redirect, request, jsonify, session
from flask_cors import CORS, cross_origin



app = Flask(__name__)
CORS(app)

# Load environment variables
load_dotenv()

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Nellie724!',
    'database': 'Bookify'
}

# Secret key for session
app.secret_key = os.getenv('SECRET_KEY')

# Spotify credentials
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

# Spotify endpoints
REDIRECT_URI = 'http://localhost:5000/callback'
AUTH_URL = 'https://accounts.spotify.com/authorize' 
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/'

new_playlist_id = ''
# Base endpoint
@app.route('/') 
def index():
    return "Welcome to my app <a href='/login'>Login with spotify</a>"

# Login endpoint: redirect to spotify login
@app.route('/login')
def login(): 
    # User permissions
    scope = 'playlist-modify-public playlist-read-private'
    # Parameters to pass to auth url
    params = {
        'client_id': CLIENT_ID, 
        'response_type': 'code', 
        'scope': scope, 
        'redirect_uri': REDIRECT_URI, 
        'show_dialog': True
    }
    # Create auth url for frontend to call
    response_data = {
        'auth_url': f"{AUTH_URL}?{urllib.parse.urlencode(params)}" 
    } 
    return jsonify(response_data)


""" 
Callback for after the user logins.
Two scenarios: unsuccessful and successful login
"""
@app.route('/callback') 
def callback(): 
    # Unsuccessful
    # If there is an error in the request, return error message
    if 'error' in request.args:
        print("Error:", request.args['error'])
        return redirect('http://localhost:3000')
    # Successful 
    # If code is in request, send a request to token url in order to store token info in a session
    if 'code' in request.args: 
        req_body = { 
            'code': request.args['code'], 
            'grant_type': 'authorization_code', 
            'redirect_uri': REDIRECT_URI, 
            'client_id': CLIENT_ID, 
            'client_secret': CLIENT_SECRET
        }

        response = requests.post(TOKEN_URL, data=req_body)
        token_info = response.json() 

        # Used to make requests to spotify api
        session['access_token'] = token_info['access_token']
        # Used to refresh access token
        session['refresh_token'] = token_info['refresh_token']
        # When the token expires
        session['expires_at'] = datetime.now().timestamp() + token_info['expires_in']

        # Redirect to endpoint
        print("Session data before redirection:", session)
        return redirect('http://localhost:3000/book')

# Endpoint to get user's playlists
@app.route('/playlists') 
@cross_origin(supports_credentials=True)
def get_playlist(): 
    if 'access_token' not in session: 
        return redirect('/login') 
    
    if datetime.now().timestamp() > session['expires_at']: 
        return redirect('/refresh-token')
    
    headers = { 
        'Authorization': f"Bearer {session['access_token']}"
    }
   
    # Get songs of most recent playlist
    response = requests.get(API_BASE_URL + f"playlists/{new_playlist_id}", headers=headers)
    return jsonify(response.json())

# Endpoint for when token needs to be refreshed
@app.route('/refresh-token')
def refresh_token(): 
    if 'refresh_token' not in session: 
        return redirect('/login') 
    
    # Make sure token is expired
    if datetime.now().timestamp() > session['expires_at']: 
        req_body = { 
            'grant_type': 'refresh_token', 
            'refresh_token': session['refresh_token'], 
            'client_id': CLIENT_ID, 
            'client_secret': CLIENT_SECRET
        }
        # Get new token
        response = requests.post(TOKEN_URL, data=req_body) 
        new_token_info = response.json() 

        # Change info in session
        session['access_token'] = new_token_info['access_token']
        session['expires_at'] = datetime.now().timestamp() + new_token_info['expires_in']

        return redirect('/playlists')
    
# Endpoint to create a playlist
@app.route('/create-playlist', methods=['POST']) 
@cross_origin(supports_credentials=True)
def create_playlist(): 
    data = request.json 
    title = data['title']
    author = data['author'] 
 
   
    # Use OpenAI 
    # Define the user message
    book_input = f"based on the synopsis, genre, setting, language, and vibe of the book, Please provide a filled-out JSON file in this format {{\n  \"playlist_name\": \"\",\n  \"playlist_description\": \"\",\n  \"playlist_songs\": [\"\"]\n}}\nWith 10 songs from the last 50 years that fit the vibe of the book/movie \"{title}\" by {author} for the spotify api. The songs must be in this format: 'Artist - Song name' where 'Artist' and 'Song name' are replaced with the actual artist and song name. There must be no duplicate songs. Do not respond with anything other than the JSON file. If you can include songs from the soundtrack. The songs should be relevant to the intended audience, setting of book, etc.,. Do not respond with anything other than the JSON file."
    user_message = {"role": "user", "content": book_input}


    os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
    client = OpenAI()
    
    print('Creating response...') 
    
    # Create a chat completion request
    completion = client.chat.completions.create(
    model='gpt-3.5-turbo',
    messages=[user_message],
    )


    # Extract and parse the assistant's reply as JSON
    completion_message = completion.choices[0].message.content
    playlist_info = json.loads(completion_message)

    # Create a new playlist
    playlist_name = playlist_info['playlist_name']
    playlist_description = playlist_info['playlist_description']

    # Create a new playlist
    headers = {
        'Authorization': f"Bearer {session['access_token']}",
        'Content-Type': 'application/json'
    }

    playlist_data = {
        'name': playlist_name,
        'description': playlist_description,
        'public': True
    }

    print(completion_message)
    print('Creating playlist...')

    # Create a list of songs to add to the playlist
    list_of_songs = []
    for song in playlist_info['playlist_songs']:
        result = requests.get(API_BASE_URL + f'search?q={song}&type=track', headers=headers).json()
        if result['tracks']['items']:
            list_of_songs.append(result['tracks']['items'][0]['uri'])

    # Make the request to create the playlist
    response = requests.post(API_BASE_URL + 'me/playlists', headers=headers, json=playlist_data)

    # Add songs to the playlist 
    if list_of_songs:
        playlist_id = response.json()['id']
        requests.post(API_BASE_URL + f'playlists/{playlist_id}/tracks', headers=headers, json={'uris': list_of_songs})

    if response.status_code == 201:
        playlist_data = response.json()
        # Extract relevant information from the playlist_data if needed    
        global new_playlist_id
        new_playlist_id = playlist_data.get('id')    
        print("Playlist created:", playlist_data)
        return jsonify({"success": True, "playlist_id": playlist_data.get('id')})
    else:
        print("Failed")
        return jsonify({"error": "Failed to create playlist", "status_code": response.status_code})

@cross_origin(supports_credentials=True)
@app.route('/save-feedback', methods=['POST'])

def save_feedback():
    db_connection = None
    db_cursor = None

    response = jsonify({"success": True})
    response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
    response.headers.add("Access-Control-Allow-Credentials", "true")

    try:
        # Establish a database connection
        db_connection = mysql.connector.connect(**db_config)
        db_cursor = db_connection.cursor()
        

        # Get feedback data from the request
        feedback_data = request.json

        # Insert feedback data into the database
        insert_query = "INSERT INTO feedback (spotifyID, rateQuality, overallExperience, delay, features) VALUES (%s, %s, %s, %s, %s)"
        insert_values = (
            feedback_data.get('spotifyID'),
            feedback_data.get('rateQuality'),
            feedback_data.get('overallExperience'),
            feedback_data.get('delay'),
            feedback_data.get('features')
        )
        db_cursor.execute(insert_query, insert_values)

        # Commit the changes
        db_connection.commit()

        print("Feedback data saved to the database.")
        return jsonify({"success": True})

    except Exception as e:
        print("Error saving feedback data to the database:", e)
        # Rollback the changes in case of an error
        db_connection.rollback()
        return jsonify({"error": "Failed to save feedback data to the database"})

    finally:
        # Close the database connection and cursor
        if db_cursor:
            db_cursor.close()
        if db_connection:
            db_connection.close()
    return response  
# Run server when you run code
if __name__ == '__main__': 
    app.run(host='0.0.0.0', debug=True)
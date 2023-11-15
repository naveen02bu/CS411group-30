import requests
import urllib.parse

from datetime import datetime
from flask import Flask, redirect, request, jsonify, session
from flask_cors import CORS, cross_origin


app = Flask(__name__)
CORS(app)

app.secret_key = '35252352-3242324'

CLIENT_ID = '125b735b568642cebd8bf395b25d7074' 
CLIENT_SECRET = 'f155917a69b9418eabd4fb654e4388b9' 
REDIRECT_URI = 'http://localhost:5000/callback'

AUTH_URL = 'https://accounts.spotify.com/authorize' 
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/'

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
        return jsonify({"error": request.args['error']})
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
   
    response = requests.get(API_BASE_URL + 'me/playlists', headers=headers)
    playlists = response.json()
    return jsonify(playlists)

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

    # Create a new playlist
    headers = {
        'Authorization': f"Bearer {session['access_token']}",
        'Content-Type': 'application/json'
    }

    playlist_data = {
        'name': title,
        'description': author,
        'public': True
    }

    # Make the request to create the playlist
    response = requests.post(API_BASE_URL + 'me/playlists', headers=headers, json=playlist_data)

    if response.status_code == 201:
        playlist_data = response.json()
        # Extract relevant information from the playlist_data if needed
        print("Playlist created:", playlist_data)
        return jsonify({"success": True, "playlist_id": playlist_data.get('id')})
    else:
        print("Failed")
        return jsonify({"error": "Failed to create playlist", "status_code": response.status_code})

# Run server when you run code
if __name__ == '__main__': 
    app.run(host='0.0.0.0', debug=True)
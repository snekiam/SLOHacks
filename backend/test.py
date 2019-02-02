from flask import Flask
from flask import jsonify

import configparser
import spotipy
import spotipy.oauth2 as oauth2
import spotipy.util as util
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/spotify-login')
def login():
    config = configparser.ConfigParser()
    config.read('config.cfg')
    client_id = config.get('SPOTIFY', 'CLIENT_ID')
    client_secret = config.get('SPOTIFY', 'CLIENT_SECRET')
    auth = oauth2.SpotifyClientCredentials(
        client_id=client_id,
        client_secret=client_secret
    )
    token = auth.get_access_token()
    spotify = spotipy.Spotify(auth=token)
    results = spotify.search(q='artist:' + "Muse", type='artist')
    results_json = jsonify(results)
    print(results_json)
    return jsonify(results)
    # return 
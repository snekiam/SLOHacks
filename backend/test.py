from flask import Flask
from flask import jsonify
from flask import request
from flask import redirect

import requests
import base64
import urllib

import configparser
import spotipy
import spotipy.oauth2 as oauth2
import spotipy.util as util
app = Flask(__name__)

# config with secrets and IDs
config = configparser.ConfigParser()
config.read('config.cfg')
client_id = config.get('SPOTIFY', 'CLIENT_ID')
redirect_uri = config.get('SPOTIFY', 'REDIRECT_URL')
client_secret = config.get('SPOTIFY', 'CLIENT_SECRET')
sp_oauth = oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri)

@app.route('/login')
def hello_world():

    scope = 'playlist-modify-public user-library-read'
    auth_query_parameters = {
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": scope,
        "client_id": client_id
    }
    url_args = "&".join(["{}={}".format(key,urllib.quote(val)) for key,val in auth_query_parameters.iteritems()])
    auth_url = "{}/?{}".format("https://accounts.spotify.com/authorize", url_args)
    return redirect(auth_url)

@app.route('/spotify-login/')
def handle_callback():
    code = request.args['code']
    token = sp_oauth.get_access_token(code)
    print(token)
    spotify = spotipy.Spotify(auth=token['access_token'])
    results = spotify.audio_features(tracks=['57lCa95tmjJ8EYdNTex8Kk'])
    results_json = jsonify(results)
    print(results_json)
    return jsonify(results)

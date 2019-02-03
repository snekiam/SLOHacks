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

    scope = 'playlist-modify-public user-library-read user-top-read'
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
    spotify = spotipy.Spotify(auth=token['access_token'])
    # return(jsonify(spotify.search(q='genre:pop', market='US', limit=50)['tracks']['items'][0]['id']))
    top_songs_audio_features = get_top_song_attributes(spotify)
    # spotify.user_playlist_create(sp_oauth)
    return top_songs_audio_features

def get_top_song_attributes(spotify):
    audio_features = []
    # get the user's current top 99 songs (the max spotify will let you)
    track_ids = [song['id'] for song in spotify.current_user_top_tracks(limit=50, offset=0)['items']]
    track_ids.extend([song['id'] for song in spotify.current_user_top_tracks(limit=50, offset=49)['items']])
    audio_features = spotify.audio_features(track_ids)
    return(jsonify(audio_features))

def get_genre_attributes(spotify):
    audio_features = []
    # get the audio features for the top 1,000 songs in a genre
    # this will take several seconds to run
    # for i in range(0, 20):
    for i in range(0, 20):
        track_ids = [song['id'] for song in spotify.search(q='genre:rap', market='US', limit=50, offset=50*i)['tracks']['items']]
        audio_features.extend(spotify.audio_features(track_ids))
    return(jsonify(audio_features))


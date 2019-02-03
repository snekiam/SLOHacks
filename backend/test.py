from flask import Flask
from flask import jsonify
from flask import request
from flask import redirect

import requests
import urllib

import configparser
import spotipy
import spotipy.oauth2 as oauth2
import spotipy.util as util

from knearest import k_nearest

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
    scope = 'playlist-modify-public playlist-modify-private user-library-read user-top-read'
    auth_query_parameters = {
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": scope,
        "client_id": client_id,
        "state": "Rock"
    }
    url_args = "&".join(["{}={}".format(key,urllib.parse.quote(val)) for (key,val) in auth_query_parameters.items()])
    auth_url = "{}/?{}".format("https://accounts.spotify.com/authorize", url_args)
    return redirect(auth_url)

@app.route('/spotify-login/')
def handle_callback():
    genre = request.args['state']
    code = request.args['code']
    token = sp_oauth.get_access_token(code)
    spotify = spotipy.Spotify(auth=token['access_token'])
    top_songs_audio_features = get_top_song_attributes(spotify)
    genre_audio_features = get_genre_attributes(spotify)
    track_ids = k_nearest(top_songs_audio_features, genre_audio_features)[0:9]
    playlist_id = spotify.user_playlist_create(spotify.me()['id'], 'Statify Generated Playlist with Genre '+ genre)['id']
    spotify.user_playlist_add_tracks(spotify.me()['id'], playlist_id, track_ids)

def get_top_song_attributes(spotify):
    audio_features = []
    # get the user's current top 99 songs (the max spotify will let you)
    track_ids = [song['id'] for song in spotify.current_user_top_tracks(limit=50, offset=0, time_range="long_term")['items']]
    track_ids.extend([song['id'] for song in spotify.current_user_top_tracks(limit=50, offset=49, time_range="long_term")['items']])
    audio_features = spotify.audio_features(track_ids)
    return(jsonify(audio_features))

def get_genre_attributes(spotify):
    audio_features = []
    # get the audio features for the top 1,000 songs in a genre
    # this will take several seconds to run
    # for i in range(0, 20):
    for i in range(0, 20):
        track_ids = [song['id'] for song in spotify.search(q='genre:rock', market='US', limit=50, offset=50*i)['tracks']['items']]
        audio_features.extend(spotify.audio_features(track_ids))
    return(jsonify(audio_features))


import os
client_id = os.environ['SPOTIFY_CLIENT_ID']
client_secret = os.environ['SPOTIFY_CLIENT_SECRET']
spotify_auth_url = 'https://accounts.spotify.com/authorize'
spotify_api_url = 'https://api.spotify.com/v1'
spotify_token_url = 'https://accounts.spotify.com/api/token'
discogs_token = os.environ['DISCOGS_TOKEN']
discogs_api_url = 'https://api.discogs.com'
redirect_uri = 'https://final-oi7qpq2pta-uw.a.run.app/spotify_results'
#redirect_uri = 'http://127.0.0.1:8000/spotify_results'
scope = "user-read-private user-read-playback-state user-modify-playback-state user-library-read user-top-read"

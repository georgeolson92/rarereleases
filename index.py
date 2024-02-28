from flask import render_template
from flask.views import MethodView
import urllib
from urllib.parse import quote 
from api_config import client_id, spotify_auth_url, spotify_api_url, redirect_uri


auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": redirect_uri,
    "scope": "user-read-private user-read-playback-state user-modify-playback-state user-library-read user-top-read",
    "client_id": client_id
}

class Index(MethodView):
    def get(self):
    	url_args = "&".join(["{}={}".format(key,urllib.parse.quote(val)) for key, val in auth_query_parameters.items()])
    	print(url_args)
    	auth_url = "{}/?{}".format(spotify_auth_url, url_args)
    	return render_template('index.html', url=auth_url)


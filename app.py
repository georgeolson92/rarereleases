import flask
import os
from index import Index
from spotify_results import Spotify_Results

app = flask.Flask(__name__)       # our Flask app

app.add_url_rule('/',
                 view_func=Index.as_view('index'),
                 methods=["GET"])

app.add_url_rule('/spotify_results',
                 view_func=Spotify_Results.as_view('spotify_results'),
                 methods=["GET"])
                 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

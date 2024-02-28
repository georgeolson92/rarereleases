from flask import Flask, redirect, render_template, request
from flask.views import MethodView
import urllib
from urllib.parse import quote 
import base64
import json
import requests
from api_config import client_secret, client_id, spotify_auth_url, spotify_api_url, spotify_token_url, discogs_token, discogs_api_url, redirect_uri, scope

auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": redirect_uri,
    "scope": scope,
    "client_id": client_id
}

class Spotify_Results(MethodView):
    def get(self):
    	# Check if auth_token exists in URL
    	auth_token = request.args['code']
    	if not auth_token:
    		return redirect('/')
    	
    	code_payload = {
        	"grant_type": "authorization_code",
        	"code": str(auth_token),
        	"redirect_uri": redirect_uri
    	}
    	
    	# Request token from Spotify
    	base64encoded = base64.b64encode("{}:{}".format(client_id, client_secret).encode())
    	headers = {"Authorization": "Basic {}".format(base64encoded.decode())}
    	post_request = requests.post(spotify_token_url, data=code_payload, headers=headers)
    
    	response_data = json.loads(post_request.text)
    	if post_request.status_code != 200:
    		return redirect('/')
    	access_token = response_data["access_token"]
    	
    	refresh_token = response_data["refresh_token"]
    	token_type = response_data["token_type"]
    	expires_in = response_data["expires_in"]
    
    	authorization_header = {"Authorization":"Bearer {}".format(access_token)}
    	
    	# Get profile data from Spotify
    	user_profile_api_endpoint = "{}/me".format(spotify_api_url)
    	profile_response = requests.get(user_profile_api_endpoint, headers=authorization_header)
    	profile_data = json.loads(profile_response.text)
    	
    	user_profile = {
    		"name": profile_data['display_name'],
    		"id": profile_data['id'],
    		"profile_url": profile_data['external_urls']['spotify']
    	}
    	
    	print("got user profile")
    	# Get top artists from Spotify
    	user_top_artists_api_endpoint = "{}/me/top/artists?time_range=short_term&limit=3".format(spotify_api_url)

    	top_artists_response = requests.get(user_top_artists_api_endpoint, headers=authorization_header)
    	top_artists_data = json.loads(top_artists_response.text)
    	print("got top artists")
    	# Add top artist to array
    	top_list = [];
    	g = 0
    	count = len(top_artists_data['items'])
    	
    	if count == 0:
    		return render_template('spotify_results.html', user_profile=user_profile)
    		
    	while ( g < count):
    		top_list.append({
    			"name": top_artists_data['items'][g]['name'],
    			"img": top_artists_data['items'][g]['images'][0]['url']
    		})
    		g += 1
    		
    	# Get Artist's albums on spotify
    	artists_albums_api_endpoint = "{}/artists/{}/albums?include_groups=album".format(spotify_api_url,top_artists_data['items'][0]['id'])
    	
    	artists_albums_response = requests.get(artists_albums_api_endpoint, headers=authorization_header)
    	artists_albums_data = json.loads(artists_albums_response.text)
    	
    	a = 0;
    	count = len(artists_albums_data["items"])
    	spotify_releases = []
    	while ( a < count):
    		spotify_releases.append(str(artists_albums_data["items"][a]["name"]).strip().lower())
    		a += 1
    	
    	# Initialize Discogs artist releases array
    	discogs_releases = [[],[],[]]
    	
    	# Get rare artist releases
    	b = 0
    	while (b < 3):
    		# Get artist ID from Discogs 
	    	discogs_api_endpoint = "{}/database/search?q={}&type=artist&token={}".format(discogs_api_url,top_artists_data['items'][b]['name'],discogs_token)
	    	discogs_response = requests.get(discogs_api_endpoint)
	    	discogs_data = json.loads(discogs_response.text)
	    	
	    	discogs_artist_id = discogs_data["results"][0]["id"]
	    	
	    	# Get releases from Discogs 
	    	discogs_artists_api_endpoint = "{}/artists/{}/releases?token={}".format(discogs_api_url,discogs_artist_id,discogs_token)
	    	discogs_artists_response = requests.get(discogs_artists_api_endpoint)
	    	discogs_artists_data = json.loads(discogs_artists_response.text)
	    	
	    	# Add artist's releases to array
	    	x = 0;
	    	count = len(discogs_artists_data["releases"])
	    	
	    	while ( x < count):
	    		if str(discogs_artists_data["releases"][x]["title"]).strip().lower() not in spotify_releases:
	    			if("format" in discogs_artists_data["releases"][x] and "Single" not in discogs_artists_data["releases"][x]["format"] and "Comp" not in discogs_artists_data["releases"][x]["format"]):
	    				release_year = ""
	    				if ("year" in discogs_artists_data["releases"][x]):
	    					release_year = discogs_artists_data["releases"][x]["year"]
	    				else:
	    					release_year = "N/A"
			    		discogs_releases[b].append({
			    			"title": str(discogs_artists_data["releases"][x]["title"]).strip(),
			    			"thumb": discogs_artists_data["releases"][x]["thumb"],
			    			"id": str(discogs_artists_data["releases"][x]["id"]),
			    			"format": ''.join(discogs_artists_data["releases"][x]["format"]),
			    			"year": release_year
			    		})
	    		x += 1
	    	
	    	b += 1
    	
    	return render_template('spotify_results.html', user_profile=user_profile, top_list=top_list, album_list=discogs_releases)


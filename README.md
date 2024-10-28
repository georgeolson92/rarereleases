# Rare Releases


## First step of configuring app:
1. Register or log in to Discogs to get an API token here: https://www.discogs.com/settings/developers
2. Register or log into Spotify and visit the devloper portal to create an application: https://developer.spotify.com/dashboard/
3. Save your client ID & client secret values for the next steps

## When running locally:

1. 	$ virtualenv -p python3 env
2. 	$ source env/bin/activate
3. 	$ pip install -r requirements.txt
4. 	$ export SPOTIFY_CLIENT_ID=(value)
5. 	$ export SPOTIFY_CLIENT_SECRET=(value)
6. 	$ export DISCOGS_TOKEN=(value)
7. 	$ python app.py

## Manually Deploying in Google Cloud:

1. Set up service account in Google with 'Cloud Run Developer' permissions
1. clone to your GCloud Shell
2. 	$ gcloud builds submit --timeout=900 --tag gcr.io/${GOOGLE_CLOUD_PROJECT}/final
3. 	 gcloud run deploy final --image gcr.io/${GOOGLE_CLOUD_PROJECT}/final --service-account (accountname)@${GOOGLE_CLOUD_PROJECT}.iam.gserviceaccount.com --set-env-vars SPOTIFY_CLIENT_ID=(value),SPOTIFY_CLIENT_SECRET=(value),DISCOGS_TOKEN=(value)

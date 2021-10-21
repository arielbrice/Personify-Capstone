import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import flask

with open("secret.txt") as file:
        clientid = file.readline
        clientsecret = file.readline
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=clientid,
                                                           client_secret=clientsecret))
# Limit of the number in a search is 50, You can not search for more items than 50 at a time
results = sp.search(q='Sagittarius', limit=50)
for idx, track in enumerate(results['tracks']['items']):
    print(idx, track['name'])

print("Hello World")
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import flask

with open("secret.txt") as file:
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=file.readline(), client_secret=file.readline()))
# Limit of the number in a search is 50, You can not search for more items than 50 at a time
#results = sp.search(q='Cancer', limit=50)
#for idx, track in enumerate(results['tracks']['items']):
#    print("Cancer:",idx, track['name'])

print("Hello World")

with open("keywords.txt") as keywordFile:
    for keyword in keywordFile:
        results = sp.search(q = keyword, limit=50)
        print("\n",keyword)
        for idx, track in enumerate(results['tracks']['items']):
            print(idx, track['name'])
<<<<<<< HEAD
=======
    keywordFile.close()
>>>>>>> a51b8975f12eda98032fa5e8d470a5c2979d5963

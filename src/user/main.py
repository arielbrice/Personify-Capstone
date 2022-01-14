import spotipy
from spotipy import client
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import flask
import os;


with open("secret.txt") as file:
   # print(file.readline(), file.readline())
   clientid = file.readline()
   clientsecret = file.readline().strip()
   print(clientid+clientsecret)
   sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=clientid, client_secret=clientsecret))
# Limit of the number in a search is 50, You can not search for more items than 50 at a time
#results = sp.search(q='Cancer', limit=50)
#for idx, track in enumerate(results['tracks']['items']):
#    print("Cancer:",idx, track['name'])
#print(sp.current_user)
print(sp.track("https://open.spotify.com/track/1oew3nFNY3vMacJAsvry0S?si=28a86dcb03774c3c"))
print(sp.artist("https://open.spotify.com/artist/6vWDO969PvNqNYHIOW5v0m?si=AWecjQtFSxK7gHyyOnDFTw"))
#print(sp.user("dakotajamesspears"))


with open("keywords.txt") as keywordFile:
    for keyword in keywordFile:
        results = sp.search(q = keyword, limit=10)
        print("\n",keyword)
        for idx, track in enumerate(results['tracks']['items']):
            print(idx, track['name'])

            
def test():
    return "hello"
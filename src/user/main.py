import spotipy
from spotipy import client
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import flask
import os


with open("secret.txt") as file:
   clientid = file.readline()
   clientsecret = file.readline().strip()
   print(clientid+clientsecret)
   sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=clientid, client_secret=clientsecret))
   sp.me()


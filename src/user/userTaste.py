import spotipy
import json
from spotipy.oauth2 import SpotifyOAuth

#'short_term' = (4 Weeks)
#'medium_term' = (6 Months)
#'long_term' = (1 Year)

'''
Return user's top tracks from their authorized Spotify account through spotipy
'''
def topTracks(sp):
    tracks = sp.current_user_top_tracks(limit=50,  time_range= 'short_term')
    track = []
    for item in tracks['items']:
        track += (item['id']) + " \n"
    topT = listToString(track)
    return topT

'''
Return user's top artists from their authorized Spotify account through spotipy
'''
def topArtists(sp):
    artists = sp.current_user_top_artists(limit=50,  time_range= 'short_term')
    artist = []
    for item in artists['items']:
        artist +=  item['name'] + " "   
    topA = listToString(artist)
    print("top: ", topA)
    return topA

'''
Prints a user's top artists from their authorized Spotify account through spotipy
'''
def printtopA(artists):
    artist = []
    for item in artists['items']:
        artist +=  (item['name']) + " "
    listToStr = listToString(artist)
    print("top: ", listToStr)
    return listToStr

'''
Converts Python list to String
'''
def listToString(s): 
    str1 = "" 
    for ele in s: 
        str1 += ele  
    return str1 

import spotipy
import json
from spotipy.oauth2 import SpotifyOAuth

#'short_term' = (4 Weeks)
#'medium_term' = (6 Months)
#'long_term' = (1 Year)

def topTracks(sp):
    tracks = sp.current_user_top_tracks(limit=50,  time_range= 'short_term')
    track = []
    for item in tracks['items']:
        track += (item['name']) + " "
    topT = listToString(track)
    return topT
    #print(tracks)

def topArtists(sp):
    artists = sp.current_user_top_artists(limit=50,  time_range= 'short_term')
    artist = []
    for item in artists['items']:
        #print (item['name'], item['genres'])
        artist +=  item['name'] + " "   
    topA = listToString(artist)
    print("top: ", topA)
    return topA

def printtopA(artists):
    artist = []
    for item in artists['items']:
        #print (item['name'], item['genres'])
        artist +=  (item['name']) + " "
    listToStr = listToString(artist)
    print("top: ", listToStr)
    return listToStr


def listToString(s): 
    
    # initialize an empty string
    str1 = "" 
    
    # traverse in the string  
    for ele in s: 
        str1 += ele  
    
    # return string  
    return str1 

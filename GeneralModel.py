import spotipy
import json
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials

'''
authorize use of spotify client
'''
def authorizeFromSecret():
    with open("secret.txt", encoding="UTF-8") as file:
        clientid = file.readline().strip()
        clientsecret = file.readline().strip()
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=clientid, client_secret=clientsecret))
    return sp

'''
read ids from txt file, store in list
returns list of ids
'''
def storeIDs():
    idList = []
    with open("HannahTopTrackIDs.txt", encoding="UTF-8") as songFile:
        for line in songFile:
            idList.append(line.strip())
    return idList

'''
use spotipy to retrieve audio features for all songs
writes info to csv file
'''
def getAudioAnalysis():
    sp = authorizeFromSecret()
    IDs = storeIDs()
    allfeatures = sp.audio_features(IDs)
    features = allfeatures[0].keys() # first row of csv. attr names

    with open("gen-mod-features.csv", 'w', encoding="UTF-8") as output:
        for feat in features:
            output.write(feat + ",")
        output.write("\n")
        for song in allfeatures:
            for value in song:
                output.write(str(song[value]) + ",")
            output.write("\n")


getAudioAnalysis()
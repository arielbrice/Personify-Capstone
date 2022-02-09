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
    with open("src/data/HannahTopTrackIDs.txt", encoding="UTF-8") as songFile:
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

    with open("indv-mod-aquarius-features-greta.csv", 'w', encoding="UTF-8") as output:
        for feat in features:
            output.write(feat + ",")
        output.write("\n")
        for song in allfeatures:
            for value in song:
                output.write(str(song[value]) + ",")
            output.write("\n")

    with open("indv-mod-aquarius-features-greta.csv", encoding="UTF-8") as featfile:
        atts = featfile.readline().split(",")
        indvSongsAndFeatures = []

        for line in featfile:
            allAtts = line.split(",")
            song = []
            for vals in allAtts:
                if is_number(vals) or allAtts.index(vals) == 12:
                    if is_number(vals):
                        song.append(float(vals))
                    else:
                        song.append(vals)
            indvSongsAndFeatures.append(song)

    with open("src/data/gen-mod-features.csv", encoding="UTF-8") as featfile:
        atts = featfile.readline().split(",")
        genSongsAndFeatures = []

        for line in featfile:
            allAtts = line.split(",")
            song = []
            for vals in allAtts:
                if is_number(vals) or allAtts.index(vals) == 12:
                    if is_number(vals):
                        song.append(float(vals))
                    else:
                        song.append(vals)
            genSongsAndFeatures.append(song)
    return indvSongsAndFeatures, genSongsAndFeatures

def compareFeatures():
    indv, gen = getAudioAnalysis()
    keep = set()
    discard = set()

    '''
    danceability = 0.1069414125
    energy = 0.2082973042
    key = 3.0530012
    loudness = 3.103078809
    mode = 0.4903143515
    speechiness = 0.0319907012
    acousticness = 0.3250085831
    instrumentalness = 0.08267264162
    liveness = 0.1770045646
    valence = 0.1834915416
    tempo = 34.11046634
    duration = 37852.24111
    timeSignature = 0.5955618167
    '''

    stdevs = [0.1069414125,0.2082973042,3.0530012,3.103078809,0.4903143515,0.0319907012,0.3250085831,0.08267264162,0.1770045646,0.1834915416,34.11046634,'na',37852.24111,0.5955618167]


    for isong in indv: # each song in greta's (50)
        for ival in isong:
            for gsong in gen: # each song in cass' (5)
                for index, val in enumerate(gsong): # each value for the song features (14 x 50)
                    for isong in indv:
                       # print(val, isong[index])
                        if(index != 11):
                            diff = abs(float(val) - float(isong[index]))
                           # print(diff)
                            if diff <= stdevs[index]*6:
                                keep.add(gsong[11])
                            else:
                                discard.add(gsong[11])

    print(len(keep))
    print(len(discard))

    for song in discard:
        if song in keep:
            keep.remove(song)
    if(len(keep) == 0):
        return discard

    return keep

# playlist to keep in database as list(?)
def showSongNames(sp):
    songs = compareFeatures()
    print("length: ",len(songs))
    sp = authorizeFromSecret()
    playlist = sp.user_playlist_create("hannahsiitia", "Test Personify Recs", public = False, description= "This playlist was made using your Zodiac sign and machine learning!")
    playlist_id = playlist["id"]
    sp.playlist_add_items(playlist_id, songs, position=None)

    return playlist_id




def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

getAudioAnalysis()
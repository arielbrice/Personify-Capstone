import spotipy
import spotipy.util as util
from spotipy import SpotifyClientCredentials, SpotifyOAuth

from pymongo import MongoClient
import mongoengine

import pandas as pd

from matplotlib import pyplot as plt
import mpl_toolkits
from mpl_toolkits.mplot3d import Axes3D

#import sklearn
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler

import numpy as np

scaler = MinMaxScaler()

# Establish DB Connection
with open("dbconnection.txt") as file:
    connectionString = file.readline().strip()

client = MongoClient(connectionString)
db = client['Personify']
trackCollection = db['Tracks']
mongoengine.register_connection(alias='core', name='personify')
mongoengine.connect(alias='pers-db', host=connectionString)

def prepareData():
    data = pd.DataFrame(list(trackCollection.find()))

    x = data.iloc[:,4]
    for item in range(len(x)):
        x[item].pop(0)
        x[item].pop(0)
        x[item].pop(0)
        x[item] = np.asarray(x[item])

    x = pd.DataFrame(data['analysis'].to_list(), columns=['acousticness', 'danceability','energy','instrumentalness','key','liveness','loudness','mode','speechiness'])
    #print(x.head)
    x.drop(['mode'], axis=1)
    x.drop(['key'], axis=1)
    data = pd.concat([data, x], axis=1)
    scaled = scaler.fit_transform(x)
    return data, scaled

#TODO: save into a model
def trainAndPredict():
    data, scaled = prepareData()
    kmeans = KMeans(n_clusters = 8, init = 'k-means++', max_iter = 1000, n_init = 50, random_state = 0)
    y = kmeans.fit_predict(scaled)

    kmeans_df = pd.DataFrame(data=y, dtype=float)
    kmeans_df.columns = ['k_cluster']

    data = pd.concat([data, kmeans_df], axis=1)
    data.drop(['analysis'], axis=1)
    data.to_csv('updated-songs-w-clusters.csv')
    return data

def modeRecs(username):
    data = trainAndPredict()
    songs = collectUserSongs(username)
    newlyAddedIDs = list(data[data['song_id'].isin(songs)]['song_id'])
    newlyAddedArtists = list(data[data['song_id'].isin(songs)]['artist'])

    mode_cluster = list(data[data['song_id'].isin(newlyAddedIDs)]['k_cluster'].value_counts().index)[0]

    isolated_cluster = pd.DataFrame(data=data[data['k_cluster'] == mode_cluster])
    print(newlyAddedArtists)

    artistsInCommon = list(isolated_cluster[isolated_cluster['artist'].isin(newlyAddedArtists) & ~(isolated_cluster['song_id'].isin(newlyAddedIDs))]['title'])

    if len(artistsInCommon) != 0:
        recs = isolated_cluster.sample(n=10)
        print (recs)
        print(recs['title'], recs['artist'])
        return recs

def euclidianRecs(username):
    data = trainAndPredict()
    songs = collectUserSongs(username)
    modeRecs(username)

def collectUserSongs(username):
    with open("secret.txt", encoding="UTF-8") as file:
        clientid = file.readline().strip()
        clientsecret = file.readline().strip()
    scope = 'user-library-read'
    #sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=clientid, client_secret=clientsecret, redirect_uri='http://localhost:5000/redirect', scope=scope, username="cassjhunt"))
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=clientid, client_secret=clientsecret, redirect_uri='http://localhost:5000/redirect', scope=scope, username=username))
    print(username)
    songs = []
    results = sp.current_user_saved_tracks()
    for item in results['items']:
        songs.append(item['track']['id'])
    return songs

print(modeRecs("cassjhunt"))
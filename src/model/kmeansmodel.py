import spotipy
import spotipy.util as util
from pymongo import MongoClient
import pandas as pd
import mongoengine

from matplotlib import pyplot as plt
import mpl_toolkits
from mpl_toolkits.mplot3d import Axes3D
import sklearn
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import pairwise_distances_argmin_min
from spotipy import SpotifyClientCredentials, SpotifyOAuth

#from database import mongo_setup

scaler = MinMaxScaler()

import numpy as np




'''
import pymongo
import pandas as pd
from pymongo import Connection
connection = Connection()
db = connection.database_name
input_data = db.collection_name
data = pd.DataFrame(list(input_data.find()))
'''


with open("../../dbconnection.txt") as file:
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
    print(x.head)
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

# euclidean distance for recommendations

# get reccomendations

#TODO: use to get the reccomended songs
def modeRecs(username):
    data = trainAndPredict()
    songs = collectUserSongs(username)
    newlyAddedIDs = list(data[data['song_id'].isin(songs)]['song_id'])
    newlyAddedArtists = list(data[data['song_id'].isin(songs)]['artist'])

    mode_cluster = list(data[data['song_id'].isin(newlyAddedIDs)]['k_cluster'].value_counts().index)[0]

    isolated_cluster = pd.DataFrame(data=data[data['k_cluster'] == mode_cluster])
    print(newlyAddedArtists)

    artistsInCommon = list(isolated_cluster[isolated_cluster['artist'].isin(newlyAddedArtists) & ~(isolated_cluster['song_id'].isin(newlyAddedIDs))]['title'])

    if len(artistsInCommon) == 0:
        recs = isolated_cluster.sample(n=10)
        print(recs['title'], recs['artist'])
        return recs
    


def euclidianRecs():
    data = trainAndPredict()
    songs = collectUserSongs()




def collectUserSongs(username):
    with open("../../secret.txt", encoding="UTF-8") as file:
        clientid = file.readline().strip()
        clientsecret = file.readline().strip()
    scope = 'user-library-read'
    #sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=clientid, client_secret=clientsecret, redirect_uri='http://localhost:5000/redirect', scope=scope, username="cassjhunt"))
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=clientid, client_secret=clientsecret, redirect_uri='http://localhost:5000/redirect', scope=scope, username=username))

    songs = []
    results = sp.current_user_saved_tracks()
    for item in results['items']:
        songs.append(item['track']['id'])
    return songs



euclidianRecs()

'''
print(scaled[y == 1,0], scaled[y == 1,1])
# visualizing clusters
fig, ax = plt.subplots(figsize=(10,8))
ax = fig.add_subplot(111, projection='3d')


#plt.scatter(scaled[y == 0,0],scaled[y == 0,1], s= 10, c= 'red', alpha=0.20, label= 'Cluster 0')
#plt.scatter(scaled[y == 1,0], scaled[y == 1,1], s= 10, c= 'blue',  alpha=0.20, label= 'Cluster 1')
#plt.scatter(scaled[y == 2,0], scaled[y == 2,1], s= 10, c= 'green',  alpha=0.20, label= 'Cluster 2')
#plt.scatter(scaled[y == 3,0], scaled[y == 3,1], s= 10, c= 'cyan',  alpha=0.20, label= 'Cluster 3')
#plt.scatter(scaled[y == 4,0], scaled[y == 4,1], s= 10, c= 'yellow',  alpha=0.20, label= 'Cluster 4')
#plt.scatter(scaled[y == 5,0], scaled[y == 5,1], s= 10, c= 'orange',  alpha=0.20, label= 'Cluster 5')
#plt.scatter(scaled[y == 6,0], scaled[y == 6,1], s= 10, c= 'purple',  alpha=0.20, label= 'Cluster 6')
plt.scatter(scaled[y == 7,0], scaled[y == 7,1], s= 10, c= 'aquamarine',  alpha=0.20, label= 'Cluster 7')

# centroids
#plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:,1], s= 25, c= 'yellow',  alpha=0.5, label= 'Centroids')

plt.title('Cluster 7')
#plt.legend()
plt.savefig('clusters.png')
plt.show()


print("dance\n", data.groupby(['k_cluster']).danceability.mean().sort_values(ascending=False))
print("energy\n", data.groupby(['k_cluster']).energy.mean().sort_values(ascending=False))
print("instrulmentalness\n", data.groupby(['k_cluster']).instrumentalness.mean().sort_values(ascending=False))
print("key\n", data.groupby(['k_cluster']).key.mean().sort_values(ascending=False))
print("liveness\n", data.groupby(['k_cluster']).liveness.mean().sort_values(ascending=False))
print("loud\n",data.groupby(['k_cluster']).loudness.mean().sort_values(ascending=False))
print("mode\n",data.groupby(['k_cluster']).mode.mean().sort_values(ascending=False))
print("speech\n",data.groupby(['k_cluster']).speechiness.mean().sort_values(ascending=False))



sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=clientid, client_secret=clientsecret))

with open("../../secret.txt", encoding="UTF-8") as file:
    clientid = file.readline().strip()
    clientsecret = file.readline().strip()
scope = 'user-library-read'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=clientid, client_secret=clientsecret, redirect_uri='http://localhost:5000/redirect', scope=scope, username="hannahsiitia"))

songs = []
results = sp.current_user_saved_tracks()

stat_map = {}
stat_keys = ['title', 'artist', 'id', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'key', 'liveness',
             'loudness', 'mode', 'speechiness']
stat_map['title'] = []
stat_map['artist'] = []
for keys in stat_keys:
    stat_map[keys] = 0

for item in results['items']:
    title = item['track']['name']
    artist = item['track']['artists'][0]['name']
    songs.append(item['track']['id'])
    testing_billboard.newSongs(title, artist)
'''



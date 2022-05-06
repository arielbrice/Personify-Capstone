from matplotlib import pyplot as plt
from pymongo import MongoClient
import pandas as pd
import mongoengine
from sklearn import preprocessing
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler

import testing_billboard

import numpy as np

import os

homeDIR = os.path.expanduser('~')

DIRDB = homeDIR + "/.personify/dbconnection.txt"

PATHSEC = homeDIR + "/.personify/secret.txt"

with open("dbconnection.txt") as file:
    connectionString = file.readline().strip()

scaler = MinMaxScaler()
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
    visualize(scaled, y, data)
    return data

def modeRecs(username, sp):
    print("finding recs for", username)
    songs = collectUserSongs(username, sp)
    data = trainAndPredict()

    newlyAddedIDs = list(data[data['song_id'].isin(songs)]['song_id'])
    newlyAddedArtists = list(data[data['song_id'].isin(songs)]['artist'])

    print("cluster commonality:" ,list(data[data['song_id'].isin(newlyAddedIDs)]['k_cluster'].value_counts().index))

    mode_cluster = list(data[data['song_id'].isin(newlyAddedIDs)]['k_cluster'].value_counts().index)[0]

    print("most common cluster: ", mode_cluster)

    isolated_cluster = pd.DataFrame(data=data[data['k_cluster'] == mode_cluster])
    recs = isolated_cluster.sample(n=50)

    return recs

def collectUserSongs(username, sp):
    print("in cUS with", username)
    songs = []
    results = sp.current_user_saved_tracks()

    for item in results['items']:
        title = item['track']['name']
        artist = item['track']['artists'][0]['name']
        print(title, artist)
        check = sp.search(q="{} {}".format(title, artist, limit=1))
        tr = check['tracks']['items']
        songs.append(item['track']['id'])

        testing_billboard.get_spotify_stats(title, artist, tr)
    print("songs", songs)
    return songs

def visualize(scaled, y, data):
    T = preprocessing.Normalizer().fit_transform(scaled)
    n_clusters = 8
    kmean_model = KMeans(n_clusters=n_clusters)
    kmean_model.fit(T)
    centroids, labels = kmean_model.cluster_centers_, kmean_model.labels_
    pca_model = PCA(n_components=2)
    pca_model.fit(T) # fit the model
    T = pca_model.transform(T) # transform the 'normalized model'\
    print(T)
    # transform the 'centroids of KMean'
    centroid_pca = pca_model.transform(centroids)
    # print(centroid_pca)
    # colors for plotting
    colors = ['blue', 'pink', 'green', 'purple', 'black', 'brown', 'teal', 'yellow']
    # assign a color to each features (note that we are using features as target)
    features_colors = [ colors[labels[i]] for i in range(len(T)) ]
    print(features_colors)
    plt.scatter(T[:, 0], T[:, 1], 10,
                c=features_colors, marker='o',
                alpha=0.2
            )
            
    # plot the PCA components
    plt.scatter(T[:, 0], T[:, 1],
                c=features_colors, marker='o',
                alpha=0.2
            )

    # plot the centroids
    '''
    plt.scatter(centroid_pca[:, 0], centroid_pca[:, 1],
                marker='x', s=100,
                linewidths=3, c=colors
            )
    '''
    # store the values of PCA component in variable: for easy writing
    xvector = pca_model.components_[0] * max(T[:,0])
    yvector = pca_model.components_[1] * max(T[:,1])
    columns = data.columns
    print(xvector)
    print(yvector)

    # plot the 'name of individual features' along with vector length
    #for i in range(len(columns)):
        # plot arrows
     #   plt.arrow(0, 0, xvector[i], yvector[i],
        #            color='b', width=0.0005,
         #           head_width=0.02, alpha=0.75
         #       )
        # plot name of features
        #plt.text(xvector[i], yvector[i], list(columns)[i], color='b', alpha=0.75)

    plt.show()

    '''
    data.to_csv("final-data-w-cluster.csv")
    print(scaled[y == 1,0], scaled[y == 1,1])
    # visualizing clusters
    fig, ax = plt.subplots(figsize=(10,8))
    #ax = fig.add_subplot(111)

    plt.xticks(np.arange(0,1,step=0.2))
    plt.yticks(np.arange(0,1,step=0.2))
    fig0 = plt.scatter(scaled[y == 0,0],scaled[y == 0,1], s= 10, c= 'red', alpha=0.20, label= 'Cluster 0')
    plt.figure()

    plt.xticks(np.arange(0, 1, step=0.2))
    plt.yticks(np.arange(0, 1, step=0.2))
    fig1 = plt.scatter(scaled[y == 1,0], scaled[y == 1,1], s= 10, c= 'blue',  alpha=0.20, label= 'Cluster 1')
    plt.figure()

    plt.xticks(np.arange(0, 1, step=0.2))
    plt.yticks(np.arange(0, 1, step=0.2))
    fig2 = plt.scatter(scaled[y == 2,0], scaled[y == 2,1], s= 10, c= 'green',  alpha=0.20, label= 'Cluster 2')
    plt.figure()

    plt.xticks(np.arange(0, 1, step=0.2))
    plt.yticks(np.arange(0, 1, step=0.2))
    fig3 = plt.scatter(scaled[y == 3,0], scaled[y == 3,1], s= 10, c= 'teal',  alpha=0.20, label= 'Cluster 3')
    plt.figure()

    plt.xticks(np.arange(0, 1, step=0.2))
    plt.yticks(np.arange(0, 1, step=0.2))
    fig4 = plt.scatter(scaled[y == 4,0], scaled[y == 4,1], s= 10, c= 'maroon',  alpha=0.20, label= 'Cluster 4')
    plt.figure()

    plt.xticks(np.arange(0, 1, step=0.2))
    plt.yticks(np.arange(0, 1, step=0.2))
    fig5 = plt.scatter(scaled[y == 5,0], scaled[y == 5,1], s= 10, c= 'darkorange',  alpha=0.20, label= 'Cluster 5')
    plt.figure()

    plt.xticks(np.arange(0, 1, step=0.2))
    plt.yticks(np.arange(0, 1, step=0.2))
    fig6 = plt.scatter(scaled[y == 6,0], scaled[y == 6,1], s= 10, c= 'purple',  alpha=0.20, label= 'Cluster 6')
    plt.figure()

    plt.xticks(np.arange(0, 1, step=0.2))
    plt.yticks(np.arange(0, 1, step=0.2))
    fig7 = plt.scatter(scaled[y == 7,0], scaled[y == 7,1], s= 10, c= 'magenta',  alpha=0.20, label= 'Cluster 7')
    plt.figure()

    # centroids
    #plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:,1], s= 25, c= 'yellow',  alpha=0.5, label= 'Centroids')

    #plt.title('Cluster 7')
    #plt.legend()
    #plt.savefig('clusters.png')
    plt.show()

    print("dance\n", data.groupby(['k_cluster']).acousticness.mean().sort_values(ascending=False))
    print("dance\n", data.groupby(['k_cluster']).danceability.mean().sort_values(ascending=False))
    print("energy\n", data.groupby(['k_cluster']).energy.mean().sort_values(ascending=False))
    print("instrulmentalness\n", data.groupby(['k_cluster']).instrumentalness.mean().sort_values(ascending=False))
    print("key\n", data.groupby(['k_cluster']).key.mean().sort_values(ascending=False))
    print("liveness\n", data.groupby(['k_cluster']).liveness.mean().sort_values(ascending=False))
    print("loud\n",data.groupby(['k_cluster']).loudness.mean().sort_values(ascending=False))
    print("mode\n",data.groupby(['k_cluster']).mode.mean().sort_values(ascending=False))
    print("speech\n",data.groupby(['k_cluster']).speechiness.mean().sort_values(ascending=False))
    '''

'''
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



#get items from the user mongo db
import pymongo
import sklearn
from sklearn.cluster import KMeans
from sklearn import metrics
import pandas as pd

with open("dbconnection.txt") as file:
    connectionstring = file.readline().strip()
client = pymongo.MongoClient(connectionstring)
mydb = client["Personify"]
mycol = mydb["Tracks"]

db = []
x = mycol.find()
for data in x:
    db.append(data['analysis'][3:])

#print(db)


#'title', 'artist', 'id','acousticness', 'danceability','energy','instrumentalness','key','liveness','loudness','mode','speechiness'

#do a kmeans clustering on the data in db


df = pd.DataFrame(db, columns=['acousticness', 'danceability','energy','instrumentalness','key','liveness','loudness','mode','speechiness'])

print(df)
km = KMeans(n_clusters = 5, init = 'k-means++', max_iter = 300, n_init = 10, random_state = 0)

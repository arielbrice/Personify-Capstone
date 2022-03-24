import urllib.parse

import mongoengine
import spotipy
import pymongo
from bson import ObjectId
from pymongo import MongoClient
import os
import datetime
import pprint
from database.track import Track

stat_keys = ['title', 'artist', 'id','acousticness', 'danceability','energy','instrumentalness','key','liveness','loudness','mode','speechiness']
with open("dbconnection.txt") as file:
    connectionstring = file.readline().strip()
client = MongoClient(connectionstring)
db = client['personify']
userCollection = db['users']

# couldn't tell you what this is for
def global_init():
    with open("dbconnection.txt") as file:
        connectionString = file.readline().strip()

    client = MongoClient(connectionString)
    db = client['Personify']
    trackCollection = db['Tracks']
    mongoengine.register_connection(alias='core', name='personify')
    mongoengine.connect(alias='pers-db', host=connectionString)
    return trackCollection



def userExists(id, coll):
    if(coll.count_documents({"user_id" : id.strip()}, limit=1) == 0):
        return False
    else:
        return True

def trackExists(title):
    coll = global_init()
    if (coll.count_documents({"title": title.strip()}, limit=1) == 0):
        return False
    else:
        print(title, "duplicate")
        return True

def insertTrack(features):
    global_init()
    analysis = []
    song = Track()
    song.song_id = features['id']
    song.artist = features['artist']
    song.title = features['title']

    for key in stat_keys:
        analysis.append(features[key])

    song.analysis = analysis

    song.save()


def updatePlaylist(id, tracks):
    userid = id
    playlist = tracks


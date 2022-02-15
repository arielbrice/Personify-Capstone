import mongoengine
import pymongo
from bson import ObjectId
from pymongo import MongoClient
import os
import datetime
import pprint

client = MongoClient('localhost', 27017)
db = client['personify']
userCollection = db['users']

# couldn't tell you what this is for
def global_init():
    mongoengine.register_connection(alias = 'core', name = 'personify')

def userExists(id):
    userid = id
    if(len(list(userCollection.find({"user_id" : id}))) == 0):
        return False
    else:
        return True

def updatePlaylist(id, tracks):
    userid = id
    playlist = tracks

    userCollection.
import mongoengine
from pymongo import MongoClient
import os
import datetime
import pprint

client = MongoClient()
client = MongoClient('localhost', 27017)
db = client.test_database
posts = db.posts

def testInsert():
    post = {"author": "Hannah",
         "text": "My first blog post!",
         "tags": ["mongodb", "python", "pymongo"],
         "date": datetime.datetime.utcnow()}

    post_id = posts.insert_one(post).inserted_id
    print(post_id)

def testFind():
    for post in posts.find():
        pprint.pprint(post)
testInsert()
testFind()





def global_init():
    mongoengine.register_connection(alias = 'core', name = 'personify')
import pymongo
from pymongo import MongoClient
import pandas as pd
import mongoengine


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

data = pd.DataFrame(list(trackCollection.find()))
data.to_csv('tracks.csv')
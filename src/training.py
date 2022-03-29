#get items from the user mongo db
import pymongo

with open("dbconnection.txt") as file:
    connectionstring = file.readline().strip()
client = pymongo.MongoClient(connectionstring)
mydb = client["Personify"]
mycol = mydb["Tracks"]

db = []
x = mycol.find()
for data in x:
    db.append(data['analysis'])

print(db)
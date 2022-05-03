from matplotlib.pyplot import title
from flask import Flask, request, url_for, session, redirect, render_template
from src.model.kmeansmodel import *
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time

from src.user.userTaste import topArtists, topTracks
import database.mongo_setup as mongo_setup
from database.user import User
from pymongo import MongoClient
import mongoengine
from tabulate import tabulate

### update this one if needed###
HOMEDIR = os.path.expanduser('~') + "/.personify"

PATHSEC = HOMEDIR+"/secret.txt"    
PATHDB = HOMEDIR + "/dbconnection.txt" 
# need to download the two files and save it under HOMEDIR

app = Flask(__name__)
app.config['SESSION_COOKIE_NAME'] = 'personify cookie'
app.secret_key = "0Ncs92894fhno"
################################

import os
import sys
if not os.path.isdir(HOMEDIR):
   os.system("mkdir " + HOMEDIR)


#if (not os.path.exists(PATHSEC)) or (not os.path.exists(PATHDB)):
#    print("Please download the two files secret.txt and dbconnection.txt and put it into the "+HOMEDIR)
#    sys.exit(0)


TOKEN_INFO = "token_info"
songrecs = []
with open("dbconnection.txt") as file:
    connectionString = file.readline().strip()



def getmongoClient():
    client = MongoClient(connectionString)
    db = client['Personify']
    userCollection = db['Users']
    mongoengine.disconnect('pers-db')
    mongo_setup.global_init()
    
    mongoengine.connect(alias='pers', host=connectionString)
    
    return userCollection


def getEntity(id, username):
    user = User()
    user.user_id = id
    user.username = username
    user.save()
    return user

def getToken():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        raise "exception"
    sp_oauth = create_spotify_oauth()
    if(sp_oauth.is_token_expired(token_info)):
        createToken()
    return token_info

def createToken():
    sp_oauth = create_spotify_oauth()

    if os.path.exists(".cache"):
        os.remove(".cache")
    try:
        token_info = sp_oauth.get_auth_response()
        session[TOKEN_INFO] = token_info
        return token_info
    except:
        print("exception")
        return None

def create_spotify_oauth():
    clientid, clientsecret = readFile()
    return SpotifyOAuth(client_id = clientid, client_secret=clientsecret,
        redirect_uri=url_for('redirectPage', _external = True), scope = 'user-top-read, playlist-modify-private, playlist-read-private, user-library-read')

def readFile():
    with open("secret.txt") as file:
        clientid = file.readline().strip()
        clientsecret = file.readline().strip()
        return clientid, clientsecret




@app.route('/')
def homepage():
    return render_template("home.html")

@app.route('/home')
def home():
    return homepage()

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/about')
def about():
    return render_template("about.html")

'''
Allows user to allow access to their Spotify info via Spotify auth page.
If the user is new, add a new entry into the database (user entity).
Using the spotipy .me() function, retrieve user display name and ID to send
as documents for new user entry. 
'''
@app.route('/login')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    code = request.args.get('code')
    #token_info = sp_oauth.get_access_token(code)
    try:
        token_info = createToken()
    except:
        
        print("user not logged in")
        return redirect(auth_url)

    coll = getmongoClient()
    sp = spotipy.Spotify(auth=token_info['access_token'])

    user_dict = sp.me()
    id = user_dict['id']
    username = user_dict['display_name']
    if(mongo_setup.userExists(id, coll) == False):
        getEntity(id, username)
        redirect(auth_url)
    else:
        redirect(auth_url)

    return redirect(auth_url)

@app.route('/redirect')
def redirectPage():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('user', _external=True))

@app.route('/user')
def user():
    try:
        token_info = getToken()
    except:
        print("user not logged in")
        return redirect(url_for('login', _external=False))
    sp = spotipy.Spotify(auth=token_info['access_token'])
    name = sp.me()['display_name']
    return render_template("user.html", name = name)

'''
primitive example for generating recs using astrology keywords as spotify search queries.
'''
'''
@app.route('/getSongs')
def getSongs():
    try:
        token_info = getToken()
    except:
        print("user not logged in")
        return redirect(url_for('login', _external=False))
    sp = spotipy.Spotify(auth=token_info['access_token'])
    songlist = []
    with open("keywords2.txt") as keywordFile:
        for keyword in keywordFile:
            results = sp.search(q = keyword, limit=10)
            print("\n",keyword)
            for idx, track in enumerate(results['tracks']['items']):
                songlist += idx , track['name']
    return "These are some songs we reccomend for a leo: " + str(songlist)
'''

#TODO: write creating a playlist function
@app.route('/playlist')
def makePlaylist():
    try:
        token_info = getToken()
    except:
        print("user not logged in")
        return redirect(url_for('login', _external=False))
    sp = spotipy.Spotify(auth=token_info['access_token'])

    u = sp.me()
    id = u['id']

    recs = modeRecs(id, sp)
    for itemt, itema in zip(recs['title'] , recs['artist']):
        print(itemt, itema)
    table = [['one','two','three'],['four','five','six'],['seven','eight','nine']]
    value = tabulate(table, tablefmt='html')

    print(tabulate(table))

    songrecs.clear()
    songrecs.extend(recs["song_id"])

    clusterCount = 0
    #cluster = recs["k_cluster"].count(5)
    #print("\n", cluster)

        
    return render_template("playlist.html", name = u['display_name'], playlist = zip(recs['title'], recs['artist']), title = recs['title'], artist = recs['artist'])


#TODO: export a playlist that is created from our algorithm
@app.route('/export')
def exportPlaylist():
    try:
        token_info = getToken()
    except:
        print("user not logged in")
        return redirect(url_for('login', _external=False))
    sp = spotipy.Spotify(auth=token_info['access_token'])
    playlist = sp.user_playlist_create(sp.me()['id'], "Personify Recomendations", public = False, description= "This playlist was made using KMeans Machiene Learning!")
    playlist_id = playlist["id"]
    if(songrecs == []):
        return makePlaylist()
    #print(songrecs)
    try:
        sp.playlist_add_items(playlist_id, songrecs[:25], position=None)
        sp.playlist_add_items(playlist_id, songrecs[25:], position=None)
    except:
        print("error")
        return makePlaylist()
    return user()

def getToken():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        raise "exception"
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if(is_expired):
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.get_refresh_access_token(token_info['refresh_token'])
    return token_info

def create_spotify_oauth():
    clientid, clientsecret = readFile()
    return SpotifyOAuth(client_id = clientid, client_secret=clientsecret,
        redirect_uri=url_for('redirectPage', _external = True), scope = 'user-top-read, playlist-modify-private, playlist-read-private, user-library-read') 

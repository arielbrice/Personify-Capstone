from flask import Flask, request, url_for, session, redirect, render_template
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
app = Flask(__name__)
from src.user.userTaste import printtopA, topArtists, topTracks
from src.model.GeneralModel import showSongNames



app.secret_key = "0Ncs92894fhno"
app.config['SESSION_COOKIE_NAME'] = 'personify cookie'
TOKEN_INFO = "token_info"

def readFile():
    with open("secret.txt") as file:
   # print(file.readline(), file.readline())
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

@app.route('/login')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    print(auth_url)
    return redirect(auth_url)

@app.route('/redirect')
def redirectPage():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('user', _external=True))
    #return redirect(url_for('user', _external=True))

@app.route('/user')
def user():
    try:
        token_info = getToken()
    except:
        print("user not logged in")
        return redirect(url_for('login', _external=False))
    sp = spotipy.Spotify(auth=token_info['access_token'])
    name = sp.me()['display_name']
    clientid, clientsecret = readFile()
    topTracks(sp)
    return render_template("user.html", name = name)

@app.route('/getTracks')
def getTracks():
    try:
        token_info = getToken()
    except:
        print("user not logged in")
        return redirect(url_for('login', _external=False))
    sp = spotipy.Spotify(auth=token_info['access_token'])
    all_songs = []
    iter = 0
    print(sp.me())
    while True:
        items = sp.current_user_saved_tracks(limit=50, offset=iter * 50)['items']
        iter += 1
        all_songs += items
        if(len(items) < 50):
            break
      
    return "This is the amount of liked songs that " + sp.me()['display_name'] + " has: "+ str(len(all_songs))
   
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
                #print(idx, track['name'])
                #print(songlist)
    return "These are some songs we reccomend for a leo: " + str(songlist)

@app.route('/topTracks')
def trackTop():
    try:
        token_info = getToken()
    except:
        print("user not logged in")
        return redirect(url_for('login', _external=False))
    sp = spotipy.Spotify(auth=token_info['access_token'])

    return "tracks: " + topTracks(sp)

@app.route('/topArtists')
def artistTop():
    try:
        token_info = getToken()
    except:
        print("user not logged in")
        return redirect(url_for('login', _external=False))
    sp = spotipy.Spotify(auth=token_info['access_token'])
    
    return "artists: " + topArtists(sp)

@app.route('/playlist')
def makePlaylist():
    try:
        token_info = getToken()
    except:
        print("user not logged in")
        return redirect(url_for('login', _external=False))
    sp = spotipy.Spotify(auth=token_info['access_token'])
    return showSongNames(sp)

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
        redirect_uri=url_for('redirectPage', _external = True), scope = 'user-top-read, playlist-modify-private') #scope = "user-library-read")
        
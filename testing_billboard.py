import billboard
import pandas as pd
import spotipy
from spotipy import SpotifyClientCredentials

from database import mongo_setup

with open("secret.txt", encoding="UTF-8") as file:
    clientid = file.readline().strip()
    clientsecret = file.readline().strip()
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=clientid, client_secret=clientsecret))

def tuple_to_dict(chart):
    # Converts the chart provided from billboard to a pandas dataframe
    t = ([{'title': i.title, 'artist': i.artist} for i in chart.entries])
    chart_entries = t
    df = pd.DataFrame.from_dict(chart_entries)
    return df

#iterate through all the months
#need to add a way to iterate through years
months = ['01', '02','03','04', '05', '06', '07','08','09','10','11','12']


def get_spotify_stats(title, artist, track):
    stat_map = {}
    """
    audio_analysis(track_id)
        Get audio analysis for a track based upon its Spotify ID Parameters:

        track_id - a track URI, URL or ID
        audio_features(tracks=[])
        Get audio features for one or multiple tracks based upon their Spotify IDs Parameters:

        tracks - a list of track URIs, URLs or IDs, maximum: 100 ids
    """
    stat_keys = ['title', 'artist', 'id','acousticness', 'danceability','energy','instrumentalness','key','liveness','loudness','mode','speechiness']
    for keys in stat_keys:
        stat_map[keys] = 0

    stat_map['title'] = title
    stat_map['artist'] = artist

    for item in track:
        raw_stats = sp.audio_features(item['id'])
        stat_map['id'] = item['id']
        for song in raw_stats:
            for feat in song:
                if feat in stat_keys:
                    stat_map[feat] = song[feat]

        add_songs_to_db(stat_map)

def add_songs_to_db(song):
    mongo_setup.insertTrack(song)

for year in range(1960,2021):
    for i in months:
        chart = billboard.ChartData('hot-100', date='{0}-{1}-15'.format(str(year), i))
        chart_df = tuple_to_dict(chart)
        for index, row in chart_df.iterrows():
            """
            check if song is in db
            if so, skip
            else query spotify for other info
            save info to db and continue
            """
            result = sp.search(q = "{} {}".format(row['title'], row['artist']), limit=1)
            track = result['tracks']['items']
            stats = get_spotify_stats(row['title'], row['artist'], track)
        #pass stats as dictionary or whatever formating is easiet after spotify query is done
    #add_songs_to_db(row["title"], row["artist"], stats)

    break
        #chart_df.to_csv('hot-100-{0}-{1}-15.csv'.format(str(year), i), sep=',', encoding='utf-8')




"""
Take the artists and songs from each df
for each artist and song, do a search on spotify if it has not already been searched
result = sp.search(q = keyword, limit=1)
once we have the song id,
we're going to use that to query the audio features from Spotify
for each spotify ID:
create a database entry
save the following information:
Title, Artist, Spotify Song ID, Acousticness, Dancebility, Energy, Instrumentalness, Key, Liveness, Loudness, Mode, Speechiness, Tempo, Time_Signature, Valence
"""

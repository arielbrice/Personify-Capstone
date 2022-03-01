import billboard
import pandas as pd

def tuple_to_dict(chart):
    # Converts the chart provided from billboard to a pandas dataframe
    t = ([{'title': i.title, 'artist': i.artist} for i in chart.entries])
    chart_entries = t
    df = pd.DataFrame.from_dict(chart_entries)
    return df

#iterate through all the months
#need to add a way to iterate through years
months = ['01']
for i in months:
    chart = billboard.ChartData('hot-100', date='2019-%s-15' % i)
    chart_df = tuple_to_dict(chart)
    chart_df.to_csv('hot-100-2019-%s-15.csv' % i, sep=',', encoding='utf-8')

# Take the artists and songs from each df
# for each artist and song, do a search on spotify if it has not already been searched
# once we have the song id,
# we're going to use that to query the audio features from Spotify
# for each spotify ID:
# create a database entry
# save the following information:
# Title, Artist, Acousticness, Dancebility, Energy, Instrumentalness, Key, Liveness, Loudness, Mode, Speechiness, Tempo, Time_Signature, Valence

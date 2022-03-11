import mongoengine


class Track(mongoengine.Document):
    title = mongoengine.StringField(required=True)
    artist = mongoengine.StringField(required=True)
    song_id = mongoengine.StringField(required=True)
    analysis = mongoengine.ListField(required=True)
    '''
    accousticness = mongoengine.FloatField(required=True)
    danceability = mongoengine.FloatField(required=True)
    energy = mongoengine.FloatField(required=True)
    instrumentalness = mongoengine.FloatField(required=True)
    liveness = mongoengine.FloatField(required=True)
    loudness = mongoengine.FloatField(required=True)
    mode = mongoengine.BooleanField(required=True)
    speechiness = mongoengine.FloatField(required=True)
    time_signature = mongoengine.IntField(required=True)
    valence = mongoengine.FloatField(required=True)
    '''

    '''
    or we could do:
    title = mongoengine.StringField(required=True)
    artist = mongoengine.StringField(required=True)
    song_id = mongoengine.IntField(required=True)
    audio_analysis = [f1, f2, f3,..., f10]
    
    '''

    meta = {
        'db_alias': 'pers-db',
        'collection': 'Track'}
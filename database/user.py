import datetime
import mongoengine


class User(mongoengine.Document):
    registration_date = mongoengine.DateTimeField(default=datetime.datetime.now)
    # TODO: automate getting user id straight from
    # Spotify API
    user_id = mongoengine.StringField(required=True)
    username = mongoengine.StringField(required=True)
    #sign = mongoengine.StringField(required=True)
    playlist = mongoengine.ListField(required=False)

    meta = {
        'db_alias': 'pers-db',
        'collection': 'Users'}
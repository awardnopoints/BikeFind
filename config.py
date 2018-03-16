import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'TeamHero'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
            'mysql+cymysql://conor:team0db1@team0db.cojxdhcdsq2b.us-west-2.rds.amazonaws.com/testdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


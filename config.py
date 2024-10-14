import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'marketplace.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY') or 'you-will-never-guess-zarif'

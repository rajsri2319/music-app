import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', f"sqlite:///{os.path.join(basedir,'database.db')}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret')
    AUDIO_FILES_PATH = os.environ.get('AUDIO_FILES_PATH', os.path.join(basedir, 'audio'))  # local for dev
    # OAuth placeholders — set real client ids/secrets in env for production
    OAUTH_GOOGLE_CLIENT_ID = os.environ.get('OAUTH_GOOGLE_CLIENT_ID')
    OAUTH_GOOGLE_CLIENT_SECRET = os.environ.get('OAUTH_GOOGLE_CLIENT_SECRET')

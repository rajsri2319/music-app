from datetime import datetime
from extensions import db
import bcrypt

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(180), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.LargeBinary(60), nullable=True)  # bcrypt
    provider = db.Column(db.String(40), nullable=True)  # 'google' etc.
    provider_id = db.Column(db.String(200), nullable=True)
    avatar_url = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # settings JSON omitted for brevity

    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def check_password(self, password):
        if not self.password_hash:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash)

class Artist(db.Model):
    __tablename__ = 'artists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)

class Album(db.Model):
    __tablename__ = 'albums'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'))
    cover_url = db.Column(db.String(400))

class Track(db.Model):
    __tablename__ = 'tracks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'))
    album_id = db.Column(db.Integer, db.ForeignKey('albums.id'))
    duration = db.Column(db.Integer)  # seconds
    file_key = db.Column(db.String(512), nullable=False)  # path or S3 key
    mime_type = db.Column(db.String(80), default='audio/mpeg')
    is_lossless = db.Column(db.Boolean, default=False)
    bitrate = db.Column(db.Integer)
    sample_rate = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Playlist(db.Model):
    __tablename__ = 'playlists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    is_public = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class PlaylistTrack(db.Model):
    __tablename__ = 'playlist_tracks'
    id = db.Column(db.Integer, primary_key=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlists.id'))
    track_id = db.Column(db.Integer, db.ForeignKey('tracks.id'))
    position = db.Column(db.Integer, default=0)

class Listen(db.Model):
    __tablename__ = 'listens'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    track_id = db.Column(db.Integer, db.ForeignKey('tracks.id'))
    device_id = db.Column(db.String(200), nullable=True)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    ended_at = db.Column(db.DateTime)
    duration = db.Column(db.Integer)

class Lyrics(db.Model):
    __tablename__ = 'lyrics'
    id = db.Column(db.Integer, primary_key=True)
    track_id = db.Column(db.Integer, db.ForeignKey('tracks.id'), unique=True)
    lrc = db.Column(db.Text)  # store LRC formatted lyric text

class Device(db.Model):
    __tablename__ = 'devices'
    id = db.Column(db.String(200), primary_key=True)  # uuid from client
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(200))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    ws_sid = db.Column(db.String(200))  # socket session id for ws routing

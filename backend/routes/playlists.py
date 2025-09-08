from flask import Blueprint, request, jsonify
from extensions import db
from models import Playlist, PlaylistTrack, Track
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint('playlists', __name__)

@bp.route('/', methods=['POST'])
@jwt_required()
def create_playlist():
    uid = get_jwt_identity()
    data = request.get_json()
    p = Playlist(name=data.get('name','New Playlist'), user_id=uid, is_public=data.get('is_public', False))
    db.session.add(p); db.session.commit()
    return jsonify({'id': p.id, 'name': p.name}), 201

@bp.route('/<int:pid>/tracks', methods=['POST'])
@jwt_required()
def add_track(pid):
    data = request.get_json()
    track_id = data.get('track_id')
    pos = data.get('position', 0)
    pt = PlaylistTrack(playlist_id=pid, track_id=track_id, position=pos)
    db.session.add(pt); db.session.commit()
    return jsonify({'msg': 'added'}), 201

@bp.route('/user/<int:uid>', methods=['GET'])
def list_user_playlists(uid):
    pls = Playlist.query.filter_by(user_id=uid).all()
    return jsonify([{'id': p.id, 'name': p.name, 'is_public': p.is_public} for p in pls])

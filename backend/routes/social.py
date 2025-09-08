from flask import Blueprint, request, jsonify
from models import Playlist, Track
bp = Blueprint('social', __name__)

@bp.route('/share/playlist/<int:pid>', methods=['POST'])
def share_playlist(pid):
    # In production create a short slug and OGP meta endpoint
    p = Playlist.query.get_or_404(pid)
    return jsonify({'share_url': f'/share/playlist/{pid}', 'msg': 'share link created'})

@bp.route('/feed/<int:user_id>', methods=['GET'])
def feed(user_id):
    # stub: return random activity
    return jsonify([{'type':'listening','user_id':user_id,'track_id': 1, 'title':'Sample Track'}])

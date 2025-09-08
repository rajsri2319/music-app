from flask import Blueprint, jsonify
from models import Track
bp = Blueprint('recs', __name__)

@bp.route('/for_user', methods=['GET'])
def recs_for_user():
    # MVP: simple popularity-based recommendation
    tracks = Track.query.order_by(Track.id.desc()).limit(20).all()
    return jsonify([{'id': t.id, 'title': t.title} for t in tracks])

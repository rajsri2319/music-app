from flask import Blueprint, request, jsonify
from models import Track
bp = Blueprint('search', __name__)

@bp.route('/', methods=['GET'])
def search():
    q = request.args.get('q','')
    tracks = Track.query.filter(Track.title.ilike(f'%{q}%')).limit(50).all()
    return jsonify([{'id':t.id,'title':t.title,'duration':t.duration} for t in tracks])

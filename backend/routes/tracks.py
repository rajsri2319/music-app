from flask import Blueprint, request, send_file, abort, current_app, Response, jsonify
from extensions import db
from models import Track, Lyrics, Listen
import os, re
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

bp = Blueprint('tracks', __name__)

@bp.route('/', methods=['GET'])
def list_tracks():
    q = request.args.get('q')
    query = Track.query
    if q:
        query = query.filter(Track.title.ilike(f'%{q}%'))
    tracks = query.limit(200).all()
    out = []
    for t in tracks:
        out.append({'id': t.id, 'title': t.title, 'duration': t.duration,
                    'file_key': t.file_key, 'mime_type': t.mime_type, 'is_lossless': t.is_lossless})
    return jsonify(out)

@bp.route('/<int:track_id>', methods=['GET'])
def track_detail(track_id):
    t = Track.query.get_or_404(track_id)
    return jsonify({'id': t.id, 'title': t.title, 'duration': t.duration, 'mime_type': t.mime_type})

def local_path_for(track):
    # In production, generate signed S3 urls or proxy S3 range requests
    return os.path.join(current_app.config['AUDIO_FILES_PATH'], track.file_key)

@bp.route('/<int:track_id>/stream', methods=['GET'])
def stream_track(track_id):
    track = Track.query.get_or_404(track_id)
    path = local_path_for(track)
    if not os.path.exists(path):
        return abort(404)
    file_size = os.path.getsize(path)
    range_header = request.headers.get('Range', None)
    if not range_header:
        return send_file(path, mimetype=track.mime_type, conditional=True)
    m = re.match(r'bytes=(\d+)-(\d*)', range_header)
    if not m:
        return Response(status=416)
    start = int(m.group(1))
    end = int(m.group(2)) if m.group(2) else file_size - 1
    if end >= file_size:
        end = file_size - 1
    length = end - start + 1
    with open(path, 'rb') as f:
        f.seek(start)
        data = f.read(length)
    rv = Response(data, status=206, mimetype=track.mime_type, direct_passthrough=True)
    rv.headers.add('Content-Range', f'bytes {start}-{end}/{file_size}')
    rv.headers.add('Accept-Ranges', 'bytes')
    rv.headers.add('Content-Length', str(length))
    return rv

@bp.route('/<int:track_id>/lyrics', methods=['GET'])
def get_lyrics(track_id):
    ly = Lyrics.query.filter_by(track_id=track_id).first()
    if not ly:
        return jsonify({'lrc': None})
    return jsonify({'lrc': ly.lrc})

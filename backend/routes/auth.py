from flask import Blueprint, request, jsonify, current_app, url_for
from extensions import db
from models import User
from flask_jwt_extended import create_access_token, create_refresh_token
import requests

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data.get('email') or not data.get('password'):
        return jsonify({'msg': 'email and password required'}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'msg': 'email exists'}), 400
    user = User(email=data['email'], username=data.get('username') or data['email'].split('@')[0])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    access = create_access_token(identity=user.id)
    refresh = create_refresh_token(identity=user.id)
    return jsonify({'access_token': access, 'refresh_token': refresh, 'user': {'id': user.id, 'username': user.username}}), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data.get('email')).first()
    if not user or not user.check_password(data.get('password', '')):
        return jsonify({'msg': 'bad credentials'}), 401
    access = create_access_token(identity=user.id)
    refresh = create_refresh_token(identity=user.id)
    return jsonify({'access_token': access, 'refresh_token': refresh, 'user': {'id': user.id, 'username': user.username}}), 200

# OAuth simplified flow (real integration requires client ids/secrets + redirect URIs)
@bp.route('/oauth/google', methods=['GET'])
def oauth_google():
    # In production, redirect to Google's OAuth endpoint with client_id and redirect_uri
    return jsonify({'msg': 'OAuth stub — implement Google OAuth in production'}), 501

from flask_jwt_extended import decode_token
from extensions import socketio, db
from models import Device, User
from flask import current_app

def init_ws(socketio_app, app):
    @socketio_app.on('connect')
    def handle_connect(auth):
        # auth should contain access_token and device_id
        token = None
        device_id = None
        if isinstance(auth, dict):
            token = auth.get('token')
            device_id = auth.get('device_id')
        if not token or not device_id:
            return False  # reject
        try:
            decoded = decode_token(token)
            uid = decoded['sub']
            # register device session
            d = Device.query.get(device_id)
            if not d:
                d = Device(id=device_id, user_id=uid, name='Web Device')
                db.session.add(d)
            d.ws_sid = socketio_app.server.eio_sid_from_sid(request.sid) if hasattr(socketio_app.server, 'eio_sid_from_sid') else request.sid
            db.session.commit()
            socketio_app.emit('device_connected', {'device_id': device_id, 'user_id': uid}, room=request.sid)
        except Exception as e:
            current_app.logger.error('ws connect error: %s', e)
            return False

    @socketio_app.on('transfer_playback')
    def handle_transfer(data):
        # data: {to_device_id, track_id, position}
        to_device = Device.query.get(data.get('to_device_id'))
        if to_device and to_device.ws_sid:
            socketio_app.emit('transfer_request', {'track_id': data.get('track_id'), 'position': data.get('position')}, room=to_device.ws_sid)

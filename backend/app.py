from flask import Flask
from config import Config
from extensions import db, migrate, jwt, cors, socketio
import os

def create_app():
    app = Flask(__name__, static_folder=None)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")

    # Blueprints
    from routes.auth import bp as auth_bp
    from routes.users import bp as users_bp
    from routes.tracks import bp as tracks_bp
    from routes.playlists import bp as playlists_bp
    from routes.search import bp as search_bp
    from routes.recommendations import bp as recs_bp
    from routes.social import bp as social_bp

    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(users_bp, url_prefix='/api/v1/users')
    app.register_blueprint(tracks_bp, url_prefix='/api/v1/tracks')
    app.register_blueprint(playlists_bp, url_prefix='/api/v1/playlists')
    app.register_blueprint(search_bp, url_prefix='/api/v1/search')
    app.register_blueprint(recs_bp, url_prefix='/api/v1/recommendations')
    app.register_blueprint(social_bp, url_prefix='/api/v1/social')

    # WebSocket handlers
    from ws import init_ws
    init_ws(socketio, app)

    @app.route('/health')
    def health():
        return {'status': 'ok'}, 200

    return app

app = create_app()

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

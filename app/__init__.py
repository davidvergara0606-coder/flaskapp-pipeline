from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from app.config.settings import Config
from app.database.database import db

migrate = Migrate()


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    CORS(app, resources={r"/*": {"origins": "*"}})

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes.auth import auth_bp, productos_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(productos_bp)

    @app.get("/health")
    def health():
        # El pipeline de despliegue llama a esta ruta para confirmar que la app arrancó.
        return jsonify(status="ok"), 200

    return app

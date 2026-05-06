from flask import Flask, jsonify
import logging
import os
from db.database import Database
from services.organization_service import OrganizationService
from services.gem_service import GemService
from routes.main_routes import main_bp
from routes.organization_routes import org_bp
from routes.gem_routes import gem_bp

def create_app():
    app = Flask(__name__,
                static_folder='static',
                template_folder='templates')

    # Logging configuration
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("sysgem.log"),
            logging.StreamHandler()
        ]
    )

    # Database configuration
    DB_CONFIG = {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": os.getenv("DB_PORT", "5432"),
        "user": os.getenv("DB_USER", "postgres"),
        "password": os.getenv("DB_PASSWORD", "xbala"),
        "database": os.getenv("DB_NAME", "db_gem")
    }

    db = Database(DB_CONFIG)
    org_service = OrganizationService(db)
    gem_service = GemService(db)

    # Store service in app config for access in routes
    app.config['ORG_SERVICE'] = org_service
    app.config['GEM_SERVICE'] = gem_service

    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(org_bp)
    app.register_blueprint(gem_bp, url_prefix='/<schema>')

    # Global error handler for JSON responses
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"ok": False, "erro": "Recurso não encontrado"}), 404

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({"ok": False, "erro": "Erro interno do servidor"}), 500

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)

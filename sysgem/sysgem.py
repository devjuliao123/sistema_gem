from flask import Flask, jsonify
import logging
import os
from sysgem_db.database import Database
from sysgem_services.organization_service import OrganizationService
from sysgem_services.gem_service import GemService
from sysgem_routes.op_main_routes import op_main_bp
from sysgem_routes.gem_routes import gem_bp

def create_app():
    app = Flask(__name__,
                static_folder='static',
                template_folder='templates')

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("sysgem_op.log"),
            logging.StreamHandler()
        ]
    )

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

    app.config['ORG_SERVICE'] = org_service
    app.config['GEM_SERVICE'] = gem_service

    app.register_blueprint(op_main_bp)
    app.register_blueprint(gem_bp, url_prefix='/<schema>')

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"ok": False, "erro": "Recurso não encontrado"}), 404

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)

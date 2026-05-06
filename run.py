from flask import Flask, jsonify
import logging
import os
import sys

# Adiciona o diretório sysgem ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'sysgem'))

from sysgem_db.database import Database
from sysgem_services.organization_service import OrganizationService
from sysgem_routes.control_main_routes import main_bp
from sysgem_routes.control_organization_routes import org_bp

def create_app():
    app = Flask(__name__,
                static_folder='sysgem/static',
                template_folder='sysgem/templates/control')

    logging.basicConfig(level=logging.INFO)

    DB_CONFIG = {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": os.getenv("DB_PORT", "5432"),
        "user": os.getenv("DB_USER", "postgres"),
        "password": os.getenv("DB_PASSWORD", "xbala"),
        "database": os.getenv("DB_NAME", "db_gem")
    }

    db = Database(DB_CONFIG)
    org_service = OrganizationService(db)
    app.config['ORG_SERVICE'] = org_service

    app.register_blueprint(main_bp)
    app.register_blueprint(org_bp, url_prefix='/api/organizacoes')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5001)

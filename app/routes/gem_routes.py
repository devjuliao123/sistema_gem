from flask import Blueprint, render_template, current_app, abort, g, request
import re

gem_bp = Blueprint('gem', __name__)

@gem_bp.url_value_preprocessor
def pull_schema(endpoint, values):
    g.schema = values.pop('schema', None)

@gem_bp.before_request
def validate_schema():
    if not g.schema:
        abort(404)

    # Security: Strict schema name validation
    if not re.match(r'^org_\d{4}$', g.schema):
        abort(400, "Schema inválido")

    org_service = current_app.config['ORG_SERVICE']
    if not org_service.schema_exists(g.schema):
        abort(404, "Organização não encontrada")

@gem_bp.route('/inicio')
def inicio():
    gem_service = current_app.config['GEM_SERVICE']
    stats = gem_service.get_stats(g.schema)
    org_info = gem_service.get_organizacao_info(g.schema)

    return render_template('gem/menu.html',
                           schema=g.schema,
                           org_info=org_info,
                           stats=stats)

# Placeholders for other modules
@gem_bp.route('/alunos')
def alunos():
    return f"Módulo de Alunos para {g.schema} (Em breve)"

@gem_bp.route('/instrutores')
def instrutores():
    return f"Módulo de Instrutores para {g.schema} (Em breve)"

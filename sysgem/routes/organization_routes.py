from flask import Blueprint, request, jsonify, current_app
import logging

org_bp = Blueprint('org', __name__, url_prefix='/api/organizacoes')

def get_service():
    return current_app.config['ORG_SERVICE']

@org_bp.route('/', methods=['GET'])
def list_orgs():
    try:
        service = get_service()
        data = service.list_all()
        return jsonify({"ok": True, "data": data})
    except Exception as e:
        return jsonify({"ok": False, "erro": str(e)}), 500

@org_bp.route('/', methods=['POST'])
def create_org():
    try:
        data = request.json
        nome = data.get("nome")
        if not nome:
            return jsonify({"ok": False, "erro": "Nome é obrigatório"}), 400

        service = get_service()
        result = service.create(nome)
        return jsonify({"ok": True, "data": result}), 201
    except ValueError as e:
        return jsonify({"ok": False, "erro": str(e)}), 400
    except Exception as e:
        logging.error(f"Error in create_org: {e}")
        return jsonify({"ok": False, "erro": "Erro interno do servidor"}), 500

@org_bp.route('/<int:numero>', methods=['DELETE'])
def delete_org(numero):
    try:
        service = get_service()
        service.delete(numero)
        return jsonify({"ok": True})
    except ValueError as e:
        return jsonify({"ok": False, "erro": str(e)}), 404
    except Exception as e:
        logging.error(f"Error in delete_org: {e}")
        return jsonify({"ok": False, "erro": "Erro interno do servidor"}), 500

@org_bp.route('/validar-nome', methods=['GET'])
def validate_name():
    nome = request.args.get("nome")
    if not nome:
        return jsonify({"ok": False, "erro": "Nome não fornecido"}), 400

    service = get_service()
    is_valid = service.validate_name(nome)
    return jsonify({"ok": True, "disponivel": is_valid})

@org_bp.route('/validar-schema/<schema_name>', methods=['GET'])
def validate_schema(schema_name):
    service = get_service()
    exists = service.schema_exists(schema_name)
    return jsonify({"ok": True, "existe": exists})

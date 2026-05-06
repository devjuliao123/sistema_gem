from flask import Blueprint, render_template, request, redirect, url_for, current_app

op_main_bp = Blueprint('op_main', __name__)

@op_main_bp.route('/')
def login():
    # Página simples de login ou seleção de organização para a operação
    return render_template('login.html')

@op_main_bp.route('/entrar', methods=['POST'])
def entrar():
    schema = request.form.get('schema')
    if schema:
        return redirect(f"/{schema}/inicio")
    return redirect(url_for('op_main.login'))

from flask import Blueprint, request, jsonify, current_app
from models import db, Viagem, User
from flask_jwt_extended import jwt_required, get_jwt_identity
import pandas as pd
from datetime import datetime
import io

admin_bp = Blueprint('admin_bp', __name__)

# Helper para verificar se o usuário é admin
def admin_required_custom():
    def wrapper(fn):
        @jwt_required()
        def decorator(*args, **kwargs):
            current_user_identity = get_jwt_identity()
            if not current_user_identity or not current_user_identity.get('is_admin'):
                return jsonify(msg="Acesso restrito a administradores."), 403
            return fn(*args, **kwargs)
        # Renomear o wrapper para evitar conflitos de nome com Flask
        decorator.__name__ = f"admin_protected_{fn.__name__}"
        return decorator
    return wrapper

@admin_bp.route('/load_csv_data', methods=['POST'])
@admin_required_custom()
def load_csv_data():
    if 'file' not in request.files:
        return jsonify({"msg": "Nenhum arquivo CSV enviado"}), 400
    
    file = request.files['file']
    if file.filename == '' or not file.filename.endswith('.csv'):
        return jsonify({"msg": "Arquivo inválido ou não é CSV"}), 400

    try:
        # Ler o CSV diretamente do stream do arquivo
        # Especificar encoding pode ser necessário, ex: encoding='latin1' ou 'utf-8'
        try:
            df = pd.read_csv(io.StringIO(file.stream.read().decode('utf-8')))
        except UnicodeDecodeError:
            file.stream.seek(0) # Resetar o ponteiro do stream
            df = pd.read_csv(io.StringIO(file.stream.read().decode('latin1')))


        # Validar colunas esperadas (ajuste conforme seu CSV)
        expected_cols = ['data_hora', 'linha_onibus', 'bairro_origem', 'bairro_destino', 'passageiros']
        if not all(col in df.columns for col in expected_cols):
            return jsonify({"msg": f"Colunas esperadas não encontradas: {expected_cols}"}), 400

        viagens_para_adicionar = []
        for _, row in df.iterrows():
            # Limpeza e conversão de dados
            try:
                data_hora = pd.to_datetime(row['data_hora'])
            except Exception:
                current_app.logger.warning(f"Skipping row due to invalid date: {row['data_hora']}")
                continue

            viagem = Viagem(
                data_hora=data_hora,
                linha_onibus=str(row['linha_onibus']),
                bairro_origem=str(row['bairro_origem']),
                bairro_destino=str(row['bairro_destino']),
                passageiros=int(row['passageiros']) if pd.notna(row['passageiros']) else 0,
                lat_origem=float(row['lat_origem']) if 'lat_origem' in row and pd.notna(row['lat_origem']) else None,
                lon_origem=float(row['lon_origem']) if 'lon_origem' in row and pd.notna(row['lon_origem']) else None,
                lat_destino=float(row['lat_destino']) if 'lat_destino' in row and pd.notna(row['lat_destino']) else None,
                lon_destino=float(row['lon_destino']) if 'lon_destino' in row and pd.notna(row['lon_destino']) else None
            )
            viagens_para_adicionar.append(viagem)
        
        if viagens_para_adicionar:
            db.session.bulk_save_objects(viagens_para_adicionar)
            db.session.commit()
        
        return jsonify({"msg": f"{len(viagens_para_adicionar)} registros de viagem carregados com sucesso!"}), 201

    except pd.errors.EmptyDataError:
        return jsonify({"msg": "Arquivo CSV vazio"}), 400
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro ao carregar CSV: {e}", exc_info=True)
        return jsonify({"msg": "Erro ao processar o arquivo CSV", "error": str(e)}), 500

@admin_bp.route('/users', methods=['GET'])
@admin_required_custom()
def get_users():
    users = User.query.all()
    return jsonify([{
        "id": str(user.id), "username": user.username, "email": user.email, "is_admin": user.is_admin
    } for user in users]), 200

@admin_bp.route('/users/<uuid:user_id>/toggle_admin', methods=['PATCH'])
@admin_required_custom()
def toggle_admin_status(user_id):
    user_to_modify = User.query.get_or_404(str(user_id))
    
    # Evitar que o admin se despromova se for o único
    current_user_identity = get_jwt_identity()
    if str(user_to_modify.id) == current_user_identity['id'] and user_to_modify.is_admin:
        admin_count = User.query.filter_by(is_admin=True).count()
        if admin_count <= 1:
            return jsonify(msg="Não é possível remover o status de admin do único administrador."), 403
            
    user_to_modify.is_admin = not user_to_modify.is_admin
    db.session.commit()
    return jsonify(msg=f"Status de admin do usuário {user_to_modify.username} atualizado para {user_to_modify.is_admin}."), 200

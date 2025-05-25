from flask import Blueprint, request, jsonify, current_app
from models import db, Viagem
from flask_jwt_extended import jwt_required, get_jwt_identity
from io import BytesIO
import pandas as pd
import matplotlib
matplotlib.use('Agg') # Non-interactive backend
import matplotlib.pyplot as plt
from sqlalchemy import func
from datetime import datetime

mobilidade_bp = Blueprint('mobilidade_bp', __name__)
# Helper para verificar se o usuário é admin (pode ser um decorator mais robusto)
def is_admin():
    current_user = get_jwt_identity()
    return current_user and current_user.get('is_admin', False)

# --- CRUD para Viagens ---
@mobilidade_bp.route('/viagens', methods=['POST'])
@jwt_required()
def create_viagem():
    if not is_admin(): # Apenas admin pode criar diretamente, por exemplo
         return jsonify({"msg": "Acesso não autorizado"}), 403
    data = request.get_json()
    try:
        # Adicionar validação de dados aqui (ex: com Marshmallow ou Pydantic)
        nova_viagem = Viagem(
            data_hora=datetime.fromisoformat(data['data_hora']),
            linha_onibus=data['linha_onibus'],
            bairro_origem=data['bairro_origem'],
            bairro_destino=data['bairro_destino'],
            passageiros=data['passageiros'],
            lat_origem=data.get('lat_origem'),
            lon_origem=data.get('lon_origem'),
            lat_destino=data.get('lat_destino'),
            lon_destino=data.get('lon_destino')
        )
        db.session.add(nova_viagem)
        db.session.commit()
        return jsonify(nova_viagem.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Erro ao criar viagem", "error": str(e)}), 400

@mobilidade_bp.route('/viagens', methods=['GET'])
@jwt_required()
def get_viagens():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Filtros opcionais
    filters = []
    if 'bairro_origem' in request.args:
        filters.append(Viagem.bairro_origem.ilike(f"%{request.args['bairro_origem']}%"))
    if 'bairro_destino' in request.args:
        filters.append(Viagem.bairro_destino.ilike(f"%{request.args['bairro_destino']}%"))
    if 'linha_onibus' in request.args:
        filters.append(Viagem.linha_onibus == request.args['linha_onibus'])
    if 'data_inicio' in request.args and 'data_fim' in request.args:
        try:
            data_inicio = datetime.fromisoformat(request.args['data_inicio'])
            data_fim = datetime.fromisoformat(request.args['data_fim'])
            filters.append(Viagem.data_hora.between(data_inicio, data_fim))
        except ValueError:
            return jsonify({"msg": "Formato de data inválido. Use YYYY-MM-DDTHH:MM:SS"}), 400

    viagens_pagination = Viagem.query.filter(*filters).order_by(Viagem.data_hora.desc()).paginate(page=page, per_page=per_page, error_out=False)
    viagens = [v.to_dict() for v in viagens_pagination.items]
    return jsonify({
        "viagens": viagens,
        "total": viagens_pagination.total,
        "pages": viagens_pagination.pages,
        "current_page": viagens_pagination.page
    }), 200

@mobilidade_bp.route('/viagens/<uuid:viagem_id>', methods=['GET'])
@jwt_required()
def get_viagem(viagem_id):
    viagem = Viagem.query.get_or_404(str(viagem_id))
    return jsonify(viagem.to_dict()), 200

@mobilidade_bp.route('/viagens/<uuid:viagem_id>', methods=['PUT'])
@jwt_required()
def update_viagem(viagem_id):
    if not is_admin():
         return jsonify({"msg": "Acesso não autorizado"}), 403
    viagem = Viagem.query.get_or_404(str(viagem_id))
    data = request.get_json()
    try:
        for key, value in data.items():
            if key == "data_hora": # Converter string de data para datetime
                setattr(viagem, key, datetime.fromisoformat(value))
            elif hasattr(viagem, key):
                setattr(viagem, key, value)
        db.session.commit()
        return jsonify(viagem.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Erro ao atualizar viagem", "error": str(e)}), 400

@mobilidade_bp.route('/viagens/<uuid:viagem_id>', methods=['DELETE'])
@jwt_required()
def delete_viagem(viagem_id):
    if not is_admin():
         return jsonify({"msg": "Acesso não autorizado"}), 403
    viagem = Viagem.query.get_or_404(str(viagem_id))
    db.session.delete(viagem)
    db.session.commit()
    return jsonify({"msg": "Viagem deletada"}), 200

# --- Análises ---
@mobilidade_bp.route('/analysis/passengers_by_neighborhood', methods=['GET'])
@jwt_required()
def get_passengers_by_neighborhood_from_db():
    try:
        # Consulta agregada ao banco de dados
        bairro_data = db.session.query(
            Viagem.bairro_origem.label('bairro'), # ou bairro_destino, ou combinar
            func.sum(Viagem.passageiros).label('total_passageiros')
        ).group_by(Viagem.bairro_origem).order_by(func.sum(Viagem.passageiros).desc()).all()

        if not bairro_data:
            return jsonify({"msg": "Nenhum dado de mobilidade encontrado para análise"}), 404

        bairros = [item.bairro for item in bairro_data]
        passageiros = [item.total_passageiros for item in bairro_data]

        # Gerar gráfico
        plt.figure(figsize=(12, 7))
        plt.bar(bairros, passageiros)
        plt.title('Total de Passageiros por Bairro de Origem em Teresina (DB)')
        plt.xlabel('Bairro')
        plt.ylabel('Total de Passageiros')
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

        img_io = BytesIO()
        plt.savefig(img_io, format='png')
        img_io.seek(0)
        plt.close()

        # Salvar no MinIO (usando app.minio_client e app.minio_bucket_name)
        minio = current_app.minio_client
        bucket_name = current_app.minio_bucket_name
        object_name = 'passageiros_por_bairro_db.png'

        if not minio:
             return jsonify({"error": "Cliente MinIO não inicializado"}), 500

        minio.put_object(
            bucket_name,
            object_name,
            img_io,
            length=img_io.getbuffer().nbytes,
            content_type='image/png'
        )
        presigned_url = minio.presigned_get_object(bucket_name, object_name)
        
        return jsonify({
            "message": "Análise concluída e gráfico gerado a partir do banco de dados.",
            "plot_url": presigned_url,
            "data": [{"bairro": b, "passageiros": p} for b, p in zip(bairros, passageiros)]
        })
    except Exception as e:
        current_app.logger.error(f"Erro na análise: {e}", exc_info=True)
        return jsonify({"msg": "Erro interno ao processar a análise", "error": str(e)}), 500

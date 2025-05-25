from flask import Blueprint, request, jsonify
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"msg": "Faltam campos obrigatórios (username, email, password)"}), 400

    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({"msg": "Usuário ou email já existe"}), 409

    new_user = User(username=username, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "Usuário registrado com sucesso!"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username_or_email = data.get('username_or_email')
    password = data.get('password')

    if not username_or_email or not password:
        return jsonify({"msg": "Faltam campos (username_or_email, password)"}), 400

    user = User.query.filter((User.username == username_or_email) | (User.email == username_or_email)).first()

    if user and user.check_password(password):
        access_token = create_access_token(identity={"id": str(user.id), "username": user.username, "is_admin": user.is_admin})
        return jsonify(access_token=access_token, user={"id": str(user.id), "username": user.username, "email": user.email, "is_admin": user.is_admin}), 200
    else:
        return jsonify({"msg": "Credenciais inválidas"}), 401

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    current_user_identity = get_jwt_identity()
    user = User.query.get(current_user_identity['id'])
    if not user:
        return jsonify({"msg": "Usuário não encontrado"}), 404
    return jsonify({
        "id": str(user.id),
        "username": user.username,
        "email": user.email,
        "is_admin": user.is_admin
    }), 200

import os
from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from minio import Minio
from minio.error import S3Error
from config import Config
from models import db
# Importar Blueprints (rotas)
from routes.auth_routes import auth_bp
from routes.mobilidade_routes import mobilidade_bp
from routes.admin_routes import admin_bp # Para carregar CSV, por exemplo

# Inicializa cliente MinIO (pode ser encapsulado em um serviço)
minio_client = None
try:
    minio_client = Minio(
        Config.MINIO_ENDPOINT,
        access_key=Config.MINIO_ACCESS_KEY,
        secret_key=Config.MINIO_SECRET_KEY,
        secure=False # Mude para True se usar HTTPS
    )
    # Cria o bucket se não existir
    if not minio_client.bucket_exists(Config.MINIO_BUCKET_NAME):
        minio_client.make_bucket(Config.MINIO_BUCKET_NAME)
except S3Error as e:
    print(f"ALERTA: Erro ao conectar ou criar bucket no MinIO: {e}. Funcionalidades do MinIO podem estar indisponíveis.")
except Exception as e:
    print(f"ALERTA: Ocorreu um erro inesperado ao inicializar o MinIO: {e}")

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    Migrate(app, db) # Inicializa Flask-Migrate
    JWTManager(app)  # Inicializa Flask-JWT-Extended

    # Disponibiliza o cliente minio para os blueprints se necessário (ou use services)
    app.minio_client = minio_client
    app.minio_bucket_name = Config.MINIO_BUCKET_NAME

    # Registrar Blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(mobilidade_bp, url_prefix='/api/mobilidade')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')


    @app.route('/')
    def health_check():
        bucket_status = "Não verificado (MinIO indisponível)"
        if app.minio_client:
            try:
                bucket_status = "Existe" if app.minio_client.bucket_exists(app.minio_bucket_name) else "Não Existe"
            except Exception:
                bucket_status = "Erro ao verificar"
        return {
            "status": "API funcionando!",
            "minio_bucket_status": bucket_status,
            "database_status": "Conectado" if db.engine.connect() else "Erro de conexão" # Teste simples
        }

    return app

# Para executar com 'flask run' (após setar FLASK_APP e FLASK_DEBUG no .env)
# ou para Gunicorn/uWSGI
# app = create_app()

# Se for executar diretamente com 'python app.py'
if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all() # CUIDADO: Em produção, use Flask-Migrate
    app.run(host='0.0.0.0', port=5000)

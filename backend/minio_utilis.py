import os
from minio import Minio
from minio.error import S3Error
from dotenv import load_dotenv

load_dotenv() # Carrega variáveis de .env se estiver usando python-dotenv para dev local

MINIO_ENDPOINT = os.getenv("MINIO_URL", "localhost:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "admin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "admin123")
MINIO_SECURE = os.getenv("MINIO_SECURE", "False").lower() == "true"

# Variáveis de ambiente passadas pelo docker-compose.yml
# MINIO_ENDPOINT = os.environ.get('MINIO_ENDPOINT', 'minio:9000') # Nome do serviço no docker-compose
# MINIO_ACCESS_KEY = os.environ.get('MINIO_ACCESS_KEY', 'your_minio_access_key')
# MINIO_SECRET_KEY = os.environ.get('MINIO_SECRET_KEY', 'your_minio_secret_key')
# MINIO_SECURE = os.environ.get('MINIO_SECURE', 'False').lower() == 'true'

try:
    client = Minio(
        MINIO_ENDPOINT,
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        secure=MINIO_SECURE
    )
except Exception as e:
    print(f"Erro ao inicializar cliente MinIO: {e}")
    client = None

def ensure_bucket_exists(bucket_name):
    if client:
        try:
            if not client.bucket_exists(bucket_name):
                client.make_bucket(bucket_name)
                print(f"Bucket '{bucket_name}' criado com sucesso.")
            else:
                print(f"Bucket '{bucket_name}' já existe.")
        except S3Error as e:
            print(f"Erro ao verificar/criar bucket '{bucket_name}': {e}")
            return False
        return True
    return False

def upload_to_minio(bucket_name, object_name, data_stream, data_length, content_type='application/octet-stream'):
    if client and ensure_bucket_exists(bucket_name):
        try:
            client.put_object(
                bucket_name,
                object_name,
                data_stream,
                length=data_length,
                content_type=content_type
            )
            print(f"Arquivo '{object_name}' enviado para o bucket '{bucket_name}'.")
            return True
        except S3Error as e:
            print(f"Erro ao enviar arquivo para MinIO: {e}")
    return False

def get_presigned_url_for_object(bucket_name, object_name):
    if client:
        try:
            url = client.presigned_get_object(bucket_name, object_name)
            return url
        except S3Error as e:
            print(f"Erro ao gerar URL pré-assinada: {e}")
    return None
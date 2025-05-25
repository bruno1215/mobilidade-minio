from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID # Para IDs únicos
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False) # Aumentado para 256
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Viagem(db.Model):
    __tablename__ = "viagens"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    data_hora = db.Column(db.DateTime, nullable=False, index=True)
    linha_onibus = db.Column(db.String(50))
    bairro_origem = db.Column(db.String(100), index=True)
    bairro_destino = db.Column(db.String(100), index=True)
    passageiros = db.Column(db.Integer)
    lat_origem = db.Column(db.Float)
    lon_origem = db.Column(db.Float)
    lat_destino = db.Column(db.Float)
    lon_destino = db.Column(db.Float)

    def to_dict(self):
        return {
            "id": str(self.id),
            "data_hora": self.data_hora.isoformat(),
            "linha_onibus": self.linha_onibus,
            "bairro_origem": self.bairro_origem,
            "bairro_destino": self.bairro_destino,
            "passageiros": self.passageiros,
            "lat_origem": self.lat_origem,
            "lon_origem": self.lon_origem,
            "lat_destino": self.lat_destino,
            "lon_destino": self.lon_destino,
        }

    def __repr__(self):
        return f'<Viagem {self.id} - Linha {self.linha_onibus}>'

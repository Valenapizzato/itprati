from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()
db = SQLAlchemy()

def init_app(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

class Estagiario(db.Model):
    __tablename__ = 'estagiarios'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    data_nascimento = db.Column(db.String(20))
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)  # NOVO
    telefone = db.Column(db.String(20))
    cidade_estado = db.Column(db.String(100))
    curso = db.Column(db.String(100))
    instituicao = db.Column(db.String(100))
    disponibilidade = db.Column(db.String(200))
    github = db.Column(db.String(200))
    habilidades = db.Column(db.String(300))
    area_interesse = db.Column(db.String(200))
    experiencias = db.Column(db.Text)
    soft_skills = db.Column(db.Text)
    endereco = db.Column(db.String(200))
    formato_trabalho = db.Column(db.String(50))
    quer_consultoria = db.Column(db.String(10))


class Empresa(db.Model):
    __tablename__ = 'empresas'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    cnpj = db.Column(db.String(20), unique=True)
    responsavel = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True)
    senha = db.Column(db.String(200), nullable=False)  # NOVO
    telefone = db.Column(db.String(20))
    areas_interesse = db.Column(db.String(200))
    requisitos = db.Column(db.Text)
    tipo_contrato = db.Column(db.String(100))
    beneficios = db.Column(db.String(200))
    cursos_exigidos = db.Column(db.String(200))
    endereco = db.Column(db.String(200))
    modelo_servico = db.Column(db.String(50))

class Candidatura(db.Model):
    __tablename__ = 'candidaturas'

    id = db.Column(db.Integer, primary_key=True)
    estudante_id = db.Column(db.Integer, db.ForeignKey('estagiarios.id'), nullable=False)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresas.id'), nullable=False)
    status = db.Column(db.String(50), default='Em análise')

    estudante = db.relationship('Estagiario', backref='candidaturas')
    empresa = db.relationship('Empresa', backref='candidaturas_recebidas')


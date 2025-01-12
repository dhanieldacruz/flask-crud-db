import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Inicializa o banco de dados
db = SQLAlchemy()

def create_app(config_name='default'):
    app = Flask(__name__)

    # Verifica se o diretório 'instance' existe, caso contrário, cria
    if not os.path.exists(app.instance_path):
        os.makedirs(app.instance_path)
    
    # Caminho absoluto para o banco de dados
    db_path = os.path.join(app.instance_path, 'database.db')
    print(f"Database path: {db_path}")  # Imprime o caminho do banco de dados

    # Configuração do banco de dados SQLite para a aplicação
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TESTING'] = True  # Configuração para testes
    db.init_app(app)

    # Importa e inicializa as rotas
    from .routes import init_routes
    init_routes(app)

    # Criar as tabelas do banco de dados (apenas para o primeiro uso)
    with app.app_context():
        db.create_all()

    return app








from app import create_app
from app import db
import pytest


@pytest.fixture
def app():
    """Cria uma instância do app para os testes."""
    app = create_app()
    app.config.update({
        "TESTING": True,  # Configura o modo de teste
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  # Banco de dados na memória
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    })

    # Configura o banco de dados em memória
    with app.app_context():
        db.create_all()

    yield app

    # Limpa o banco de dados após os testes
    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Fornece um cliente de teste para fazer requisições."""
    return app.test_client()


def test_app_creation(app):
    """Teste básico para verificar se a aplicação Flask é criada corretamente."""
    assert app is not None
    assert app.config["TESTING"] is True


def test_database_creation(app):
    """Verifica se o banco de dados é criado corretamente."""
    with app.app_context():
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        assert len(tables) > 0  # Garante que existem tabelas no banco


def test_home_route(client):
    """Testa uma rota simples (substitua pela sua rota real)."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Bem-vindo" in response.data

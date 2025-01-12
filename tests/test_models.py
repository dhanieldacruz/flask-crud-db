import pytest
from app import create_app, db
from app.models import User  # Certifique-se de importar a classe User corretamente

@pytest.fixture
def app():
    # Configuração do app para testes
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Usando banco de dados em memória para testes
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    with app.app_context():
        db.create_all()  # Cria todas as tabelas antes de rodar os testes
    yield app
    with app.app_context():
        db.drop_all()  # Limpa as tabelas após os testes

def test_user_model(app):
    user = User(name='John Doe', email='john@example.com')
    with app.app_context():
        db.session.add(user)
        db.session.commit()  # Insere no banco de dados
        
        # Recarrega o objeto 'user' para garantir que o ID tenha sido atribuído
        db.session.refresh(user)

        # Verifica se o ID foi atribuído corretamente, dentro do contexto da sessão
        assert user.id is not None
        assert user.name == 'John Doe'
        assert user.email == 'john@example.com'



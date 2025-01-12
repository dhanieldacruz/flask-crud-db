import pytest
from app import create_app, db
from app.models import User

@pytest.fixture
def app():
    """Cria uma instância do app para os testes."""
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  # Usando banco de dados em memória para os testes
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    })

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


# Teste para a criação de um usuário (Create)
def test_create_user(client):
    """Teste para verificar a criação de um usuário."""
    response = client.post('/users', json={'name': 'João Silva', 'email': 'joao@exemplo.com'})
    data = response.get_json()

    assert response.status_code == 201
    assert data['name'] == 'João Silva'
    assert data['email'] == 'joao@exemplo.com'


# Teste para obter todos os usuários (Read)
def test_get_users(client):
    """Teste para verificar se é possível obter todos os usuários."""
    client.post('/users', json={'name': 'João Silva', 'email': 'joao@exemplo.com'})
    response = client.get('/users')
    data = response.get_json()

    assert response.status_code == 200
    assert len(data) > 0
    assert data[0]['name'] == 'João Silva'
    assert data[0]['email'] == 'joao@exemplo.com'


# Teste para obter um usuário específico (Read)
def test_get_user(client):
    """Teste para verificar a leitura de um usuário pelo ID."""
    response_create = client.post('/users', json={'name': 'Maria Oliveira', 'email': 'maria@exemplo.com'})
    user_id = response_create.get_json()['id']

    response = client.get(f'/users/{user_id}')
    data = response.get_json()

    assert response.status_code == 200
    assert data['name'] == 'Maria Oliveira'
    assert data['email'] == 'maria@exemplo.com'


# Teste para atualizar um usuário (Update)
def test_update_user(client):
    """Teste para verificar a atualização de um usuário."""
    response_create = client.post('/users', json={'name': 'Carlos Souza', 'email': 'carlos@exemplo.com'})
    user_id = response_create.get_json()['id']

    response = client.put(f'/users/{user_id}', json={'name': 'Carlos Silva', 'email': 'carlos@novoemail.com'})
    data = response.get_json()

    assert response.status_code == 200
    assert data['name'] == 'Carlos Silva'
    assert data['email'] == 'carlos@novoemail.com'


# Teste para excluir um usuário (Delete)
def test_delete_user(client):
    """Teste para verificar a exclusão de um usuário."""
    response_create = client.post('/users', json={'name': 'Ana Costa', 'email': 'ana@exemplo.com'})
    user_id = response_create.get_json()['id']

    response = client.delete(f'/users/{user_id}')
    data = response.get_json()

    assert response.status_code == 200
    assert data['message'] == 'Usuário deletado com sucesso.'


# Teste para tentar excluir um usuário que não existe
def test_delete_nonexistent_user(client):
    """Teste para tentar excluir um usuário inexistente."""
    response = client.delete('/users/9999')
    data = response.get_json()

    assert response.status_code == 404
    assert data['error'] == 'Usuário não encontrado.'

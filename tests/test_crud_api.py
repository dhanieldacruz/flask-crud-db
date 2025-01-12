import pytest
from unittest.mock import patch, MagicMock
import sys
import os
import requests

project_path = os.path.abspath(os.path.join(os.getcwd(), ".."))  
sys.path.append(project_path)

from utils.crud_api import UserAPI

# URL fictícia para os testes
BASE_URL = "http://localhost:5000/users"


@pytest.fixture
def user_api():
    return UserAPI(BASE_URL)


# Teste para a criação de um usuário
@patch('requests.post')
def test_create_user(mock_post, user_api):
    # Dados do usuário
    user_data = {"name": "John Doe", "email": "john@example.com"}
    
    # Mock da resposta da requisição
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {"id": 1, "name": "John Doe", "email": "john@example.com"}
    mock_post.return_value = mock_response
    
    # Chama o método para criar o usuário
    user_api.create_user(user_data['name'], user_data['email'])
    
    # Verifica se o método post foi chamado com os parâmetros corretos
    mock_post.assert_called_once_with(BASE_URL, json=user_data)


# Teste para obter todos os usuários
@patch('requests.get')
def test_get_all_users(mock_get, user_api):
    # Mock da resposta da requisição
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {"id": 1, "name": "John Doe", "email": "john@example.com"},
        {"id": 2, "name": "Jane Doe", "email": "jane@example.com"}
    ]
    mock_get.return_value = mock_response
    
    # Chama o método para obter todos os usuários
    user_api.get_all_users()
    
    # Verifica se o método get foi chamado com a URL correta
    mock_get.assert_called_once_with(BASE_URL)


# Teste para obter um usuário pelo ID
@patch('requests.get')
def test_get_user_by_id(mock_get, user_api):
    # Mock da resposta da requisição
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"id": 1, "name": "John Doe", "email": "john@example.com"}
    mock_get.return_value = mock_response
    
    # Chama o método para obter um usuário
    user_api.get_user_by_id(1)
    
    # Verifica se o método get foi chamado com o ID correto
    mock_get.assert_called_once_with(f"{BASE_URL}/1")


# Teste para atualizar um usuário
@patch('requests.put')
def test_update_user(mock_put, user_api):
    # Dados do usuário a serem atualizados
    user_data = {"name": "John Updated", "email": "john.updated@example.com"}
    
    # Mock da resposta da requisição
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"id": 1, "name": "John Updated", "email": "john.updated@example.com"}
    mock_put.return_value = mock_response
    
    # Chama o método para atualizar o usuário
    user_api.update_user(1, user_data['name'], user_data['email'])
    
    # Verifica se o método put foi chamado com os parâmetros corretos
    mock_put.assert_called_once_with(f"{BASE_URL}/1", json=user_data)


# Teste para excluir um usuário
@patch('requests.delete')
def test_delete_user(mock_delete, user_api):
    # Mock da resposta da requisição
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_delete.return_value = mock_response
    
    # Chama o método para excluir o usuário
    user_api.delete_user(1)
    
    # Verifica se o método delete foi chamado com o ID correto
    mock_delete.assert_called_once_with(f"{BASE_URL}/1")

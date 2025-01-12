from flask import request, jsonify
from . import db  
from .models import User  

def init_routes(app):
    # Rota para criar um novo usuário (Create)
    @app.route('/users', methods=['POST'])
    def create_user():
        data = request.get_json()
        if not data or not data.get('name') or not data.get('email'):
            return jsonify({"error": "Nome e e-mail são obrigatórios."}), 400

        new_user = User(name=data['name'], email=data['email'])
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'id': new_user.id, 'name': new_user.name, 'email': new_user.email}), 201

    # Rota para obter todos os usuários (Read)
    @app.route('/users', methods=['GET'])
    def get_users():
        users = User.query.all()
        result = [{'id': user.id, 'name': user.name, 'email': user.email} for user in users]
        return jsonify(result), 200

    # Rota para obter um usuário pelo ID (Read)
    @app.route('/users/<int:id>', methods=['GET'])
    def get_user(id):
        user = User.query.get(id)
        if not user:
            return jsonify({"error": "Usuário não encontrado."}), 404
        return jsonify({'id': user.id, 'name': user.name, 'email': user.email}), 200

    # Rota para atualizar um usuário pelo ID (Update)
    @app.route('/users/<int:id>', methods=['PUT'])
    def update_user(id):
        user = User.query.get(id)
        if not user:
            return jsonify({"error": "Usuário não encontrado."}), 404

        data = request.get_json()
        user.name = data.get('name', user.name)
        user.email = data.get('email', user.email)

        db.session.commit()

        return jsonify({'id': user.id, 'name': user.name, 'email': user.email}), 200

    # Rota para excluir um usuário pelo ID (Delete)
    @app.route('/users/<int:id>', methods=['DELETE'])
    def delete_user(id):
        user = User.query.get(id)
        if not user:
            return jsonify({"error": "Usuário não encontrado."}), 404

        db.session.delete(user)
        db.session.commit()

        return jsonify({"message": "Usuário deletado com sucesso."}), 200

    # Rota inicial
    @app.route('/')
    def home():
        return "Bem-vindo à aplicação CRUD de usuários!"

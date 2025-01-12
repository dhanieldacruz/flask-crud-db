import requests

class UserAPI:
    def __init__(self, url):
        self.url = url

    # 1. Criar um Novo Usuário (POST)
    def create_user(self, name, email):
        user_data = {
            "name": name,
            "email": email
        }

        try:
            response = requests.post(self.url, json=user_data)
            if response.status_code == 201:
                print(f"Usuário criado com sucesso: {response.json()}")
            else:
                print(f"Erro ao criar usuário: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Erro ao fazer a requisição: {e}")

    # 2. Obter Todos os Usuários (GET)
    def get_all_users(self):
        try:
            response = requests.get(self.url)
            if response.status_code == 200:
                users = response.json()
                print("Usuários:")
                for user in users:
                    print(f"ID: {user['id']}, Name: {user['name']}, Email: {user['email']}")
            else:
                print(f"Erro ao obter usuários: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Erro ao fazer a requisição: {e}")

    # 3. Obter um Usuário pelo ID (GET)
    def get_user_by_id(self, user_id):
        try:
            response = requests.get(f"{self.url}/{user_id}")
            if response.status_code == 200:
                user = response.json()
                print(f"Usuário encontrado: ID: {user['id']}, Name: {user['name']}, Email: {user['email']}")
            else:
                print(f"Erro ao obter usuário: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Erro ao fazer a requisição: {e}")

    # 4. Atualizar um Usuário pelo ID (PUT)
    def update_user(self, user_id, name=None, email=None):
        user_data = {}
        if name:
            user_data['name'] = name
        if email:
            user_data['email'] = email

        try:
            response = requests.put(f"{self.url}/{user_id}", json=user_data)
            if response.status_code == 200:
                user = response.json()
                print(f"Usuário atualizado: ID: {user['id']}, Name: {user['name']}, Email: {user['email']}")
            else:
                print(f"Erro ao atualizar usuário: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Erro ao fazer a requisição: {e}")

    # 5. Excluir um Usuário pelo ID (DELETE)
    def delete_user(self, user_id):
        try:
            response = requests.delete(f"{self.url}/{user_id}")
            if response.status_code == 200:
                print(f"Usuário ID {user_id} deletado com sucesso.")
            else:
                print(f"Erro ao excluir usuário: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Erro ao fazer a requisição: {e}")

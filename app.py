from app import create_app  # Importa a função que cria o app Flask

if __name__ == '__main__':
    app = create_app()  # Cria o app Flask
    app.run(debug=True)  # Inicia o servidor Flask
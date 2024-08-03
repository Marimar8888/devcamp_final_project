from app import create_app

app = create_app()

@app.route('/') # Creo la ruta de acceso a nuestra aplicación con el decorador
def hello():
    return "Hey Flask"

if __name__ == '__main__':
    app.run(debug=True)
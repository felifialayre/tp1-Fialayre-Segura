import logging
from flask import Flask, request, jsonify
from models import db, Jugador, TipoPartida, Partida
from sqlalchemy.engine.url import URL

app = Flask(__name__)
port = 5000

# Configurar el logging
logging.basicConfig(level=logging.DEBUG)

# Define the database connection details
db_config = {
    'drivername': 'postgresql',
    'username': 'juanasegura',
    'password': 'juanasegura',
    'host': 'localhost',
    'port': '5432',
    'database': 'falta_envido'
}

# Create the database URL
db_url = URL.create(**db_config)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route("/")
def hello():
    return 'hello'

if __name__ == '__main__':
    logging.debug('Starting server...')
    with app.app_context():
        try:
            db.create_all()
            logging.debug('Tables created successfully')
        except Exception as e:
            logging.error('Error creating tables: %s', e)
    app.run(host='0.0.0.0', debug=True, port=port)
    logging.debug('Server started...')
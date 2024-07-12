import logging
from flask import Flask, request, jsonify
from models import db, Jugador, TipoPartida, Partida
from sqlalchemy.engine.url import URL
from sqlalchemy import func
from flask_cors import CORS

app = Flask(__name__)
port = 5000
CORS(app)

# Configurar el logging
logging.basicConfig(level=logging.DEBUG)

# Detalles de la conexion
db_config = {
    'drivername': 'postgresql',
    'username': 'juanasegura',
    'password': 'juanasegura',
    'host': 'localhost',
    'port': '5432',
    'database': 'falta_envido'
}

# Crea URL de la DB
db_url = URL.create(**db_config)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route("/")
def hello():
    return 'hello'

@app.route('/home')
def return_players():
    contenido = []
    count_jugadores = db.session.query(func.count(Jugador.id)).scalar()
    for i in range (1, count_jugadores+1):
        current = db.session.query(Jugador).filter_by(id=i).first()
        current_dic = {
            'id' : current.id,
            'nombre' : current.nombre,
            'avatar' : current.avatar,
            'apodo' : current.apodo
        }
        contenido.append(current_dic)
    return contenido

@app.route('/players/<player_id>')
def return_player_by_id(player_id):
    jugador = db.session.query(Jugador).filter_by(id=player_id).first()
    return {
        'id' : jugador.id,
        'nombre' : jugador.nombre,
        'avatar' : jugador.avatar,
        'edad' : jugador.edad,
        'ganadas' : jugador.edad,
        'perdidas' : jugador.perdidas,
        'apodo' : jugador.apodo,
    }

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
import logging
import datetime
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
    jugadores = Jugador.query.all()
    for jugador in jugadores:
        jugador_dic = {
            'id': jugador.id,
            'nombre': jugador.nombre,
            'avatar': jugador.avatar,
            'apodo': jugador.apodo
        }
        contenido.append(jugador_dic)
    return jsonify(contenido)

@app.route("/home", methods=["POST"])
def create_player():
    try:
        data = request.json
        nombre = data.get('nombre')
        apodo = data.get('apodo')
        edad = data.get('edad')
        avatar = data.get('avatar')
        
        nuevo_jugador = Jugador(
            nombre=nombre, 
            apodo=apodo, 
            edad=edad, 
            ganadas=0, 
            perdidas=0, 
            avatar=avatar
        )
        db.session.add(nuevo_jugador)
        db.session.commit()

        return jsonify({
            'jugador': {
                'id': nuevo_jugador.id,
                'nombre': nuevo_jugador.nombre,
                'apodo': nuevo_jugador.apodo,
                'edad': nuevo_jugador.edad,
                'ganadas': nuevo_jugador.ganadas,
                'perdidas': nuevo_jugador.perdidas,
                'avatar': nuevo_jugador.avatar,
                'fecha_creacion': nuevo_jugador.fecha_creacion
            }
        }), 201

    except Exception as e:
        logging.error(f"Error creating player: {e}")
        return jsonify({'message': f'No se pudo crear el jugador: {e}'}), 500



@app.route('/player/<player_id>')
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
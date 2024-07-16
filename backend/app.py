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
    'username': 'felipefialayre',
    'password': 'felipefialayre',
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

@app.route('/players/<player_id>')
def return_player_by_id(player_id):
    jugador = db.session.query(Jugador).filter_by(id=player_id).first()
    return {
        'id' : jugador.id,
        'nombre' : jugador.nombre,
        'avatar' : jugador.avatar,
        'edad' : jugador.edad,
        'ganadas' : jugador.ganadas,
        'perdidas' : jugador.perdidas,
        'apodo' : jugador.apodo,
    }

@app.route('/players/<player_id>', methods = ["DELETE"])
def delete_character_by_id(player_id):
    jugador = db.session.query(Jugador).filter_by(id=player_id).first()
    if jugador is not None:
       db.session.delete(jugador)
       db.session.commit()
       return jsonify({"message": True}), 200
    else:
       print(f"No se encontró ningún jugador con ID {player_id}.")
       return jsonify({"message": False}), 500
    
    
@app.route('/edit/<player_id>', methods = ["PUT"]) 
def edit_character_by_id(player_id):
    try:
        
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "El cuerpo de la solicitud debe ser JSON"}), 400
        nombre = data.get('nombre')
        apodo = data.get('apodo')
        edad = data.get('edad')
        avatar = data.get('avatar')
            
        jugador = Jugador.query.get(player_id)
        
        if not jugador:
            return jsonify({"error": "Jugador no encontrado"}), 404
           
        if nombre is not None:
            jugador.nombre = nombre
        if apodo is not None:
            jugador.apodo = apodo
        if edad is not None:
            jugador.edad = edad
        if avatar is not None:
            jugador.avatar = avatar

        db.session.commit()
        
        return jsonify({"mensaje" : True})

    except Exception as e:
        logging.error(f"Error creating player: {e}")
        return jsonify({'message': False}), 500


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
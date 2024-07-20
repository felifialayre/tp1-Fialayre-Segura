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

@app.route("/home", methods=["POST"])
def create_player():
    try:
        data = request.json
        nombre = data.get('nombre')
        apodo = data.get('apodo')
        edad = data.get('edad')
        avatar = data.get('avatar')

        ultimo_jugador = db.session.query(Jugador).order_by(Jugador.id.desc()).first()
        nuevo_id = 1 if ultimo_jugador is None else ultimo_jugador.id + 1
        
        nuevo_jugador = Jugador(
            id=nuevo_id,
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
       Partida.query.filter_by(jugador_id=player_id).delete()
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

@app.route('/players/<player_id>/partidas')
def get_partidas_by_player_id(player_id):
    try:
        partidas = db.session.query(Partida, TipoPartida).join(TipoPartida).filter(Partida.jugador_id == player_id).all()
        if not partidas:
            return jsonify({"message": "No se encontraron partidas"}), 404
        
        partidas_list = [
            {
                'id': partida.Partida.id,
                'tipo_partida_id': partida.Partida.tipo_partida_id,
                'cant_jugadores': partida.TipoPartida.cant_jugadores,
                'flor': partida.TipoPartida.flor,
                'max_puntos': partida.TipoPartida.max_puntos,
                'ganada': partida.Partida.ganada,
                'fecha_creacion': partida.Partida.fecha_creacion
            }
            for partida in partidas
        ]
        return jsonify(partidas_list)
    except Exception as e:
        logging.error(f"Error al buscar partidas para el jugador {player_id}: {e}")
        return jsonify({"message": "Error al buscar partidas"}), 500

@app.route('/players/<int:player_id>/partidas', methods=['POST'])
def agregar_partida(player_id):
    try:
        data = request.get_json()
        tipo_partida_id = data.get('tipo_partida_id')
        resultado = data.get('resultado')

        ultima_partida = db.session.query(Partida).order_by(Partida.id.desc()).first()
        nuevo_id = 1 if ultima_partida is None else ultima_partida.id + 1

        nueva_partida = Partida(
            id=nuevo_id,  
            jugador_id=player_id,
            tipo_partida_id=tipo_partida_id,
            ganada=resultado,
            fecha_creacion=datetime.datetime.now()
        )

        db.session.add(nueva_partida)

        jugador = db.session.query(Jugador).filter_by(id=player_id).first()
        if resultado:
            jugador.ganadas += 1
        else:
            jugador.perdidas += 1

        db.session.commit()

        return jsonify({"message": "Partida agregada correctamente"}), 201

    except Exception as e:
        logging.error(f"Error al agregar partida para el jugador {player_id}: {e}")
        return jsonify({"error": str(e)}), 500
 
@app.route('/partidas/<int:partida_id>', methods=['DELETE'])
def delete_partida_by_id(partida_id):
    try:
        partida = db.session.query(Partida).filter_by(id=partida_id).first()
        if not partida:
            return jsonify({"message": "Partida no encontrada"}), 404
        
        jugador = db.session.query(Jugador).filter_by(id=partida.jugador_id).first()
        if partida.ganada:
            jugador.ganadas -= 1
        else:
            jugador.perdidas -= 1

        db.session.delete(partida)
        db.session.commit()
        return jsonify({"message": True}), 200
    
    except Exception as e:
        logging.error(f"Error al eliminar partida: {e}")
        return jsonify({"message": "Error al eliminar partida"}), 500



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
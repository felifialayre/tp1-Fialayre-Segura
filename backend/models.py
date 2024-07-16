import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Jugador(db.Model):
    __tablename__ = 'jugadores'
    id = db.Column (db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    apodo = db.Column(db.String(255), nullable=False)
    edad = db.Column (db.Integer, nullable=False)
    ganadas = db.Column(db.Integer, nullable=False, default=0)
    perdidas = db.Column(db.Integer, nullable=False, default=0)
    avatar = db.Column (db.Integer, default=1)
    fecha_creacion = db.Column (db.DateTime, default=datetime.datetime.now())

class TipoPartida (db.Model):
    __tablename__='tipos_partida'
    id = db.Column(db.Integer, primary_key=True)
    cant_jugadores = db.Column (db.Integer, nullable=False)
    apodo = db.Column(db.Boolean, default = False)
    max_puntos = db.Column (db.Integer, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.datetime.now())

class Partida (db.Model):
    __tablename__ = 'partidas'
    id = db.Column(db.Integer, primary_key=True)
    tipo_partida_id = db.Column (db.Integer, db.ForeignKey('tipos_partida.id'))
    jugador_id = db.Column (db.Integer, db.ForeignKey('tipos_partida.id'))
    fecha_creacion = db.Column(db.DateTime, default=datetime.datetime.now())
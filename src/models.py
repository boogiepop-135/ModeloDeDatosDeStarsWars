from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    fecha_subscripcion = db.Column(db.DateTime, default=datetime.utcnow)
    
    favoritos = db.relationship('Favorito', backref='usuario', lazy=True, cascade='all, delete-orphan')

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "fecha_subscripcion": self.fecha_subscripcion
        }

class Personaje(db.Model):
    __tablename__ = 'personaje'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    especie = db.Column(db.String(50))
    genero = db.Column(db.String(20))
    afiliacion = db.Column(db.String(50))
    descripcion = db.Column(db.Text)
    
    favoritos = db.relationship('Favorito', backref='personaje', lazy=True, cascade='all, delete-orphan')

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "especie": self.especie,
            "genero": self.genero,
            "afiliacion": self.afiliacion,
            "descripcion": self.descripcion
        }

class Planeta(db.Model):
    __tablename__ = 'planeta'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    clima = db.Column(db.String(50))
    terreno = db.Column(db.String(50))
    poblacion = db.Column(db.Integer)
    descripcion = db.Column(db.Text)
    
    favoritos = db.relationship('Favorito', backref='planeta', lazy=True, cascade='all, delete-orphan')

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "clima": self.clima,
            "terreno": self.terreno,
            "poblacion": self.poblacion,
            "descripcion": self.descripcion
        }

class Favorito(db.Model):
    __tablename__ = 'favorito'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    personaje_id = db.Column(db.Integer, db.ForeignKey('personaje.id'), nullable=True)
    planeta_id = db.Column(db.Integer, db.ForeignKey('planeta.id'), nullable=True)
    fecha_agregado = db.Column(db.DateTime, default=datetime.utcnow)

    def serialize(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "personaje_id": self.personaje_id,
            "planeta_id": self.planeta_id,
            "fecha_agregado": self.fecha_agregado
        }
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import db, Usuario, Personaje, Planeta, Favorito
from flask_cors import CORS
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///starwars.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)

# Inicialización de la base de datos
db.init_app(app)
migrate = Migrate(app, db)

# Configuración del admin
admin = Admin(app, name='StarWars Admin', template_mode='bootstrap3')
admin.add_view(ModelView(Usuario, db.session))
admin.add_view(ModelView(Personaje, db.session))
admin.add_view(ModelView(Planeta, db.session))
admin.add_view(ModelView(Favorito, db.session))

# Endpoints para Personajes
@app.route('/people', methods=['GET'])
def get_all_people():
    personajes = Personaje.query.all()
    return jsonify([personaje.serialize() for personaje in personajes]), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    personaje = Personaje.query.get(people_id)
    if personaje:
        return jsonify(personaje.serialize()), 200
    return jsonify({"message": "Personaje no encontrado"}), 404

# Endpoints para Planetas
@app.route('/planets', methods=['GET'])
def get_all_planets():
    planetas = Planeta.query.all()
    return jsonify([planeta.serialize() for planeta in planetas]), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planeta = Planeta.query.get(planet_id)
    if planeta:
        return jsonify(planeta.serialize()), 200
    return jsonify({"message": "Planeta no encontrado"}), 404

# Endpoints para Usuarios
@app.route('/users', methods=['GET'])
def get_all_users():
    usuarios = Usuario.query.all()
    return jsonify([usuario.serialize() for usuario in usuarios]), 200

# Endpoints para Favoritos
@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    # Usaremos el primer usuario como ejemplo
    usuario = Usuario.query.first()
    if not usuario:
        return jsonify({"message": "Usuario no encontrado"}), 404
    
    favoritos = Favorito.query.filter_by(usuario_id=usuario.id).all()
    
    result = {
        "planetas": [f.planeta.serialize() for f in favoritos if f.planeta],
        "personajes": [f.personaje.serialize() for f in favoritos if f.personaje]
    }
    
    return jsonify(result), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    usuario = Usuario.query.first()
    planeta = Planeta.query.get(planet_id)
    
    if not usuario or not planeta:
        return jsonify({"message": "Usuario o planeta no encontrado"}), 404
    
    existe = Favorito.query.filter_by(usuario_id=usuario.id, planeta_id=planet_id).first()
    if existe:
        return jsonify({"message": "Este planeta ya está en favoritos"}), 400
    
    nuevo_favorito = Favorito(usuario_id=usuario.id, planeta_id=planet_id)
    db.session.add(nuevo_favorito)
    db.session.commit()
    
    return jsonify({"message": "Planeta añadido a favoritos"}), 201

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    usuario = Usuario.query.first()
    personaje = Personaje.query.get(people_id)
    
    if not usuario or not personaje:
        return jsonify({"message": "Usuario o personaje no encontrado"}), 404
    
    existe = Favorito.query.filter_by(usuario_id=usuario.id, personaje_id=people_id).first()
    if existe:
        return jsonify({"message": "Este personaje ya está en favoritos"}), 400
    
    nuevo_favorito = Favorito(usuario_id=usuario.id, personaje_id=people_id)
    db.session.add(nuevo_favorito)
    db.session.commit()
    
    return jsonify({"message": "Personaje añadido a favoritos"}), 201

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    usuario = Usuario.query.first()
    if not usuario:
        return jsonify({"message": "Usuario no encontrado"}), 404
    
    favorito = Favorito.query.filter_by(usuario_id=usuario.id, planeta_id=planet_id).first()
    if not favorito:
        return jsonify({"message": "Planeta favorito no encontrado"}), 404
    
    db.session.delete(favorito)
    db.session.commit()
    
    return jsonify({"message": "Planeta eliminado de favoritos"}), 200

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    usuario = Usuario.query.first()
    if not usuario:
        return jsonify({"message": "Usuario no encontrado"}), 404
    
    favorito = Favorito.query.filter_by(usuario_id=usuario.id, personaje_id=people_id).first()
    if not favorito:
        return jsonify({"message": "Personaje favorito no encontrado"}), 404
    
    db.session.delete(favorito)
    db.session.commit()
    
    return jsonify({"message": "Personaje eliminado de favoritos"}), 200

# Endpoints opcionales para CRUD completo
@app.route('/people', methods=['POST'])
def create_person():
    data = request.get_json()
    nuevo_personaje = Personaje(
        nombre=data.get('nombre'),
        especie=data.get('especie'),
        genero=data.get('genero'),
        afiliacion=data.get('afiliacion'),
        descripcion=data.get('descripcion')
    )
    db.session.add(nuevo_personaje)
    db.session.commit()
    return jsonify(nuevo_personaje.serialize()), 201

@app.route('/planets', methods=['POST'])
def create_planet():
    data = request.get_json()
    nuevo_planeta = Planeta(
        nombre=data.get('nombre'),
        clima=data.get('clima'),
        terreno=data.get('terreno'),
        poblacion=data.get('poblacion'),
        descripcion=data.get('descripcion')
    )
    db.session.add(nuevo_planeta)
    db.session.commit()
    return jsonify(nuevo_planeta.serialize()), 201

if __name__ == '__main__':
    app.run(debug=True)
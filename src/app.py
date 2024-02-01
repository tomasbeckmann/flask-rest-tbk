"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Pokemon, Pokemon_stat, Pokemon_ability, Pokemon_type
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

""" db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else: """

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route("/pokemon", methods=['GET'])
def home():
  pokemons = Pokemon.query.all()
  pokemons = list(map(lambda pokemon: pokemon.serialize_1(), pokemons))

  return jsonify({
    "data": pokemons,
    "status": 'success'
  }),200
  
@app.route("/pokemon/<int:id>", methods=['GET'])
def get_pokemon(id):
  pokemon = Pokemon.query.filter_by(pokemon_id=id).first()
  if pokemon is not None:
    return jsonify(pokemon.serialize_2()), 200
  else:
    return jsonify({"error":"Pokemon not found"}),404

@app.route("/pokemon/<int:id>", methods=['DELETE'])
def delete_pokemon(id):
  pokemon = Pokemon.query.filter_by(pokemon_id=id).first()
  if pokemon is not None:
    db.session.delete(pokemon)
    db.session.commit()
    return jsonify({
      "msg": "Pokemon deleted",
      "status": "Success"
    }), 203
  else:
    return jsonify({"error":"Pokemon not found"}),404  

@app.route('/pokemon', methods=['POST'])
def create_pokemon():
  get_from_body = request.json.get("name")
  pokemon = Pokemon() 
  pokemon_exist = Pokemon.query.filter_by(name=get_from_body).first()
  if pokemon_exist is not None:
    return "The Pokemon already exist"
  else:
    pokemon.name = request.json.get("name")
    pokemon.type = request.json.get("type")
    pokemon.stat = request.json.get("stat")
    pokemon.ability = request.json.get("ability")

    return f"The pokemon was created", 201

@app.route('/pokemon', methods=["PUT"])
def update_pokemon():
  name_to_search = request.json.get("name")
  pokemon = Pokemon.query.filter_by(name=name_to_search).first()
  if pokemon is None:
    return "The Pokemon does not exist", 401
  else:
    pokemon.name = request.json.get("name")
    pokemon.type = request.json.get("type")
    pokemon.stat = request.json.get("stat")
    pokemon.ability = request.json.get("ability")

    db.session.add(pokemon)
    db.session.commit()

    return f"Pokemon updated", 201
  
@app.route("/pokemontype/<int:id>", methods=['GET'])
def get_pokemon_type(id):
  pokemon_type = Pokemon_type.query.filter_by(type_id=id).first()
  if pokemon_type is not None:
    return jsonify(pokemon_type.serialize_1()), 200
  else:
    return jsonify({"error":"Pokemon type not found"}),404
  
@app.route("/pokemontype/<int:id>", methods=['DELETE'])
def delete_pokemon_type(id):
  pokemon_type = Pokemon_type.query.filter_by(type_id=id).first()
  if pokemon_type is not None:
    db.session.delete(pokemon_type)
    db.session.commit()
    return jsonify({
      "msg": "Pokemon type deleted",
      "status": "Success"
    }), 203
  else:
    return jsonify({"error":"Pokemon not found"}),404  

@app.route('/pokemontype', methods=['POST'])
def create_pokemon_type():
  get_from_body = request.json.get("id")
  pokemon_type = Pokemon_type() 
  pokemon_type_exist = Pokemon_type.query.filter_by(type_id=get_from_body).first()
  if pokemon_type_exist is not None:
    return "The Pokemon type already exist"
  else:
    pokemon_type.type_id = request.json.get("type_id")
    pokemon_type.type_1 = request.json.get("type_1")
    pokemon_type.type_2 = request.json.get("type_2")

    return f"The pokemon type was created", 201

@app.route('/pokemontype', methods=["PUT"])
def update_pokemon_type():
  id_to_search = request.json.get("id")
  pokemon_type = Pokemon_type.query.filter_by(type_id=id_to_search).first()
  if pokemon_type is None:
    return "The Pokemon type does not exist", 401
  else:
    pokemon_type.type_id = request.json.get("type_id")
    pokemon_type.type_1 = request.json.get("type_1")
    pokemon_type.type_2 = request.json.get("type_2")


    db.session.add(pokemon_type)
    db.session.commit()

    return f"Pokemon type updated", 201

@app.route("/pokemonstat/<int:id>", methods=['GET'])
def get_pokemon_stat(id):
  pokemon_stat = Pokemon_stat.query.filter_by(stat_id=id).first()
  if pokemon_stat is not None:
    return jsonify(pokemon_stat.serialize_1()), 200
  else:
    return jsonify({"error":"Pokemon stat not found"}),404
  
@app.route("/pokemonstat/<int:id>", methods=['DELETE'])
def delete_pokemon_stat(id):
  pokemon_stat = Pokemon_stat.query.filter_by(stat_id=id).first()
  if pokemon_stat is not None:
    db.session.delete(pokemon_stat)
    db.session.commit()
    return jsonify({
      "msg": "Pokemon stat deleted",
      "status": "Success"
    }), 203
  else:
    return jsonify({"error":"Pokemon not found"}),404  

@app.route('/pokemonstat', methods=['POST'])
def create_pokemon_stat():
  get_from_body = request.json.get("id")
  pokemon_stat = Pokemon_stat() 
  pokemon_stat_exist = Pokemon_stat.query.filter_by(stat_id=get_from_body).first()
  if pokemon_stat_exist is not None:
    return "The Pokemon stat already exist"
  else:
    pokemon_stat.stat_id = request.json.get("stat_id")
    pokemon_stat.height = request.json.get("height")
    pokemon_stat.weight = request.json.get("weight")
    pokemon_stat.hp = request.json.get("hp")
    pokemon_stat.attack = request.json.get("attack")
    pokemon_stat.defense = request.json.get("defense")

    return f"The pokemon stat was created", 201

@app.route('/pokemonstat', methods=["PUT"])
def update_pokemon_stat():
  id_to_search = request.json.get("id")
  pokemon_stat = Pokemon_stat.query.filter_by(stat_id=id_to_search).first()
  if pokemon_stat is None:
    return "The Pokemon stat does not exist", 401
  else:
    pokemon_stat.stat_id = request.json.get("stat_id")
    pokemon_stat.height = request.json.get("height")
    pokemon_stat.weight = request.json.get("weight")
    pokemon_stat.hp = request.json.get("hp")
    pokemon_stat.attack = request.json.get("attack")
    pokemon_stat.defense = request.json.get("defense")

    db.session.add(pokemon_stat)
    db.session.commit()

    return f"Pokemon stat updated", 201
  
@app.route("/pokemonability/<int:id>", methods=['GET'])
def get_pokemon_ability(id):
  pokemon_ability = Pokemon_ability.query.filter_by(ability_id=id).first()
  if pokemon_ability is not None:
    return jsonify(pokemon_ability.serialize_1()), 200
  else:
    return jsonify({"error":"Pokemon ability not found"}),404
  
@app.route("/pokemonability/<int:id>", methods=['DELETE'])
def delete_pokemon_ability(id):
  pokemon_ability = Pokemon_ability.query.filter_by(ability_id=id).first()
  if pokemon_ability is not None:
    db.session.delete(pokemon_ability)
    db.session.commit()
    return jsonify({
      "msg": "Pokemon ability deleted",
      "status": "Success"
    }), 203
  else:
    return jsonify({"error":"Pokemon not found"}),404  

@app.route('/pokemonability', methods=['POST'])
def create_pokemon_ability():
  get_from_body = request.json.get("id")
  pokemon_ability = Pokemon_ability() 
  pokemon_ability_exist = Pokemon_ability.query.filter_by(ability_id=get_from_body).first()
  if pokemon_ability_exist is not None:
    return "The Pokemon ability already exist"
  else:
    pokemon_ability.ability_id = request.json.get("ability_id")
    pokemon_ability.ability_1 = request.json.get("ability_1")
    pokemon_ability.ability_2 = request.json.get("ability_2")

    return f"The pokemon ability was created", 201

@app.route('/pokemonability', methods=["PUT"])
def update_pokemon_ability():
  id_to_search = request.json.get("id")
  pokemon_ability = Pokemon_ability.query.filter_by(ability_id=id_to_search).first()
  if pokemon_ability is None:
    return "The Pokemon ability does not exist", 401
  else:
    pokemon_ability.ability_id = request.json.get("ability_id")
    pokemon_ability.ability_1 = request.json.get("ability_1")
    pokemon_ability.ability_2 = request.json.get("ability_2")

    db.session.add(pokemon_ability)
    db.session.commit()

    return f"Pokemon ability updated", 201


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)

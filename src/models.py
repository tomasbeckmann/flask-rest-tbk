from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

""" class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        } """

class Pokemon(db.Model):
    __tablename__ = 'pokemon'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    pokemon_id = db.Column(db.Integer, primary_key=True,)
    name = db.Column(db.String(25), nullable=False)
    pokemontype_id = db.Column(db.Integer, db.ForeignKey('pokemontype.type_id'), nullable=False)
    pokemontype = db.relationship('Pokemon_type')
    pokemonstat_id = db.Column(db.Integer, db.ForeignKey('pokemonstat.stat_id'), nullable=False)
    pokemonstat = db.relationship('Pokemon_stat')
    pokemonability_id = db.Column(db.Integer, db.ForeignKey('pokemonability.ability_id'), nullable=False)
    pokemonability = db.relationship('Pokemon_ability')


    def serialize_1(self):
        return {
            "pokemon_id" : self.pokemon_id,
            "name" : self.name,
        }

    def serialize_2(self):
        return {
            "pokemon_id" : self.pokemon_id,
            "name" : self.name
        }


class Pokemon_type(db.Model):
    __tablename__ = 'pokemontype'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    type_id = db.Column(db.Integer, primary_key=True, nullable=False)
    type_1 = db.Column(db.String(10), nullable=False)
    type_2 = db.Column(db.String(10), nullable=True)

    def serialize(self):
        return {
            "type_id" : self.type_id,
            "type_1" : self.type_1,
            "type_2" : self.type_2,
        }
    

class Pokemon_stat(db.Model):
    __tablename__ = 'pokemonstat'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    stat_id = db.Column(db.Integer, primary_key=True, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    hp = db.Column(db.Integer, nullable=False)
    attack = db.Column(db.Integer, nullable=False)
    defense = db.Column(db.Integer, nullable=False)

    def serialize(self):
        return {
            "stat_id" : self.stat_id,
            "height" : self.height,
            "weight" : self.weight,
            "hp" : self.hp,
            "attack" : self.attack,
            "defense" : self.defense,
        }

class Pokemon_ability(db.Model):
    __tablename__ = 'pokemonability'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.\
    ability_id = db.Column(db.Integer, primary_key=True, nullable=False)
    ability_1 = db.Column(db.String(25), nullable=False)
    ability_2 = db.Column(db.String(25), nullable=False)

    def serialize(self):
        return {
            "ability_id" : self.ability_id,
            "ability_1" : self.ability_1,
            "ability_2" : self.ability_2,
        }
    

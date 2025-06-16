from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import reqparse
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///superheroes.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Hero(db.Model):
    __tablename__ = "heroes"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    super_name = db.Column(db.String, nullable=False)

    powers = db.relationship('HeroPower', back_populates='hero', cascade='all, delete-orphan')

class Power(db.Model):
    __tablename__ = "powers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)

    heroes = db.relationship('HeroPower', back_populates='power', cascade='all, delete-orphan')

class HeroPower(db.Model):
    __tablename__ = "hero_powers"
    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String, nullable=False)
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'), nullable=False)

    hero = db.relationship('Hero', back_populates='powers')
    power = db.relationship('Power', back_populates='heroes')

    VALID_STRENGTHS = ['Strong', 'Weak', 'Average']

    @db.validates('strength')
    def validate_strength(self, key, strength):
        if strength not in self.VALID_STRENGTHS:
            raise ValueError(f"Strength must be one of {self.VALID_STRENGTHS}")
        return strength

# Request parsers for validation of JSON data for hero powers and power 
hero_power_parser = reqparse.RequestParser()
hero_power_parser.add_argument('strength', type=str, required=True,choices=HeroPower.VALID_STRENGTHS,help="Strength is required and must be one of ['Strong', 'Weak', 'Average']")
hero_power_parser.add_argument('hero_id', type=int, required=True,help="Hero ID is required and must be an integer")
hero_power_parser.add_argument('power_id', type=int, required=True,help="Power ID is required and must be an integer")

power_update_parser = reqparse.RequestParser()
power_update_parser.add_argument('description', type=str, required=True, help="Description is required")

#get all heroes
@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    return jsonify([{"id": hero.id, "name": hero.name, "super_name": hero.super_name} for hero in heroes])

#get a hero by Id
@app.route('/heroes/<int:hero_id>', methods=['GET'])
def get_hero(hero_id):
    hero = Hero.query.get(hero_id)
    if not hero:
        return jsonify({"error": "Hero not found"}), 404

    hero_powers = []
    for hp in hero.powers:
        hero_powers.append({
            "id": hp.id,
            "hero_id": hp.hero_id,
            "power_id": hp.power_id,
            "strength": hp.strength,
            "power": {
                "id": hp.power.id,
                "name": hp.power.name,
                "description": hp.power.description
            }
        })
    
    response = {
        "id": hero.id,
        "name": hero.name,
        "super_name": hero.super_name,
        "hero_powers": hero_powers
    }
    return jsonify(response)
#gets all powers
@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    return jsonify([{"id": power.id, "name": power.name, "description": power.description} for power in powers])

#get single power by id
@app.route('/powers/<int:power_id>', methods=['GET'])
def get_power(power_id):
    power = Power.query.get(power_id)
    if not power:
        return jsonify({"error": "Power not found"}), 404
    return jsonify({"id": power.id, "name": power.name, "description": power.description})

@app.route('/powers/<int:power_id>', methods=['PATCH'])
def update_power(power_id):
    power = Power.query.get(power_id)
    if not power:
        return jsonify({"error": "Power not found"}), 404

    args = power_update_parser.parse_args()
    desc = args['description'].strip()
    if len(desc) < 20:
        return jsonify({"errors": ["Description must be  20 characters long"]}), 400

    power.description = desc
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": [str(e)]}), 400

    return jsonify({"id": power.id, "name": power.name, "description": power.description})

@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    args = hero_power_parser.parse_args()

    hero = Hero.query.get(args['hero_id'])
    if not hero:
        return jsonify({"errors": ["Hero not found"]}), 404
    power = Power.query.get(args['power_id'])
    if not power:
        return jsonify({"errors": ["Power not found"]}), 404

    strength = args['strength']

    if strength not in HeroPower.VALID_STRENGTHS:
        return jsonify({"errors": [f"Strength to be one of {HeroPower.VALID_STRENGTHS}"]}), 400

    new_hero_power = HeroPower(
        strength=strength,
        hero_id=args['hero_id'],
        power_id=args['power_id']
    )
    try:
        db.session.add(new_hero_power)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": [str(e)]}), 400

    return jsonify({
        "id": new_hero_power.id,
        "hero_id": new_hero_power.hero_id,
        "power_id": new_hero_power.power_id,
        "strength": new_hero_power.strength,
        "power": {
            "id": new_hero_power.power.id,
            "name": new_hero_power.power.name,
            "description": new_hero_power.power.description
        },
        "hero": {
            "id": new_hero_power.hero.id,
            "name": new_hero_power.hero.name,
            "super_name": new_hero_power.hero.super_name
        }
    }), 201

if __name__ == '__main__':
    app.run(debug=True)

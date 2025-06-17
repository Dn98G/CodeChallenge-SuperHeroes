from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import reqparse
import os

# Initialize Flask app and configure the database
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL", "sqlite:///superheroes.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Set up SQLAlchemy and Flask-Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Model representing a superhero
class Superhero(db.Model):
    __tablename__ = "heroes"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)  
    alias = db.Column(db.String, nullable=False)  

    
    hero_abilities = db.relationship(
        "HeroAbility", back_populates="hero", cascade="all, delete-orphan"
    )

# Model representing a superpower or ability
class Ability(db.Model):
    __tablename__ = "powers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)

    linked_heroes = db.relationship(
        "HeroAbility", back_populates="ability", cascade="all, delete-orphan"
    )


# Association model linking Superheroes with Powers and defining strength
class HeroAbility(db.Model):
    __tablename__ = "hero_powers"
    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String, nullable=False)
    hero_id = db.Column(db.Integer, db.ForeignKey("heroes.id"), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey("powers.id"), nullable=False)

    
    hero = db.relationship("Superhero", back_populates="hero_abilities")
    ability = db.relationship("Ability", back_populates="linked_heroes")

    ALLOWED_STRENGTHS = ["Strong", "Weak", "Average"]

    # Validate the 'strength' field to accept only predefined values
    @db.validates("strength")
    def validate_strength(self, key, value):
        if value not in self.ALLOWED_STRENGTHS:
            raise ValueError(
                f"Strength must be one of: {', '.join(self.ALLOWED_STRENGTHS)}"
            )
        return value

# Parser for POST /hero_powers endpoint
ability_assignment_parser = reqparse.RequestParser()
ability_assignment_parser.add_argument(
    "strength",
    type=str,
    required=True,
    choices=HeroAbility.ALLOWED_STRENGTHS,
    help="Strength must be one of: Strong, Weak, or Average.",
)
ability_assignment_parser.add_argument(
    "hero_id", type=int, required=True, help="Hero ID must be provided."
)
ability_assignment_parser.add_argument(
    "power_id", type=int, required=True, help="Power ID must be provided."
)

# Parser for PATCH /powers/<id> endpoint
description_update_parser = reqparse.RequestParser()
description_update_parser.add_argument(
    "description", type=str, required=True, help="A description is required."
)

# Retrieve list of all superheroes
@app.route("/heroes", methods=["GET"])
def list_heroes():
    all_heroes = Superhero.query.all()
    result = [
        {"id": hero.id, "name": hero.name, "super_name": hero.alias}
        for hero in all_heroes
    ]
    return jsonify(result)


# Retrieve details of a specific superhero including their powers
@app.route("/heroes/<int:hero_id>", methods=["GET"])
def fetch_hero_details(hero_id):
    hero = Superhero.query.get(hero_id)
    if not hero:
        return jsonify({"error": "Hero not found"}), 404

    abilities = []
    for ability_link in hero.hero_abilities:
        abilities.append(
            {
                "id": ability_link.id,
                "strength": ability_link.strength,
                "hero_id": ability_link.hero_id,
                "power_id": ability_link.power_id,
                "power": {
                    "id": ability_link.ability.id,
                    "name": ability_link.ability.name,
                    "description": ability_link.ability.description,
                },
            }
        )

    return jsonify(
        {
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.alias,
            "hero_powers": abilities,
        }
    )


# Retrieve list of all available powers
@app.route("/powers", methods=["GET"])
def list_powers():
    powers = Ability.query.all()
    return jsonify(
        [{"id": p.id, "name": p.name, "description": p.description} for p in powers]
    )

# Get detailed info about a specific power
@app.route("/powers/<int:power_id>", methods=["GET"])
def get_power_info(power_id):
    power = Ability.query.get(power_id)
    if not power:
        return jsonify({"error": "Power not found"}), 404
    return jsonify(
        {"id": power.id, "name": power.name, "description": power.description}
    )

# Update the description of a specific power
@app.route("/powers/<int:power_id>", methods=["PATCH"])
def modify_power_description(power_id):
    power = Ability.query.get(power_id)
    if not power:
        return jsonify({"error": "Power not found"}), 404

    # Parse and validate the new description
    data = description_update_parser.parse_args()
    desc = data["description"].strip()
    if len(desc) < 20:
        return jsonify({"errors": ["Description must be at least 20 characters."]}), 400

    power.description = desc

    # Attempt to save changes to the database
    try:
        db.session.commit()
    except Exception as err:
        db.session.rollback()
        return jsonify({"errors": [str(err)]}), 400

    return jsonify(
        {"id": power.id, "name": power.name, "description": power.description}
    )


# Assign a new power to a superhero with a defined strength
@app.route("/hero_powers", methods=["POST"])
def assign_power_to_hero():
    args = ability_assignment_parser.parse_args()

    # Validate existence of hero and power
    hero = Superhero.query.get(args["hero_id"])
    if not hero:
        return jsonify({"errors": ["Hero not found."]}), 404

    power = Ability.query.get(args["power_id"])
    if not power:
        return jsonify({"errors": ["Power not found."]}), 404

    # Create and store the relationship record
    new_link = HeroAbility(
        strength=args["strength"], hero_id=args["hero_id"], power_id=args["power_id"]
    )

    try:
        db.session.add(new_link)
        db.session.commit()
    except Exception as err:
        db.session.rollback()
        return jsonify({"errors": [str(err)]}), 400

    return jsonify(
        {
            "id": new_link.id,
            "strength": new_link.strength,
            "hero_id": new_link.hero_id,
            "power_id": new_link.power_id,
            "power": {
                "id": power.id,
                "name": power.name,
                "description": power.description,
            },
            "hero": {"id": hero.id, "name": hero.name, "super_name": hero.alias},
        }
    ), 201

# Entry point to run the server
if __name__ == "__main__":
    app.run(debug=True)


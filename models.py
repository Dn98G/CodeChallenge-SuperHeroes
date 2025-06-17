from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

# Initialize the SQLAlchemy database object
db = SQLAlchemy()

# Hero Model
class Hero(db.Model):
    __tablename__ = "heroes"  

    id = db.Column(db.Integer, primary_key=True)  
    name = db.Column(db.String, nullable=False)  
    super_name = db.Column(db.String, nullable=False)  

    # One-to-many relationship with HeroPower
    hero_powers = db.relationship(
        "HeroPower",
        back_populates="hero",
        cascade="all, delete-orphan",  
    )

# Power Model
class Power(db.Model):
    __tablename__ = "powers"  

    id = db.Column(db.Integer, primary_key=True)  
    name = db.Column(db.String, nullable=False)  
    description = db.Column(
        db.String, nullable=False
    )  

    
    power_heroes = db.relationship(
        "HeroPower", back_populates="power", cascade="all, delete-orphan"
    )


# Association Model: HeroPower
class HeroPower(db.Model):
    __tablename__ = "hero_powers"  

    id = db.Column(db.Integer, primary_key=True)  
    strength = db.Column(
        db.String, nullable=False
    )  

    # Foreign key linking to Hero
    hero_id = db.Column(db.Integer, db.ForeignKey("heroes.id"), nullable=False)

    # Foreign key linking to Power
    power_id = db.Column(db.Integer, db.ForeignKey("powers.id"), nullable=False)

    # Relationship back to Hero and Power
    hero = db.relationship("Hero", back_populates="hero_powers")
    power = db.relationship("Power", back_populates="power_heroes")

    # Valid values for strength
    VALID_STRENGTHS = ["Strong", "Weak", "Average"]

    # Validator to ensure strength is one of the allowed values
    @validates("strength")
    def validate_strength(self, key, value):
        if value not in self.VALID_STRENGTHS:
            raise ValueError(
                f"Invalid strength value. Choose from: {', '.join(self.VALID_STRENGTHS)}"
            )
        return value

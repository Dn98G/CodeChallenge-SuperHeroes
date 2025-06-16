from flask_sqlachemy import SQLAlchemy

db =SQLAlchemy()

class Hero(db.model):
    __tablename__ = "heroes"
    id=db.Column(db.Integer, primary_key =True)
    name=db.Column(db.String, nullable =False)
    super_name =db.Column(db.String, nullable=False)

    powers=db.relationship('HeroPower', back_populates='hero', cascade='all, delete-orphan')
 
class Power(db.Model):
    __tablename__ ="powers"
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String,nullable=False)
    description=db.Column(db.String, nullable=False)

    heroes=db.relationship('HeroPower', back_populates='power', cascade='all, delete-orphan')

class HeroPower(db.Model):
    __tablename__ ="hero-powers"
    id=db.Column(db.Integer, primary_key=True)
    strength=db.Column(db.String, nullable=False)
    hero_id=db.Column(db.Integer, db.Foreignkey('hero.id', nullable=False))
    power_id=db.Column(db.Integer, db.Foreignkey('power.id', nullable=False))

    hero=db.relationship('Hero', back_populates='powers')
    power=db.relationship('Power', back_populates='heroes')

    VALID_STRENGTHS = ['Strong', 'Weak', 'Average']
    @db.validates('strength')
    def validate_strength(self, key, strength):
        if strength not in self.VALID_STRENGTHS:
            raise ValueError(f"Strength must be one of {self.VALID_STRENGTHS}")
        return strength
# app/models/character.py
from app import db

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    actor = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    photo_url = db.Column(db.String(500), nullable=True)
    character_url = db.Column(db.String(500), nullable=True)

    def __repr__(self):
        return f"<Character {self.name}>"

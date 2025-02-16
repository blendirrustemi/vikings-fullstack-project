# app/routes/api.py
from flask import Blueprint, jsonify
from app.models.character import Character

api_bp = Blueprint('api', __name__)

"""
API endpoint to get all characters
"""

@api_bp.route('/characters')
def get_characters():
    characters = Character.query.all()
    return jsonify([{
        'name': c.name,
        'actor': c.actor,
        'description': c.description,
        'photo_url': c.photo_url
    } for c in characters])


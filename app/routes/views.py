# app/routes/views.py
from flask import Blueprint, render_template
from app.models.character import Character

views_bp = Blueprint('views', __name__)

@views_bp.route('/')
def index():
    characters = Character.query.all()
    return render_template('index.html', characters=characters)

@views_bp.route('/character/<int:id>')
def character_page(id):
    character = Character.query.get(id)
    return render_template('character_page.html', character=character)
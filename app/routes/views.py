# app/routes/views.py
from flask import Blueprint, render_template
from app.models.character import Character
from app.utils.vikings_netflix_scraper import scrape_vikings_characters
from app.utils.database import store_characters

views_bp = Blueprint('views', __name__)

@views_bp.route('/')
def index():
    try:
        characters = Character.query.all()
        return render_template('index.html', characters=characters)
    except Exception as e:
        print(e)
        return str(e)
    
@views_bp.route('/character/<int:id>')
def character_page(id):
    character = Character.query.get(id)
    return render_template('character_page.html', character=character)


@views_bp.route('/scrape_vikings', methods=['GET'])
def scrape_vikings():
    # Run the scraper to get the character data
    
    store_characters()

    return "Scraping complete and data saved to database."
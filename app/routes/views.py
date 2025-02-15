# app/routes/views.py
from flask import Blueprint, redirect, render_template, request, url_for
from app.models.character import Character
from app.utils.vikings_netflix_scraper import scrape_vikings_characters
from app.utils.database import store_characters
from app import db
views_bp = Blueprint('views', __name__)

@views_bp.route('/')
def index():
    try:
        search_query = request.args.get('search', '').lower()  # Get the search query from URL args
        has_photo = request.args.get('has_photo') == 'true'  # Check if "Has photo?" checkbox is checked
        
        if search_query:
            # If search_query is provided, filter by name or actor
            characters = Character.query.filter(
                (Character.name.ilike(f'%{search_query}%')) |
                (Character.actor.ilike(f'%{search_query}%'))
            )
        else:
            # If no search query is provided, fetch all characters
            characters = Character.query

        # If "Has photo?" filter is applied, filter by non-empty photo_url
        if has_photo:
            characters = characters.filter(Character.photo_url != None).filter(Character.photo_url != '')

        characters = characters.all()

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


@views_bp.route('/character/<int:id>', methods=['POST'])
def update_character(id):
    character = Character.query.get(id)
    if character:
        character.name = request.form['name']
        character.actor = request.form['actor']
        character.description = request.form['description']
        character.photo_url = request.form['photo_url']
        character.character_url = request.form['character_url']
        
        db.session.commit()  # Save changes to the database
        
        # Redirect to the updated character page using the correct endpoint
        return redirect(url_for('views.character_page', id=character.id))  # Make sure this is 'views.character_page'
    
    return "Character not found", 404

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
        """
        View for the homepage
        Filters the characters based on the search query and has_photo.
        """
        search_query = request.args.get('search', '').lower()
        has_photo = request.args.get('has_photo') == 'true'
        
        # If the query is provided, it filters by checking on the character name and actor
        if search_query:
            characters = Character.query.filter(
                (Character.name.ilike(f'%{search_query}%')) |
                (Character.actor.ilike(f'%{search_query}%'))
            )
        else:
            characters = Character.query

        # If has_photo is True it filters by checking if the photo_url is not None or empty
        if has_photo:
            characters = characters.filter(Character.photo_url != None).filter(Character.photo_url != '')

        characters = characters.all()

        return render_template('index.html', characters=characters)
    except Exception as e:
        print(e)
        return str(e)
    

"""
View for the individual character page
"""
@views_bp.route('/character/<int:id>')
def character_page(id):
    character = Character.query.get(id)
    return render_template('character_page.html', character=character)

"""
Endpoint to edit the character details
"""
@views_bp.route('/character/<int:id>', methods=['POST'])
def update_character(id):
    character = Character.query.get(id)
    if character:
        character.name = request.form['name']
        character.actor = request.form['actor']
        character.description = request.form['description']
        character.photo_url = request.form['photo_url']
        character.character_url = request.form['character_url']
        
        db.session.commit()
        
        return redirect(url_for('views.character_page', id=character.id))
    
    return "Character not found", 404

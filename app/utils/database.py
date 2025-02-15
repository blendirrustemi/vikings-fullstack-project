from app.utils import vikings_netflix_scraper, vikings_nfl_scraper  # Correct the import path for the scraper
from app.models.character import db, Character  # Correct import path for db and the Character model

def store_characters():
    characters = None # Call my scrapers

    for char in characters:
        character = Character(
            name=char['name'],
            actor=char['actor'],
            description=char['description'],
            photo_url=char['photo_url']
        )
        
        # Add the character to the session
        db.session.add(character)
    
    # Commit the changes to the database
    db.session.commit()

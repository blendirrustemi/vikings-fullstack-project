from app.models.character import db, Character
from app.utils.vikings_netflix_scraper import scrape_vikings_characters
from app.utils.norsemen_series import scrape_norsemen_cast

def store_characters():
    vikings = scrape_vikings_characters()
    norsemen = scrape_norsemen_cast()

    characters = vikings + norsemen

    for char in characters:
        character = Character(
            name=char['name'],
            actor=char['actor'],
            description=char['description'],
            photo_url=char['photo_url'],
            character_url=char['character_url']
        )
        
        # Add the character model to the session
        db.session.add(character)
    
    # Commit the changes
    db.session.commit()

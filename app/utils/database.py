# app/utils/database.py
from app.db import db
from app.models.character import Character
from app.utils.vikings_netflix_scraper import scrape_vikings_characters
from app.utils.norsemen_series import scrape_norsemen_cast

import time

def retry_scrape(scrape_function, retries=3, delay=2):
    for attempt in range(retries):
        try:
            return scrape_function()
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print("All attempts failed.")
                return []

def store_characters():
    print("Started Scraping Vikings...")
    vikings = retry_scrape(scrape_vikings_characters)
    print(f"Scraped {len(vikings)} Vikings Characters!")

    print("Started Scraping Norsemen...")
    norsemen = retry_scrape(scrape_norsemen_cast)
    print(f"Scraped {len(norsemen)} Norsemen Characters!")

    characters = vikings + norsemen
    from app import create_app  # import inside function to avoid circular import

    app = create_app()

    """
    Store the characters in the database
    """
    with app.app_context():
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

from playwright.sync_api import sync_playwright
import time

def scrape_vikings_characters():
    character_data = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Step 1: Go to the Vikings Cast page
        page.goto("https://www.history.com/shows/vikings/cast")

        # Step 2: Accept cookies
        try:
            page.click('button[data-testid="tou-agree-btn"]', timeout=5000)
            time.sleep(1)  # here im giving time if there are any UI changes
        except:
            print("Cookies button not found, skipping...")

        # Step 3: Scrape character names and profile pictures
        """
        In this step, we will scrape the character names and profile pictures,
        then store them in a list of dictionaries. This helps us navigate directly to the url, so we dont click on each character.
        """
        try:
            characters = page.query_selector_all('li')

            character_info = []
            for char in characters:
                name_element = char.query_selector('div.details strong')
                img_element = char.query_selector('div.img-container img')

                if name_element and img_element:
                    name = name_element.inner_text().strip().lower()
                    img_url = img_element.get_attribute('src')

                    character_info.append({'name': name, 'img_url': img_url})
        except:
            print("Error occurred while scraping character names and profile pictures.")
            return []

        # Step 4: Iterate through each name and visit the character's page
        try:
            for char in character_info:
                try:
                    name = char['name']
                    profile_pic = char['img_url']

                    # Format the URL
                    character_url = f"https://www.history.com/shows/vikings/cast/{name.replace(' ', '-')}"

                    page.goto(character_url)
                    page.wait_for_load_state('networkidle')

                    # Step 5: Extract required elements
                    name_element = page.query_selector('header.section-title strong[itemprop="name"]')
                    actor_element = page.query_selector('header.section-title small')
                    description_element = page.query_selector('header.section-title + p')

                    # Extract text content
                    name_text = name_element.inner_text().strip() if name_element else "Unknown"
                    actor_text = actor_element.inner_text().replace("Played by ", "").strip() if actor_element else "Unknown"
                    description_text = description_element.inner_text().strip() if description_element else "No description available"

                    """
                    Here we create the dictionary for each character and append it to the character_data list.
                    """
                    character_data.append({
                        'name': name_text,
                        'actor': actor_text,
                        'description': description_text,
                        'photo_url': profile_pic,
                        'character_url': character_url
                    })
                except:
                    print(f"Error occurred while scraping {name}'s details.")
                    continue
        except:
            print("Error occurred while scraping character details.")
            return []

        browser.close()

    return character_data

import requests
from bs4 import BeautifulSoup

def get_profile_picture(character_url):
    response = requests.get(character_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Get the profile picture
        img_tag = soup.find('a', {'class': 'mw-file-description'}).find('img') if soup.find('a', {'class': 'mw-file-description'}) else None
        if img_tag:
            img_src = img_tag['src']
            return f"https:{img_src}"
    return ''

def scrape_norsemen_cast():
    url = "https://en.wikipedia.org/wiki/Norsemen_(TV_series)"
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Get the name and description from the section
            cast_div = soup.find('div', {'class': 'mw-heading mw-heading2'})
            
            if cast_div:
                """
                If the data is found, then continue with the parsing, getting the name, description, and profile picture.
                """
                cast_list = cast_div.find_next('ul')

                parsed_data = []
                
                if cast_list:
                    for li in cast_list.find_all('li'):
                        a_tag = li.find('a')
                        if a_tag:
                            # Extract the character's name (actor)
                            actor_name = a_tag.get_text(strip=True)
                            character_url = "https://en.wikipedia.org" + a_tag['href']
                            
                            # Extract the character's name (after "as")
                            character_description = li.get_text().split("as")
                            if len(character_description) > 1:
                                character_name = character_description[1].split(',')[0].strip()
                                character_description_text = ', '.join(character_description[1].split(',')[1:]).strip()
                            else:
                                character_name = ""
                                character_description_text = ""
                            
                            # Get the profile picture
                            profile_picture_url = get_profile_picture(character_url)
                            
                            parsed_data.append({
                                'name': character_name,
                                'actor': actor_name,
                                'description': character_description_text,
                                'photo_url': profile_picture_url,
                                'character_url': character_url
                            })

                    return parsed_data
                else:
                    print("Cast list not found.")
                    return []
            else:
                print("Cast and characters section not found.")
                return []
        else:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")
            return []
    except Exception as e:
        print(f"An error occurred while scraping: {e}")
        return []
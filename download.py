import os
import requests
import shutil
from bs4 import BeautifulSoup

resp = requests.get('https://pokemondb.net/pokedex/all')
soup = BeautifulSoup(resp.text, features='html.parser')
table = soup.find('table')
count = 0
for row in table.find_all('tr'):
    columns = row.find_all('td')
    if columns:
        number = columns[0].get_text()
        name = columns[1].get_text().lower()
        path = f'images/{number}.jpg'
        # skip alt forms for now
        if os.path.exists(path):
            print(f'{name} already exists')
            continue
        url = f"https://pokemondb.net{columns[1].find('a')['href']}"
        pokemon_page = requests.get(url)
        if pokemon_page.status_code == 200:
            pokemon = BeautifulSoup(pokemon_page.text, features='html.parser')
            try:
                pokemon_image = requests.get(pokemon.find('img')['src'], stream=True)
            except Exception as exc:
                continue
            if pokemon_image.status_code == 200:
                print(path)
                with open(path, 'wb') as outf:
                    shutil.copyfileobj(pokemon_image.raw, outf)

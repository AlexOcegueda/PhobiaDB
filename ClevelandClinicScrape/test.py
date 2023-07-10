import re
import requests
from bs4 import BeautifulSoup
# This page was to test out crawling on one page link before doing them all.

def process_disease_page(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract name and description
        name = soup.find('h1', class_="page-header__title").text.strip()
        description = soup.find('div', class_="page-header__subtitle").text.strip()

        # Scrape section data
        data = {}
        current_section = None
        for element in soup.find_all(['h3', 'ul', 'p']):
            if element.name == 'h3':
                current_section = element.text.strip()
                data[current_section] = {'items': []}
            elif current_section and element.name in ['ul', 'p']:
                data[current_section]['items'].append(element.text.strip())

        result = {
            'name': name,
            'description': description,
            'data': data
        }

        return result

    except requests.exceptions.RequestException as e:
        print('Error:', e)

starting_url = 'https://my.clevelandclinic.org/health/diseases'
disease_url = 'https://my.clevelandclinic.org/health/diseases/22557-barophobia-fear-of-gravity#management-and-treatment'
result = process_disease_page(disease_url)
print(result)

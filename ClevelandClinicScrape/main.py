import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

geckodriver_path = './geckodriver'  # Replace with the actual path to geckodriver

# Configure Firefox options
firefox_options = Options()
firefox_options.add_argument("--headless")  # Run Firefox in headless mode

# Set the path to the geckodriver executable
driver = webdriver.Firefox(
    executable_path=geckodriver_path,
    options=firefox_options,
    capabilities=DesiredCapabilities().FIREFOX
)

# Set the page load timeout (in seconds)
timeout = 10
driver.set_page_load_timeout(timeout)

# Rest of your code using Selenium with Firefox
# ...

def crawl(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find disease links
        disease_links = driver.find_elements(By.CSS_SELECTOR, 'a.index-list-link')
        filtered_links = [link for link in disease_links if 'phobia' in link.text.lower()]

        for link in filtered_links:
            href = link.get_attribute('href')
            base_url = 'https://my.clevelandclinic.org'
            disease_url = urljoin(base_url, href)
            print(disease_url)
            data = process_disease_page(disease_url)
            save_data_to_json(data)
            print('Saved data to JSON')

        # Follow pagination links if available
        next_link = soup.select_one('a[rel="next"]')
        if next_link:
            next_href = next_link['href']
            next_url = urljoin(base_url, next_href)
            crawl(next_url)
    except requests.exceptions.RequestException as e:
        print('Error:', e)

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

def save_data_to_json(data):
    with open('crawled_data.json', 'a', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)
        file.write('\n')

starting_url = 'https://my.clevelandclinic.org/health/diseases'
crawl(starting_url)

# Close the WebDriver instance
driver.quit()

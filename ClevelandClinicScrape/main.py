import json
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from selenium.common.exceptions import StaleElementReferenceException

def crawl(url):
    try:
        driver.get(url)
        
        wait = WebDriverWait(driver, 10)
        alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p","q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
        alpha = ["h", "i", "j", "k", "l", "m", "n", "o", "p","q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
        # browse A-Z btn
        first_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'js-library-search-nav__browse-btn')))
        first_button.click()

        # clicking through a-z of navigation
        for letter in alpha:
            letter_id = f"aab3c309-de3a-40a3-a565-007740a9633djs-{letter}"
            letter_xpath = f"//*[@id='{letter_id}']"

            second_button = wait.until(EC.element_to_be_clickable((By.XPATH, letter_xpath)))
            second_button.click()

            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.index-list-link')))

            elements = driver.find_elements(By.CSS_SELECTOR, '.index-list-link') # diseases 

            # Initialize an empty list for the crawled data
            crawled_data = []

            for element in elements:
                print(element)
                try:
                    element_text = element.text

                    if 'phobia' in element_text.lower():
                        href = element.get_attribute('href')
                        if href:
                            result = process_disease_page(href)
                            crawled_data.append(result)  
                except StaleElementReferenceException:
                    continue

            # Save the list of crawled data to a new JSON file
            filename = f"crawled_data_{letter}.json"
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(crawled_data, file, ensure_ascii=False)
        
    except Exception as e:
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

geckodriver_path = './geckodriver'  # Replace with the actual path to geckodriver

# Configure Firefox options
firefox_options = Options()
firefox_options.add_argument('-headless')  # Run Firefox in headless mode

# Create a Firefox service instance
service = Service(geckodriver_path)

# Create a Firefox webdriver instance
driver = webdriver.Firefox(service=service, options=firefox_options)

starting_url = 'https://my.clevelandclinic.org/health/diseases'
crawl(starting_url)

print('done')
driver.quit()

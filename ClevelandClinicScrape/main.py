"""
Crawl and extract data from a ClevelandClinic.org about phobias. 
This can be modified to return ALL diseases and I am planning to 
add in documentations where to comment out the phobia filter to 
achieve this. 

Author: Alex Ocegueda Castro
Version: 1.0
"""

import json
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
    """
    Crawl the website and extract data related to phobias.

    Args:
        url (str): The URL of the website to crawl.

    Returns:
        None

    Raises:
        Exception: If any error occurs during the crawling process.
        StaleElementReferenceException: Pops up if an element has gone out of scope and skips it.
    """
    try:
        driver.get(url)
        
        wait = WebDriverWait(driver, 10)
        alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p","q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
        
        first_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'js-library-search-nav__browse-btn')))
        first_button.click()

        for letter in alphabet:
            letter_id = f"aab3c309-de3a-40a3-a565-007740a9633djs-{letter}"
            letter_xpath = f"//*[@id='{letter_id}']"

            second_button = wait.until(EC.element_to_be_clickable((By.XPATH, letter_xpath)))
            second_button.click()

            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.index-list-link')))

            elements = driver.find_elements(By.CSS_SELECTOR, '.index-list-link') # diseases 

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

            filename = f"crawled_data_{letter}.json"
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(crawled_data, file, ensure_ascii=False)
        
    except Exception as e:
        print('Error:', e)


def process_disease_page(url):
    """
    Process a specific disease page and extract relevant data.

    Args:
        url (str): The URL of the disease page.

    Returns:
        dict: The extracted data from the disease page.

    Raises:
        requests.exceptions.RequestException: If any error occurs during the HTTP request.
    """
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

geckodriver_path = './geckodriver'  

# KEEP IN MIND THIS IS FOR FIREFOX. MUST BE MODIFIED FOR CHROME OR OTHER BROWSERS 
firefox_options = Options()
firefox_options.add_argument('-headless')

service = Service(geckodriver_path)

driver = webdriver.Firefox(service=service, options=firefox_options)

starting_url = 'https://my.clevelandclinic.org/health/diseases'
crawl(starting_url)

print('done')
driver.quit()

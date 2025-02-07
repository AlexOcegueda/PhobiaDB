import requests
import pytest
import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from ClevelandClinicScrape.crawl import crawl

@pytest.mark.integration
def test_live_treatment_endpoint():
    url = "http://alexocegueda.pythonanywhere.com/treatments/Arachnophobia"
    response = requests.get(url)
    assert response.status_code == 200

    data = response.json()  
    assert isinstance(data, list), "Expected a JSON list from /treatments/<phobia_name>"

    assert "psychotherapy" in data, "Expected 'psychotherapy' in returned treatments"
    assert "exposure therapy" in data, "Expected 'exposure therapy' in returned treatments"

@pytest.mark.integration
def test_live_symptom_endpoint():
    """
    This test calls the live /symptoms/<phobia_name> endpoint hosted on PythonAnywhere.

    It verifies:
      - HTTP 200 status
      - The response is valid JSON (list)
      - The returned symptoms match our expectations for 'Arachnophobia'
    """
    url = "http://alexocegueda.pythonanywhere.com/symptoms/Arachnophobia"
    response = requests.get(url)
    assert response.status_code == 200, "Expected a 200 response from the live endpoint."

    symptoms_data = response.json()  
    assert isinstance(symptoms_data, list), "Expected a JSON list from /symptoms/<phobia_name>."

    expected_symptoms = {"panic attack", "chills", "rapid heartbeat", "lightheaded"}
    returned_symptoms = set(symptoms_data)
    for symptom in expected_symptoms:
        assert symptom in returned_symptoms, f"Expected '{symptom}' in the live endpoint response."

@pytest.mark.integration
def test_scraper_integration_live():
    """
    Live integration test for our web scraper.

    1. Spins up a real Firefox WebDriver (headless).
    2. Calls our `crawl()` function against the live Cleveland Clinic site.
    3. Checks if at least one JSON file got generated with data 
       that indicates the scraper worked.
    """

    # 1) Set up a headless driver (adjust if you use Chrome, etc.)
    options = Options()
    options.add_argument("-headless")
    driver = webdriver.Firefox(options=options)

    try:
        # 2) Call the real site
        start_url = "https://my.clevelandclinic.org/health/diseases"
        crawl(start_url, driver)

    finally:
        # 1) Quit the driver
        driver.quit()

    # Now outside the try/finally block, check if any file is non-empty:
    found_nonempty = False
    for letter in "abcdefghijklmnopqrstuvwxyz":
        filename = f"crawled_data_{letter}.json"
        if os.path.exists(filename):
            if os.path.getsize(filename) > 0:
                found_nonempty = True
                break

    assert found_nonempty, "Expected at least one non-empty JSON file..."

    # Now that we've confirmed at least one file was non-empty, do cleanup:
    for letter in "abcdefghijklmnopqrstuvwxyz":
        filename = f"crawled_data_{letter}.json"
        if os.path.exists(filename):
            os.remove(filename)
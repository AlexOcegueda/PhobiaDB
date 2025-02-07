
"""
Crawl and extract data from a ClevelandClinic.org about phobias. 

Author: Alex Ocegueda Castro
Version: 2.0
"""

import json
import requests
from bs4 import BeautifulSoup
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

def process_disease_page(url):
    """
    Return:
    {
      "name": "<phobia name from h1>",
      "description": "",
      "data": {
         "What is X?": "Answer text ...",
         "How is X treated?": "Answer text ...",
         ...
      }
    }
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # 1) Disease name from <h1>
        h1 = soup.find("h1")
        name = h1.get_text(strip=True) if h1 else "No Name Found"

        # 2) We skip description now
        description = ""

        # 3) Q&A dict
        data = {}

        # 4) Grab elements that might hold Q/A content:
        #    - We'll look at <h3> for questions
        #    - We'll gather <p> / <ul> for the answers
        content_elements = soup.find_all(["h3", "p", "ul"])

        current_question = None
        current_answer_parts = []

        def save_question_answer(q, answers):
            if not q:
                return
            joined_answer = " ".join(answers).strip()
            data[q] = joined_answer

        for elem in content_elements:
            text = elem.get_text(strip=True)

            # If it's an h3 that ends with '?', treat it as a new question
            if elem.name == "h3" and text.endswith("?"):
                # If we were building an answer for a previous question, save it
                if current_question:
                    save_question_answer(current_question, current_answer_parts)

                # Start a new question
                current_question = text
                current_answer_parts = []

            elif current_question and elem.name == "p":
                current_answer_parts.append(text)

            elif current_question and elem.name == "ul":
                for li in elem.find_all("li", recursive=False):
                    li_text = li.get_text(strip=True)
                    if li_text:
                        current_answer_parts.append(li_text)

        # 5) End: if there's a question still open, save it
        if current_question:
            save_question_answer(current_question, current_answer_parts)

        # 6) Return final dictionary
        return {
            "name": name,
            "description": description,
            "data": data
        }

    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return {"name": "", "description": "", "data": {}}


def crawl(url, driver):
    """
    Crawl Cleveland Clinic letters A-Z (or just letter 'a'), looking for ANY <a> 
    whose href contains "/health/diseases/". Then check if "phobia" appears in 
    that href. If so, call `process_disease_page()` and save results to JSON.
    """
    try:
        wait = WebDriverWait(driver, 10)
        driver.get(url)

        # If you only want letter A for now, keep it as ["a"].
        # Otherwise, use list("abcdefghijklmnopqrstuvwxyz") for all letters.
        alphabet = list("abcdefghijklmnopqrstuvwxyz")

        for letter in alphabet:
            letter_upper = letter.upper()

            # 1) Click the letter link by text (e.g., "A")
            letter_link = wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, letter_upper))
            )
            letter_link.click()

            # 2) Give the site a moment to load results
            time.sleep(2)

            # 3) WAIT for at least one anchor containing "/health/diseases/" to appear
            wait.until(
                lambda d: len(
                    d.find_elements(By.CSS_SELECTOR, 'a[href*="/health/diseases/"]')
                ) > 0
            )

            # 4) Collect all <a> whose href has "/health/diseases/"
            disease_anchors = driver.find_elements(
                By.CSS_SELECTOR, 'a[href*="/health/diseases/"]'
            )

            crawled_data = []

            # 5) For each anchor, check if URL has "phobia", then scrape it
            for anchor in disease_anchors:
                try:
                    href = anchor.get_attribute("href")
                    
                    # If the URL (href) contains "phobia", we consider it a match
                    if "phobia" in href.lower():
                        result = process_disease_page(href)
                        crawled_data.append(result)

                except StaleElementReferenceException:
                    # If the element went stale, skip
                    continue
                except Exception as ex:
                    # Any other error while extracting data from a card
                    print(f"Could not extract data from an anchor: {ex}")
                    continue

            # 6) Save JSON for this letter
            filename = f"crawled_data_{letter}.json"
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(crawled_data, f, ensure_ascii=False)

    except Exception as e:
        print("Error in crawl():", e)

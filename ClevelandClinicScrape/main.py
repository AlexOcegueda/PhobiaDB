# main.py

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

from crawl import crawl

if __name__ == "__main__":

    firefox_options = Options()
    firefox_options.add_argument('-headless')

    service = Service("/usr/local/bin/geckodriver") # assumes your gecko driver is global on your PC
    driver = webdriver.Firefox(service=service, options=firefox_options)

    try:
        starting_url = "https://my.clevelandclinic.org/health/diseases"
        crawl(starting_url, driver)
    finally:
        driver.quit()

    print("Done scraping!")

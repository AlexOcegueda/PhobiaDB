# ClevelandClinicScrape
  - Description: This returns A-Z of phobias in the diseases section of Cleveland Clinic. https://my.clevelandclinic.org/health/diseases
  - It is made to use with geckodriver (firefox) but you can refractor the driver to use chrome if you prefer using that browser instead
      - Just make sure to get the appropriate version which matches with your python version
      - I recommend using a python virtual environment to setup all the dependencies to avoid messing with your global settings if you do encounter issues with             geckodriver
      - Also putting your driver in the same directory will make linking it up easier. You must change the path to your driver in the code.

# PhobiaDB
These are scripts I used to fill up my Postgresql DB with all the data I collected.

# WikipediaPhobias
  - Containers a web scraper to retrieve a table of phobias along with their description.
  - Simply run python3 main.py while you are in the correct folder and it should return a JSON file


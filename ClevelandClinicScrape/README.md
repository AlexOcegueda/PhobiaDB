
Questions.py is the data used to upload the questions and their answers to the database
Data.py is used to upload symptoms and treatments.
Sentence.py was used for data and rename.py was used for questions.
phrases.py extracts phrases ranked on top sentences from paragraphs
chunk.py searchs for specific parts of speech to extract keywords and phrases
rank.py is used to see the importance of each sentence and split them up

## ClevelandClinicScrape
  - Description: This returns A-Z of phobias in the diseases section of Cleveland Clinic. https://my.clevelandclinic.org/health/diseases
  - It is made to use with geckodriver (firefox) but you can refractor the driver to use chrome if you prefer using that browser instead
      - Just make sure to get the appropriate version which matches with your python version
      - I recommend using a python virtual environment to setup all the dependencies to avoid messing with your global settings if you do encounter issues with             geckodriver
      - Also putting your driver in the same directory will make linking it up easier. You must change the path to your driver in the code.

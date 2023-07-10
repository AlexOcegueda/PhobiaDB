import requests
from bs4 import BeautifulSoup
import json
import re

url = 'https://en.wikipedia.org/wiki/List_of_phobias'
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')
trs = soup.find_all('tr')
data = []

for tr in trs:
    # Extract the first word before the word "fear"
    fear_index = tr.text.find('fear')
    if fear_index != -1:
        first_word = tr.text[:fear_index].strip()
    else:
        continue

    # Remove newline characters, \u, and \n from the rest of the content
    rest_of_content = re.sub(r'\n+', ' ', tr.text[fear_index+4:].strip())
    cleaned_content = re.sub(r'\\[un]', '', rest_of_content)

    # Remove brackets with numbers
    cleaned_content = re.sub(r'\[[0-9]+\]', '', cleaned_content)

    full_content = f"fear {cleaned_content}"

    tr_dict = {"name": first_word, "description": full_content, "symptoms": "", 
               "causes": "", "treatments": "", "images": ""}
    data.append(tr_dict)

with open('data.json', 'w') as f:
    json.dump(data, f)

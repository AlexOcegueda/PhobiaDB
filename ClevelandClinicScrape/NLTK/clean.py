# Cleans JSON data for use
# Programmer: Alex Ocegueda Castro 

import os
import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag

stop_words = set(stopwords.words('english'))

def extract_keywords_and_phrases(text):
    """
    Extracts keywords and phrases from a given text.

    Args:
        text (str): The input text to extract keywords and phrases from.

    Returns:
        tuple: A tuple containing the extracted keywords, tagged tokens, and phrases.
    """
    tokens = word_tokenize(text.lower())

    # Remove stopwords and punctuation
    keywords = [word for word in tokens if word.isalpha() and word not in stop_words]

    tagged_tokens = pos_tag(tokens)

    phrases = []
    current_phrase = []

    for token, tag in tagged_tokens:
        if tag.startswith('NN'):
            current_phrase.append(token)
        else:
            if current_phrase:
                phrases.append(' '.join(current_phrase))
                current_phrase = []

    if current_phrase:
        phrases.append(' '.join(current_phrase))

    return keywords, tagged_tokens, phrases

folder_path = "./test/easyread"  

for filename in os.listdir(folder_path):
    if filename.endswith(".json"):
        file_path = os.path.join(folder_path, filename)

        with open(file_path, 'r') as file:
            data = json.load(file)

        processed_data = []

        for item in data:
            data_dict = item
            for section in data_dict['data']:
                for i in range(len(data_dict['data'][section]['items'])):
                    item_text = data_dict['data'][section]['items'][i]
                    keywords, tagged_tokens, phrases = extract_keywords_and_phrases(item_text)
                    data_dict['data'][section]['items'][i] = {
                        'keywords': keywords,
                        'tagged_tokens': tagged_tokens,
                        'phrases': phrases
                    }

            processed_data.append(data_dict)

        output_file_path = os.path.join(folder_path, f"processed_{filename}")
        with open(output_file_path, 'w') as file:
            json.dump(processed_data, file, indent=4)

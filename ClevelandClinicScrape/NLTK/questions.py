# Question extraction
# Programmer Alex Ocegueda Castro

import json
import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from rake_nltk import Rake

def remove_stopwords_and_tokenize(text):
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(text.lower())
    filtered_tokens = [word for word in tokens if word.isalnum() and word not in stop_words]
    return filtered_tokens

def extract_rake_keywords(text):
    r = Rake()
    r.extract_keywords_from_text(text)
    keywords = r.get_ranked_phrases()[:7]  # Change the number to get desired top keywords
    return keywords

def copy_and_restructure_json(input_folder_path, output_folder_path):
    """
    Copies JSON files from the input folder to the output folder and restructures the data.

    Args:
        input_folder_path (str): Path to the folder containing the input JSON files.
        output_folder_path (str): Path to the folder to store the output JSON files.

    Returns:
        None
    """
    os.makedirs(output_folder_path, exist_ok=True)

    for filename in os.listdir(input_folder_path):
        if filename.endswith(".json"):
            input_file_path = os.path.join(input_folder_path, filename)

            with open(input_file_path, 'r') as file:
                data = json.load(file)

            output_data = []

            for item in data:
                phobia_name = item['name']
                name_only = phobia_name.split()[0].lower()
                description = item['description']
                new_item = {'name': phobia_name, 'description': description, 'data': {}}

                for question, content in item['data'].items():
                    if question not in ["What are phobias?", "What is a phobia?", "Related Institutes & Services"]:
                        new_item['data'][question] = ' '.join(content['items'])  # Convert array to a single string

                output_data.append(new_item)

            output_file_path = os.path.join(output_folder_path, filename)
            with open(output_file_path, 'w') as outfile:
                json.dump(output_data, outfile, indent=4)

            print(f"JSON file copied and restructured. Output file: {output_file_path}")

input_folder_path = '../BackupData'  # Replace with the path to your input folder containing JSON files
output_folder_path = '../questions'  # Replace with the desired path to store the output JSON files

copy_and_restructure_json(input_folder_path, output_folder_path)

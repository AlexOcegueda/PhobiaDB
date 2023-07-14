import json
import os
import shutil
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
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
                new_item = {'name': phobia_name, 'description': description}

                for question, content in item['data'].items():
                    if question not in ["What are phobias?", "What is a phobia?", "Related Institutes & Services"]:
                        new_item[question] = ' '.join(content['items'])  # Convert array to a single string
                        if question.lower() in [
                            # symptoms, treatment, cope
                            f"what are {name_only} symptoms?",
                            f"what are the symptoms of {name_only}?",
                            f"what are the signs and symptoms of {name_only}?",
                            f"what is {name_only} treatment like?",
                            f"how is {name_only} treated?",
                            f"what triggers {name_only}?",
                            f"what is the outlook for people with {name_only}?",
                            f"how can I best learn to cope with {name_only}?"]:
                            
                            words = remove_stopwords_and_tokenize(new_item[question])
                            new_item[question] = extract_rake_keywords(' '.join(words))

                output_data.append(new_item)

            output_file_path = os.path.join(output_folder_path, filename)
            with open(output_file_path, 'w') as outfile:
                json.dump(output_data, outfile, indent=4)

            print(f"JSON file copied and restructured. Output file: {output_file_path}")


# Example usage
input_folder_path = '../BackupData'  # Replace with the path to your input folder containing JSON files
output_folder_path = '../questions'  # Replace with the desired path to store the output JSON files

copy_and_restructure_json(input_folder_path, output_folder_path)

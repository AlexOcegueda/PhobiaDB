# Keyword extraction
# Programmer: Alex Ocegueda Castro

import json
import os
import nltk
from nltk.corpus import stopwords
from rake_nltk import Rake

def process_json_files(input_folder_path, output_folder_path):
    """
    Processes a folder of JSON files by performing keyword extraction of specific medical terms
    for symptoms and treatments of specific phobias. After this it outputs a new JSON file for 
    each file in the folder specified.

    Args:
        input_folder_path (str): Path to the folder containing the input JSON files.
        output_folder_path (str): Path to the folder to store the output JSON files.

    Returns:
        None
    """
    os.makedirs(output_folder_path, exist_ok=True)

    # Initialize the RAKE algorithm
    rake = Rake()

    keywords_to_check = [
        "excessive sweating",
        "hyperventilation",
        "panic attack",
        "fear and anxiety",
        "desire to escape",
        "rapid heartbeat",
        "dizzy",
        "lightheaded",
        "feeling queasy",
        "trembling",
        "nausea",
        "shortness of breath",
        "heart palpitations",
        "upset stomach or indigestion",
        "chills",

        "virtual reality",
        "exposure therapy",
        "cognitive behavior therapy",
        "psychotherapy",
        "medication",
        "lifestyle changes",
    ]

    for filename in os.listdir(input_folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(input_folder_path, filename)

            with open(file_path, 'r') as file:
                data = json.load(file)

            output_data = []

            for item in data:
                new_item = {"name": item["name"], "description": item["description"]}
                for heading, content in item['data'].items():
                    sentences = []
                    keywords = []
                    phobia_name = item['name'].split()[0].lower()
                    if heading not in ["What are phobias?", "What is a phobia?", "Related Institutes & Services"]:
                        new_item[heading] = ' '.join(content['items'])  # Convert array to a single string
                        new_item[heading] = {'keywords': []}  # Initialize as dictionary
                        
                        if heading.lower() in [
                            # symptoms, treatment, cope
                            f"what are {phobia_name} symptoms?",
                            f"what are the symptoms of {phobia_name}?",
                            f"what are the signs and symptoms of {phobia_name}?",
                            f"what are the treatments for {phobia_name}?",
                            f"what is {phobia_name} treatment?",
                            f"what is {phobia_name} treatment like?",
                            f"how is {phobia_name} treated?",
                            f"what are {phobia_name} treatments?",
                            f"how is {phobia_name} managed or treated?",
                            f"how do i manage or treat {phobia_name}?",
                            f"how do you treat {phobia_name}?",
                            f"how can i overcome {phobia_name}?",
                            f"can other treatments help me cope with mysophobia?",
                            f"how do providers treat {phobia_name}?",
                            f"what are ways to treat pedophobia?",

                            # edge cases 
                            "what are autophobia (monophobia) symptoms?",
                            "what are the symptoms of snake phobia?",

                            "what is the treatment for autophobia (monophobia)?",
                            "how do you treat fear of knees?",
                            "how do i get over a fear of snakes?",
                            "how are phobias treated, and can they be cured?"

                            ]:
                            for paragraph in content['items']:
                                paragraph_sentences = nltk.sent_tokenize(paragraph)
                                sentences.extend(paragraph_sentences)
                                rake.extract_keywords_from_text(paragraph)
                                extracted_keywords = rake.get_ranked_phrases()[:5]  # Adjust the number of keywords to extract
                                filtered_keywords = [kw for kw in keywords_to_check if any(kw.lower() in sentence.lower() for sentence in paragraph_sentences)]
                                keywords.extend(filtered_keywords)

                            # Remove duplicates from keywords
                            keywords = list(set(keywords))

                            new_item[heading]['keywords'] = keywords
                output_data.append(new_item)

            output_file = os.path.join(output_folder_path, f"{os.path.splitext(filename)[0]}.json")

            with open(output_file, 'w') as outfile:
                json.dump(output_data, outfile, indent=4)

            print(f"Sentence tokenization and keyword extraction complete. Output file: {output_file}")


input_folder_path = '../BackupData'  # Replace with the path to your folder containing input JSON files
output_folder_path = '../datas'  # Replace with the desired path to store the output JSON files

process_json_files(input_folder_path, output_folder_path)

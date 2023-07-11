import json
import nltk
import string
import os

# Sentence Tokenization and Punctuation Removal
# Programmer: Alex Ocegueda Castro

def process_json_files(folder_path):
    """
    Processes a folder of JSON files by performing sentence tokenization, punctuation removal,
    and outputs a new JSON file for each file in the folder.

    Args:
        folder_path (str): Path to the folder containing the JSON files.

    Returns:
        None
    """
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)

            with open(file_path, 'r') as file:
                data = json.load(file)

            output_data = []

            for item in data:
                new_item = {"name": item["name"], "description": item["description"], "data": {}}
                for heading, content in item['data'].items():
                    sentences = []
                    for paragraph in content['items']:
                        # Tokenize the paragraph into sentences
                        paragraph_sentences = nltk.sent_tokenize(paragraph)
                        # Remove punctuation and "\u2019" from each sentence
                        cleaned_sentences = []
                        for sentence in paragraph_sentences:
                            cleaned_sentence = sentence.translate(str.maketrans("", "", string.punctuation))
                            cleaned_sentence = cleaned_sentence.replace("\u2019", "")
                            cleaned_sentences.append(cleaned_sentence)
                        sentences.extend(cleaned_sentences)
                    new_item["data"][heading] = {"items": sentences}
                output_data.append(new_item)

            # Generate the output file path based on the input file name
            output_file = os.path.splitext(file_path)[0] + '_output.json'

            # Write the output data to the JSON file
            with open(output_file, 'w') as outfile:
                json.dump(output_data, outfile, indent=4)

            print(f"Sentence tokenization complete. Output file: {output_file}")


# Example usage
folder_path = '../data'  # Replace with the path to your folder containing JSON files
process_json_files(folder_path)

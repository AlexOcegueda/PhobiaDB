# Ranks sentences on importance
# Programmer: Alex Ocegueda Castro


import json
import os
from transformers import pipeline
from nltk.tokenize import sent_tokenize

def process_json_files(input_folder_path, output_folder_path):
    """
    Processes a folder of JSON files by performing sentence ranking and outputs a new JSON file
    for each file in the folder.

    Args:
        input_folder_path (str): Path to the folder containing the input JSON files.
        output_folder_path (str): Path to the folder to store the output JSON files.

    Returns:
        None
    """
    os.makedirs(output_folder_path, exist_ok=True)

    # Initialize the BART-based model for sentence ranking
    model_name = "facebook/bart-large-cnn"
    sentence_ranker = pipeline("text2text-generation", model=model_name)

    # Define the number of top sentences to select
    top_sentences = 1

    for filename in os.listdir(input_folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(input_folder_path, filename)

            with open(file_path, 'r') as file:
                data = json.load(file)

            ranked_data = []

            for item in data:
                phobia_name = item['name']
                description = item['description']
                ranked_item = {'name': phobia_name, 'description': description, 'data': {}}

                for question, sentences in item.items():
                    if question not in ['name', 'description']:
                        ranked_sentences = []
                        # Combine the sentences into a single text
                        text = ' '.join(sentences)
                        # Tokenize the text into sentences
                        tokenized_sentences = sent_tokenize(text)

                        # Rank the sentences using the BART-based model
                        ranked_sentences = sentence_ranker(text, max_length=60, min_length=40,
                                                           num_return_sequences=top_sentences)

                        # Extract the top-ranked sentences
                        top_ranked_sentences = []
                        selected_sentences = set()
                        for ranked_sentence in ranked_sentences:
                            generated_sentence = ranked_sentence['generated_text']
                            # Check if the generated sentence is already selected
                            if generated_sentence not in selected_sentences:
                                top_ranked_sentences.append(generated_sentence)
                                selected_sentences.add(generated_sentence)
                            # Check if we have already selected two sentences
                            if len(top_ranked_sentences) == top_sentences:
                                break

                        ranked_item['data'][question] = top_ranked_sentences

                # Add the ranked item to the list
                ranked_data.append(ranked_item)

            output_file = os.path.join(output_folder_path, f"{os.path.splitext(filename)[0]}.json")

            with open(output_file, 'w') as outfile:
                json.dump(ranked_data, outfile, indent=4)

            print(f"Sentence ranking complete. Output file: {output_file}")


# Example usage
input_folder_path = '../NLTK/test2'  # Replace with the path to your input folder containing JSON files
output_folder_path = '../Processed_data'  # Replace with the desired path to store the processed JSON files

process_json_files(input_folder_path, output_folder_path)

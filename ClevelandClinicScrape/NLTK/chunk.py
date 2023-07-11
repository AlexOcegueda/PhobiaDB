# Extract Phrases from JSON Data
# Programmer: Alex Ocegueda Castro

import json
import nltk
import os
from nltk.chunk import RegexpParser

# chunking pattern for extracting phrases
chunk_pattern = r"""
    Chunk:  {<NN.*><.*>*<JJ.*>*<VB.*>*}
            {<W.*><.*>{0,2}?<VB.*><.*>{0,2}?<NN.*>}
            {<W.*><.*>{0,2}?<VB.*><.*>{0,2}?<JJ.*>*<NN.*>}
            {<W.*><VBZ><.*>{0,2}?<NN.*>}
"""

def process_json_file(input_file, output_file):
    """
    Extracts phrases from a JSON file and writes the extracted phrases to another JSON file.

    Args:
        input_file (str): Path to the input JSON file.
        output_file (str): Path to the output JSON file.

    Returns:
        None
    """
    if os.path.exists(input_file):
        # Load JSON data from the input file
        with open(input_file, 'r') as file:
            data = json.load(file)

        extracted_phrases = []

        for item in data:
            if 'data' in item:
                extracted_item = {'name': item['name'], 'description': item['description'], 'data': {}}
                for key, value in item['data'].items():
                    if 'items' in value and isinstance(value['items'], list):
                        items = value['items']
                        extracted_items = []
                        for item_text in items:
                            # Perform part-of-speech tagging on the item text
                            tagged_tokens = nltk.pos_tag(nltk.word_tokenize(item_text))

                            # Chunk the tagged tokens using the defined pattern
                            chunk_parser = RegexpParser(chunk_pattern)
                            parsed_tree = chunk_parser.parse(tagged_tokens)

                            # Extract phrases from the parsed tree
                            for subtree in parsed_tree.subtrees():
                                if subtree.label() == 'Chunk':
                                    phrase_tokens = [token for token, _ in subtree.leaves()]
                                    phrase = ' '.join(phrase_tokens)
                                    extracted_items.append(phrase)

                        extracted_item['data'][key] = extracted_items

                extracted_phrases.append(extracted_item)

        if os.path.exists(output_file):
            with open(output_file, 'r') as file:
                existing_data = json.load(file)

            if isinstance(existing_data, list):
                existing_data.extend(extracted_phrases)

            extracted_phrases = existing_data

        # Write extracted phrases to the output JSON file
        with open(output_file, 'w') as outfile:
            json.dump(extracted_phrases, outfile, indent=4)

        print("Extraction complete. Output file:", output_file)
    else:
        print("Input file does not exist.")


# Example usage
input_json_file = './test/testa.json'
output_json_file = './test/testa_output.json'
process_json_file(input_json_file, output_json_file)

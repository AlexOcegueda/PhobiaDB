# Phrase Extraction from Tagged Tokens
# Programmer: Alex Ocegueda Castro 

import json
from nltk import pos_tag

def extract_phrases(tagged_tokens):
    """
    Extracts phrases from a list of tagged tokens.

    Args:
        tagged_tokens (list): A list of tuples containing token and corresponding POS tag.

    Returns:
        list: A list of extracted phrases.
    """
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

    return phrases

# Load and process the JSON data
with open('./test/processed_crawled_data_a.json', 'r') as file:
    data = json.load(file)

phrases = []

for item in data:
    for section in item['data']:
        for i in range(len(item['data'][section]['items'])):
            tagged_tokens = item['data'][section]['items'][i]['tagged_tokens']
            item_phrases = extract_phrases(tagged_tokens)
            phrases.extend(item_phrases)

output_data = {
    'phrases': phrases
}

# Write the data to a new JSON file
output_file_path = 'output.json'
with open(output_file_path, 'w') as file:
    json.dump(output_data, file, indent=4)

print(f"Phrases are written to {output_file_path}.")

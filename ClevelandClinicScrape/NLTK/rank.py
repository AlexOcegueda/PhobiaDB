import json
from gensim.summarization import summarize

# Load the JSON data
with open('sentences_output.json', 'r') as file:
    data = json.load(file)

# Extract sentences from the JSON data
sentences = []
for item in data:
    for _, content in item['data'].items():
        sentences.extend(content['items'])

# Convert the sentences to a single string
text = ' '.join(sentences)

# Apply TextRank to get the top-ranked sentences
summary = summarize(text, ratio=0.2)  # Adjust the ratio as needed

# Create a new JSON object for the summary
summary_data = {
    'summary': summary
}

# Generate the output file path for the summary
output_file = 'summary_output.json'

# Write the summary data to the JSON file
with open(output_file, 'w') as outfile:
    json.dump(summary_data, outfile, indent=4)

print("Summary generation complete. Output file:", output_file)

import json
import psycopg2

# Load the data from the JSON file
with open('data.json', 'r') as file:
    data = json.load(file)

# Establish a connection to the PostgreSQL database
conn = psycopg2.connect(
    host='your_host',
    port='your_port',
    database='your_database',
    user='your_username',
    password='your_password'
)
cursor = conn.cursor()

# Create the "phobias" table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS phobias (
        id SERIAL PRIMARY KEY,
        name TEXT,
        description TEXT,
        symptoms TEXT,
        causes TEXT,
        treatments TEXT,
        images TEXT
    )
''')

# Insert the data into the "phobias" table
for item in data:
    name = item['name']
    description = item['description']
    symptoms = item['symptoms']
    causes = item['causes']
    treatments = item['treatments']
    images = item['images']

    cursor.execute('''
        INSERT INTO phobias (name, description, symptoms, causes, treatments, images)
        VALUES (%s, %s, %s, %s, %s, %s)
    ''', (name, description, symptoms, causes, treatments, images))

# Commit the changes and close the connection
conn.commit()
conn.close()

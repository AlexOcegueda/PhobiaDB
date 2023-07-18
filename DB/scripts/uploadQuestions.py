import sqlite3
import json
import os

conn = sqlite3.connect('phobias.db')
conn.execute('''CREATE TABLE IF NOT EXISTS phobias
                (id INTEGER PRIMARY KEY, name TEXT, description TEXT, data TEXT)''')

folder_path = '../questions'  # Specify the path to the folder containing JSON files

for file_name in os.listdir(folder_path):
    if file_name.endswith('.json'):
        file_path = os.path.join(folder_path, file_name)

        with open(file_path, 'r') as file:
            try:
                data = json.load(file)

                for phobia in data:
                    phobia_name = phobia["name"]
                    phobia_description = phobia["description"]
                    phobia_data = json.dumps(phobia.get("data", {}))

                    # Check if phobia already exists in the database
                    cursor = conn.execute("SELECT id FROM phobias WHERE name=?", (phobia_name,))
                    existing_phobia = cursor.fetchone()

                    if existing_phobia:
                        # Phobia already exists, update the data
                        phobia_id = existing_phobia[0]
                        conn.execute('UPDATE phobias SET name=?, description=?, data=? WHERE id=?',
                                     (phobia_name, phobia_description, phobia_data, phobia_id))
                    else:
                        # Phobia does not exist, insert a new row
                        conn.execute('INSERT INTO phobias (name, description, data) VALUES (?, ?, ?)',
                                     (phobia_name, phobia_description, phobia_data))

            except (ValueError, KeyError):
                print(f"Invalid JSON format in file: {file_path}")

conn.commit()
conn.close()

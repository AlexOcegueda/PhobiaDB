import sqlite3
import json
import os

conn = sqlite3.connect('phobias.db')
cursor = conn.cursor()

junctions = []
def create_junction_table():
    # Create the 'phobia_symptom_treatment' junction table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS phobia_symptom_treatment (
            phobia_id INTEGER,
            symptom_id INTEGER,
            treatment_id INTEGER,
            FOREIGN KEY (phobia_id) REFERENCES phobias (id),
            FOREIGN KEY (symptom_id) REFERENCES symptoms (id),
            FOREIGN KEY (treatment_id) REFERENCES treatments (id)
        )
    ''')

def insert_junction_data(json_folder):
    # Iterate through the JSON files in the specified folder
    for file_name in os.listdir(json_folder):
        if file_name.endswith('.json'):
            file_path = os.path.join(json_folder, file_name)

            # Load the phobia, symptom, and treatment data from the JSON file
            with open(file_path, 'r') as file:
                data = json.load(file)

                for phobia_data in data: # goes through init list of phobias
                    phobia_full_name = phobia_data['name']
                    phobia_id = cursor.execute('SELECT id FROM phobias WHERE name = ?', (phobia_full_name,)).fetchone()[0]
                    phobia_name = phobia_full_name.split()[0].lower()
                    symptoms = []
                    treatments = []
                    # Every question in this phobia
                    for question in phobia_data.keys():
                        if question.lower() in [f'what are {phobia_name} symptoms?',
                                        f'what are the symptoms of {phobia_name}?',
                                        f'what are the signs and symptoms of {phobia_name}?',
                                        'what are autophobia (monophobia) symptoms?',
                                        'what are the symptoms of snake phobia?']:
                            
                            symptom_data = phobia_data[question]
                            if 'keywords' in symptom_data:
                                symptom_keywords = symptom_data['keywords']
                                for keyword in symptom_keywords:
                                    try:
                                        symptom_id = cursor.execute('SELECT id FROM symptoms WHERE symptom = ?', (keyword,)).fetchone()[0]
                                        #cursor.execute('INSERT INTO phobia_symptom_treatment (phobia_id, symptom_id) VALUES (?, ?)', (phobia_id, symptom_id))
                                        symptoms.append(symptom_id)
                                    except TypeError:
                                        print("couldn't find", keyword)

                        if question.lower() in [f"what are the treatments for {phobia_name}?",
                                        f"what is {phobia_name} treatment?",
                                        f"what is {phobia_name} treatment like?",
                                        f"how is {phobia_name} treated?",
                                        f"what are {phobia_name} treatments?",
                                        f"how is {phobia_name} managed or treated?",
                                        f"how do i manage or treat {phobia_name}?",
                                        f"how do you treat {phobia_name}?",
                                        f"how can i overcome {phobia_name}?",
                                        f"can other treatments help me cope with {phobia_name}?",
                                        f"how do providers treat {phobia_name}?",
                                        f"what are ways to treat {phobia_name}?",
                                        "what is the treatment for autophobia (monophobia)?",
                                        "how do you treat fear of knees?",
                                        "how do i get over a fear of snakes?",
                                        "how are phobias treated, and can they be cured?"]:
                            treatment_data = phobia_data[question]
                            if 'keywords' in treatment_data:
                                treatment_keywords = treatment_data['keywords']
                                for keyword in treatment_keywords:
                                    try:
                                        treatment_id = cursor.execute('SELECT id FROM treatments WHERE treatment = ?', (keyword,)).fetchone()[0]
                                        #cursor.execute('INSERT INTO phobia_symptom_treatment (phobia_id, treatment_id) VALUES (?, ?)', (phobia_id, treatment_id))
                                        treatments.append(treatment_id)
                                    except TypeError:
                                        print('Treatment not found', keyword)
                                        continue
                    
                    print("s: ",symptoms)
                    print("t: ",treatments)
                    

                    for s_id in symptoms:
                        for t_id in treatments:
                            temp = [phobia_id, s_id, t_id]
                            junctions.append(temp)
                    


def main():
    create_junction_table()

    json_folder = './symptoms'  # Specify the path to the folder containing JSON files
    insert_junction_data(json_folder)

    for junction in junctions:
        phobia_id, symptom_id ,treatment_id = junction # phobia_id, symptom_id, treatment_id
        cursor.execute('INSERT INTO phobia_symptom_treatment (phobia_id, symptom_id, treatment_id) VALUES (?, ?, ?)', (phobia_id, symptom_id, treatment_id))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()

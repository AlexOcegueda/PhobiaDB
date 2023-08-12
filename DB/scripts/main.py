from flask import Flask, render_template, request, g
import sqlite3
import json

app = Flask(__name__)

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('phobias.db')
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pass

    # Fetch all phobias from the database in alphabetical order
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT name, brief_description FROM phobias ORDER BY name')  # Modify the query to select brief_description
    phobia_info = [(row['name'], row['brief_description']) for row in cursor.fetchall()]  # Fetch name and brief_description
    return render_template('index.html', phobia_info=phobia_info)  # Pass phobia_info to the template


@app.route('/phobia/<phobia_name>', methods=['GET'])
def get_phobia_details(phobia_name):
    db = get_db()
    cursor = db.cursor()

    cursor.execute('''
        SELECT phobias.name, phobias.description, phobias.brief_description, symptoms.symptom, treatments.treatment
        FROM phobia_symptom_treatment
        JOIN symptoms ON phobia_symptom_treatment.symptom_id = symptoms.id
        JOIN treatments ON phobia_symptom_treatment.treatment_id = treatments.id
        JOIN phobias ON phobia_symptom_treatment.phobia_id = phobias.id
        WHERE phobias.name = ?
    ''', (phobia_name,))
    rows = cursor.fetchall()

    if rows:
        phobia_name = rows[0]['name']
        description = rows[0]['description']
        brief_description = rows[0]['brief_description'] 

        symptoms_set = set()
        treatments_set = set()

        for row in rows:
            symptoms_set.add(row['symptom'])
            treatments_set.add(row['treatment'])

        symptoms_str = ', '.join(symptoms_set)
        treatments_str = ', '.join(treatments_set)

        return render_template('phobia_details.html', phobia_name=phobia_name, description=description,
                               brief_description=brief_description,  
                               symptoms_str=symptoms_str, treatments_str=treatments_str)
    
    else:
        return '<p>Phobia not found.</p>'

@app.route('/phobia_symptom_treatment', methods=['GET'])
def display_phobia_symptom_treatment():
    db = get_db()
    cursor = db.cursor()

    cursor.execute('''
    SELECT phobias.name AS phobia, symptoms.symptom, treatments.treatment
    FROM phobia_symptom_treatment
    JOIN phobias ON phobia_symptom_treatment.phobia_id = phobias.id
    JOIN symptoms ON phobia_symptom_treatment.symptom_id = symptoms.id
    JOIN treatments ON phobia_symptom_treatment.treatment_id = treatments.id
    ORDER BY phobias.name
    ''')

    # Fetch all rows and store them in a list of dictionaries
    rows = cursor.fetchall()

    if rows:
        phobia_details = {}
        for row in rows:
            phobia_name = row['phobia']
            symptom = row['symptom']
            treatment = row['treatment']

            if phobia_name not in phobia_details:
                phobia_details[phobia_name] = {
                    'symptoms': set(),
                    'treatments': set()
                }

            phobia_details[phobia_name]['symptoms'].add(symptom)
            phobia_details[phobia_name]['treatments'].add(treatment)

        formatted_details = []
        for phobia_name, data in phobia_details.items():
            formatted_details.append({
                'phobia_name': phobia_name,
                'symptoms': ', '.join(data['symptoms']),
                'treatments': ', '.join(data['treatments'])
            })

        return render_template('phobia_symptom_treatment.html', phobia_details=formatted_details)
    else:
        return '<p>No data found.</p>'

@app.route('/treatments/<phobia_name>', methods=['GET'])
def get_phobia_treatments(phobia_name):
    db = get_db()
    cursor = db.cursor()

    # Convert the input phobia_name to lowercase before querying the database
    phobia_name_lower = phobia_name.lower()

    cursor.execute('''
        SELECT treatments.treatment
        FROM phobia_symptom_treatment
        JOIN treatments ON phobia_symptom_treatment.treatment_id = treatments.id
        JOIN phobias ON phobia_symptom_treatment.phobia_id = phobias.id
        WHERE LOWER(phobias.name) = ?
    ''', (phobia_name_lower,))
    rows = cursor.fetchall()

    treatments_set = set()

    for row in rows:
        treatments_set.add(row['treatment'])

    treatments_list = list(treatments_set)

    return json.dumps(treatments_list)

@app.route('/symptoms/<phobia_name>', methods=['GET'])
def get_phobia_symptoms(phobia_name):
    db = get_db()
    cursor = db.cursor()

    # Convert the input phobia_name to lowercase before querying the database
    phobia_name_lower = phobia_name.lower()

    cursor.execute('''
        SELECT symptoms.symptom
        FROM phobia_symptom_treatment
        JOIN symptoms ON phobia_symptom_treatment.symptom_id = symptoms.id
        JOIN phobias ON phobia_symptom_treatment.phobia_id = phobias.id
        WHERE LOWER(phobias.name) = ?
    ''', (phobia_name_lower,))
    rows = cursor.fetchall()

    symptoms_set = set()

    for row in rows:
        symptoms_set.add(row['symptom'])

    symptoms_list = list(symptoms_set)

    return json.dumps(symptoms_list)

def index():
    if request.method == 'POST':
        pass

    # Fetch all phobias from the database in alphabetical order
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT name, brief_description FROM phobias ORDER BY name')  
    phobia_info = [(row['name'], row['brief_description']) for row in cursor.fetchall()]  
    return render_template('index.html', phobia_info=phobia_info)  

@app.route('/documentation', methods=['GET'])
def documentation():
    return render_template('documentation.html')

if __name__ == "__main__":
    app.run(debug=True)

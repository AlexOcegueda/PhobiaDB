import sqlite3

conn = sqlite3.connect('phobias.db')  
cursor = conn.cursor()  

def create_symptoms_table():
    """
    Create the 'symptoms' table and insert symptom data.

    The 'symptoms' table has columns 'id' (auto-incrementing primary key) and 'symptom' (text).

    Returns:
        None
    """
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS symptoms (
            id INTEGER PRIMARY KEY,
            symptom TEXT
        )
    ''')

    symptoms = [
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
        "chills"
    ]

    for symptom in symptoms:
        cursor.execute('INSERT INTO symptoms (symptom) VALUES (?)', (symptom,))

def create_treatments_table():
    """
    Create the 'treatments' table and insert treatment data.

    The 'treatments' table has columns 'id' (auto-incrementing primary key) and 'treatment' (text).

    Returns:
        None
    """
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS treatments (
            id INTEGER PRIMARY KEY,
            treatment TEXT
        )
    ''')

    treatments = [
        "virtual reality",
        "exposure therapy",
        "cognitive behavior therapy",
        "psychotherapy",
        "medication",
        "lifestyle changes"
    ]

    for treatment in treatments:
        cursor.execute('INSERT INTO treatments (treatment) VALUES (?)', (treatment,))

def main():

    create_symptoms_table()
    create_treatments_table()

    conn.commit()  # Commit the changes to the database
    conn.close()  # Close the database connection

if __name__ == "__main__":
    main()

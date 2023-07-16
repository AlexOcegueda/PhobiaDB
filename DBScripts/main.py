import sqlite3

# Connect to the 'phobias.db' database
conn = sqlite3.connect('phobias.db')
cursor = conn.cursor()

def view_all_tables():
    # Execute a query to fetch all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")

    # Fetch all rows and print the table names
    tables = cursor.fetchall()
    for table in tables:
        print(table[0])

def view_all(table):
    """
    Fetches and displays all items from the given table.
    """
    cursor.execute(f'SELECT * FROM {table}')
    rows = cursor.fetchall()

    for row in rows:
        print(row)

def delete_table(table):
    """
    Deletes the 'phobias' table from the database.
    """
    cursor.execute(f'''DROP TABLE IF EXISTS {table}''')

def get_symptoms_and_treatments(phobia_name):

    cursor.execute('''
        SELECT symptoms.symptom, treatments.treatment
        FROM phobia_symptom_treatment
        JOIN symptoms ON phobia_symptom_treatment.symptom_id = symptoms.id
        JOIN treatments ON phobia_symptom_treatment.treatment_id = treatments.id
        JOIN phobias ON phobia_symptom_treatment.phobia_id = phobias.id
        WHERE phobias.name = ?
    ''', (phobia_name,))
    rows = cursor.fetchall()

    for row in rows:
        print(row)

def get_symptom_phobia():
    symptom_id = 1  # Replace with the desired symptom ID
    cursor.execute('''
        SELECT phobias.name
        FROM phobia_symptom_treatment
        JOIN phobias ON phobia_symptom_treatment.phobia_id = phobias.id
        WHERE symptom_id = ?
    ''', (symptom_id,))
    rows = cursor.fetchall()

    for row in rows:
        print(row)

def update():
    cursor.execute("UPDATE symptoms SET symptom = 'upset stomach or indigestion' WHERE id = 14")

def main():

    #view_all('phobia_symptom_treatment')
    #delete_table('phobia_symptom_treatment')
    #view_all_tables()
    #view_all('symptoms')

    get_symptoms_and_treatments('Acrophobia (Fear of Heights)')
    #get_symptom_phobia()

if __name__ == "__main__":
    main()

# Commit the changes and close the connection
conn.commit()
conn.close()

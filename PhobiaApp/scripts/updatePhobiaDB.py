# This was suppose to hold cmds to update items in DB
import sqlite3

conn = sqlite3.connect('phobias.db')
cursor = conn.cursor()

def update_androphobia_brief_description(phobia, description):
    new_brief_description = description
    phobia = phobia
    cursor.execute("UPDATE phobias SET brief_description = ? WHERE name = ?", (new_brief_description, phobia))
    conn.commit()

def main():
    n = input("Enter phobia to change: ")
    m = input("Enter new brief description: ")
    update_brief_description(n, m)
    conn.close()

if __name__ == "__main__":
    main()

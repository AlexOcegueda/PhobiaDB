import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Connect to the SQLite database
conn = sqlite3.connect('./phobias.db')

# Query the database to retrieve treatment data
query = '''
    SELECT t.treatment, COUNT(DISTINCT pst.phobia_id) as count
    FROM phobia_symptom_treatment AS pst
    INNER JOIN treatments AS t ON t.id = pst.treatment_id
    GROUP BY t.treatment
    ORDER BY count DESC
    LIMIT 10
'''
df = pd.read_sql_query(query, conn)

# Check if the dataframe is empty
if df.empty:
    print("No data available for plotting.")
else:
    # Set the color palette for the barplot
    sns.set_palette('pastel')

    # Create the bar graph using Seaborn
    sns.barplot(x='count', y='treatment', data=df)
    plt.xlabel('Count')
    plt.ylabel('Treatment')
    plt.title('Most Common Treatments for Phobias')

    # Adjust the layout to prevent labels from being cut off
    plt.tight_layout()

    # Show the graph
    plt.show()

# Close the database connection
conn.close()

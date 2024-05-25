# Suppose to create clear visuals of data
import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

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

if df.empty:
    print("No data available for plotting.")
else:
    sns.set_palette('pastel')

    # Create the bar graph
    sns.barplot(x='count', y='treatment', data=df)
    plt.xlabel('Count')
    plt.ylabel('Treatment')
    plt.title('Most Common Treatments for Phobias')
    plt.tight_layout()

    plt.show()

conn.close()

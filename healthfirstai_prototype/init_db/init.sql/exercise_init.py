import pandas as pd
import psycopg2

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    dbname="postgres", user="root", password="root", host="localhost", port="5432"
)


# Define function to insert data into a table
def insert_data(table, columns, values):
    query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(values))})"
    cursor.execute(query, values)


# Open a cursor to perform database operations
cursor = conn.cursor()

csv_data = "megaGymDataset.csv"
df = pd.read_csv(csv_data)

df['Equipment'].fillna('None', inplace=True)

# Add data to exercise_type table
exercise_types = df['Type'].unique()
for exercise_type in exercise_types:
    insert_data("exercise_type", ["exercise_type"], [exercise_type])

# Add data to body_parts table
body_parts = df['BodyPart'].unique()
for body_part in body_parts:
    insert_data("body_parts", ["bodypart_name"], [body_part])

# Add data to equipment table
equipment = df['Equipment'].unique()
for equip in equipment:
    insert_data("equipment", ["equipment_name"], [equip])

# Add data to difficulty table
difficulty = df['Level'].unique()
for level in difficulty:
    insert_data("difficulty", ["difficulty_name"], [level])

# Commit changes to the database
conn.commit()

# Add data to exercise table with corresponding IDs from other tables
for index, row in df.iterrows():
    exercise_type_id_query = f"SELECT exercise_type_id FROM exercise_type WHERE exercise_type = %s"
    cursor.execute(exercise_type_id_query, [row['Type']])
    exercise_type_id = cursor.fetchone()[0]

    body_part_id_query = f"SELECT bodypart_id FROM body_parts WHERE bodypart_name = %s"
    cursor.execute(body_part_id_query, [row['BodyPart']])
    body_part_id = cursor.fetchone()[0]

    equipment_id_query = f"SELECT equipment_id FROM equipment WHERE equipment_name = %s"
    cursor.execute(equipment_id_query, [row['Equipment']])
    equipment_id = cursor.fetchone()[0]

    difficulty_id_query = f"SELECT difficulty_id FROM difficulty WHERE difficulty_name = %s"
    cursor.execute(difficulty_id_query, [row['Level']])
    difficulty_id = cursor.fetchone()[0]

    insert_data("exercise", ["name", "description", "bodyPart_ID", "exercise_type_ID", "equipment_ID", "difficulty_ID"],
                [row['Title'], row['Desc'], body_part_id, exercise_type_id, equipment_id, difficulty_id])

# Commit changes to the database
conn.commit()

# Close the cursor and the connection
cursor.close()
conn.close()

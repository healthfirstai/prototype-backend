# NOTE: This is where the main application logic is implemented for the exercise agent
import json
import mysql.connector

def generate_schedule_json(user_id):

    # Connect to the MySQL database
    db_connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='healthfirstai',
        port='3307'
    )

    # Create a cursor to execute SQL queries
    cursor = db_connection.cursor()

    try:
        # Query to fetch the user's schedule along with workout details
        query = f"""
                SELECT uws.Schedule_ID, uws.Schedule_Day, uws.Schedule_Time, 
                       w.Workout_ID, w.Workout_Name, w.Workout_Description
                FROM user_workout_schedule uws
                INNER JOIN workout w ON uws.Workout_ID = w.Workout_ID
                WHERE uws.User_ID = {user_id}
            """
        cursor.execute(query)
        schedule_data = cursor.fetchall()

        # Initialize the schedule dictionary
        schedule_json = {}

        for schedule in schedule_data:
            schedule_id, schedule_day, schedule_time, workout_id, workout_name, workout_desc = schedule
            exercise_dict = {}

            # Query to fetch exercises for the specific workout along with their body parts, reps, and sets
            query = f"""
                SELECT e.Exercise_ID, e.Name, e.Description, et.Exercise_type, 
                       e.Equipment, e.Difficulty, bp.BodyPart_Name, we.Reps, we.Sets
                FROM workout_exercise we
                INNER JOIN exercise e ON we.Exercise_ID = e.Exercise_ID
                INNER JOIN exercise_type et ON e.Exercise_type_ID = et.Exercise_type_ID
                LEFT JOIN exercise_body_part ebp ON e.Exercise_ID = ebp.Exercise_ID
                LEFT JOIN body_parts bp ON ebp.BodyPart_ID = bp.BodyPart_ID
                WHERE we.Workout_ID = {workout_id}
            """
            cursor.execute(query)
            exercise_data = cursor.fetchall()

            for exercise in exercise_data:
                exercise_id, exercise_name, exercise_desc, exercise_type, exercise_equipment, exercise_difficulty, body_part_name, reps, sets = exercise

                if exercise_id in exercise_dict:
                    exercise_dict[exercise_id]['Body_Part'].append(body_part_name)
                else:
                    exercise_info = {
                        'Exercise_ID': exercise_id,
                        'Name': exercise_name,
                        'Description': exercise_desc,
                        'Exercise_Type': exercise_type,
                        'Equipment': exercise_equipment,
                        'Difficulty': exercise_difficulty,
                        'Body_Part': [body_part_name],
                        'Reps': reps,
                        'Sets': sets
                    }
                    exercise_dict[exercise_id] = exercise_info

            schedule_info = {
                'Schedule_Day': schedule_day,
                'Schedule_Time': str(schedule_time),
                'Workout_ID': workout_id,
                'Workout_Name': workout_name,
                'Workout_Description': workout_desc,
                'Exercises': list(exercise_dict.values())
            }

            schedule_json[schedule_id] = schedule_info

        # Write the JSON data to a file
        with open('user_schedule.json', 'w') as json_file:
            json.dump(schedule_json, json_file, indent=4)

        print("Schedule JSON file generated successfully.")

    except Exception as e:
        print("Error:", e)

    finally:
        # Close the database connection
        cursor.close()
        db_connection.close()

if __name__ == '__main__':
    generate_schedule_json(1)


import time
import sqlite3
from firebase_handler import initialize_firebase_app, create_new_code, flag_code_expired

def run_code_generation():
    initialize_firebase_app('./credentials.json', 'https://fortressofzeus-default-rtdb.firebaseio.com/')

    while True:
        users = get_users_from_database()
        
        for user in users:
            user_id = user['user_id']
            create_new_code(user_id, "current_code", generate_random_code())
            time.sleep(1)  # Add a short delay between code generation for each user

        cleanup_expired_codes()
        time.sleep(14)  # Sleep for 14 seconds before the next iteration

def get_users_from_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Assuming a 'users' table with columns 'user_id', 'username', 'email', etc.
    cursor.execute("SELECT user_id, username, email FROM users")
    users = [{'user_id': row[0], 'username': row[1], 'email': row[2]} for row in cursor.fetchall()]

    conn.close()
    return users

def cleanup_expired_codes():
    # Implement code cleanup logic here
    # For simplicity, this example flags all codes as expired after 15 seconds
    flag_code_expired_for_all_users()

def flag_code_expired_for_all_users():
    users = get_users_from_database()

    for user in users:
        user_id = user['user_id']
        old_code = get_old_code_from_database(user_id)
        
        if old_code:
            flag_code_expired(user_id, old_code)

def generate_random_code():
    # Implement your code generation logic here
    # This is a simple example, you might want to use a more secure method
    import random
    return random.randint(1, 999999)

def get_old_code_from_database(user_id):
    # Implement logic to retrieve the old code from your SQLite database
    # You might want to fetch the old code from the 'code' column in your 'users' table
    # Adjust this according to your actual database schema
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT code FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    
    return result[0] if result else None

if __name__ == "__main__":
    run_code_generation()

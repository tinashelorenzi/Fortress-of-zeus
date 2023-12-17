import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime, timedelta

_initialized = False
def initialize_firebase_app(cred_path, db_url):
    """
    Initializes a Firebase app using the provided credentials and database URL.

    Args:
        cred_path (str): The path to the credentials file.
        db_url (str): The URL of the Firebase Realtime Database.

    Returns:
        None
    """
    global _initialized

    # Check if already initialized
    if not _initialized:
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred, {'databaseURL': db_url})
        _initialized = True
def is_code_valid(user_id, code_type, provided_code):
    """
    Checks if a given code is valid for a specific user.

    Parameters:
        user_id (str): The ID of the user.
        code (str): The code to be checked.

    Returns:
        bool: True if the code is valid and not expired, False otherwise.
    """
    code_type = "current_code"
    initialize_firebase_app('./credentials.json', 'https://fortressofzeus-default-rtdb.firebaseio.com/')
    user_codes_ref = db.reference(f'authentication_codes/{user_id}/{code_type}')
    code_info = user_codes_ref.get()

    if code_info:
        expiration_timestamp = code_info.get('expiration_timestamp', 0)
        stored_code_value = code_info.get('code_value', None)

        # Check expiration timestamp and verify the provided code
        return (
            expiration_timestamp > int(datetime.utcnow().timestamp())
            and str(stored_code_value) == str(provided_code)
        )
    else:
        return False

def flag_code_expired(user_id,code_type):
    """
    Sets the expiration timestamp of a given authentication code to 0.

    Args:
        user_id (str): The ID of the user for whom the authentication code belongs.
        code (str): The authentication code to be expired.

    Returns:
        None
    """
    user_codes_ref = db.reference(f'authentication_codes/{user_id}/{code_type}')
    user_codes_ref.update({'expiration_timestamp': 0})

def create_new_code(user_id, code_type, code_value, expiration_seconds=15):
    """
    Creates a new authentication code for a user.

    Args:
        user_id (str): The ID of the user for whom the authentication code is being created.
        code_value (str): The value of the authentication code.
        expiration_seconds (int, optional): The number of seconds for which the authentication code will be valid. Defaults to 15.

    Returns:
        None
    """
    expiration_timestamp = int((datetime.utcnow() + timedelta(seconds=expiration_seconds)).timestamp())
    user_codes_ref = db.reference(f'authentication_codes/{user_id}/{code_type}')
    user_codes_ref.set({'code_value': code_value, 'expiration_timestamp': expiration_timestamp})
    return code_value
def code_check(user_id, provided_code):
    """
    Checks if a provided code is valid for a specific user.

    Parameters:
        user_id (str): The ID of the user.
        provided_code (str): The code provided by the user.

    Returns:
        bool: True if the provided code is valid for the user, False otherwise.
    """
    # Assume 'current_code' as the code type, modify as needed
    code_type = 'current_code'

    return is_code_valid(user_id, code_type, provided_code)
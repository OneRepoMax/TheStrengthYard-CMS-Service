import re
import string

def is_strong_password(password):
    # Check length
    if len(password) < 8:
        return False

    # Check for at least 1 uppercase letter
    if not re.search(r'[A-Z]', password):
        return False

    # Check for at least 1 lowercase letter
    if not re.search(r'[a-z]', password):
        return False

    # Check for at least 1 digit
    if not re.search(r'\d', password):
        return False

    # Check for special characters
    if not re.search(r'[$%#*&\-.@]', password):
        return False

    return True


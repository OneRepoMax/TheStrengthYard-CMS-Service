import re
import string
import random

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
    if not re.search(r'[$%#*&\-.@!;]', password):
        return False

    return True

def generate_strong_password(length=12):
    # Define character sets
    uppercase_letters = string.ascii_uppercase
    lowercase_letters = string.ascii_lowercase
    digits = string.digits
    special_characters = r'$%#*&-.@'

    # Combine character sets
    all_characters = uppercase_letters + lowercase_letters + digits + special_characters

    # Ensure the password length is at least 8
    length = max(length, 8)

    # Generate the password
    password = []
    password.append(random.choice(uppercase_letters))
    password.append(random.choice(lowercase_letters))
    password.append(random.choice(digits))
    password.append(random.choice(special_characters))

    # Fill the rest of the password with random characters
    for _ in range(length - 4):
        password.append(random.choice(all_characters))

    # Shuffle the characters to ensure randomness
    random.shuffle(password)

    return ''.join(password)
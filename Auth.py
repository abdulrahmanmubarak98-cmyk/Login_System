import json

# Imports the JSON library to read/write user data to a file in JSON format
import os

# Imports the OS library to check if files exist
import getpass

# Imports getpass to securely prompt for passwords (hides input from screen)
import bcrypt

# Imports bcrypt library for hashing and verifying passwords securely

USERS_FILE = "users.json"
# Defines the filename where user credentials will be stored as a constant


# Load Users Function
# Defines a function to load users from the JSON file
def load_users():
    # Checks if the file exists; if not, returns an empty dictionary
    if not os.path.exists(USERS_FILE):
        return {}
    # Opens the file in read mode ("r")
    # Attempts to parse and return the JSON data
    with open(USERS_FILE, "r") as f:
        try:
            return json.load(f)
        # If the JSON is corrupted/invalid, returns an empty dictionary instead of crashing
        except json.JSONDecodeError:
            return {}


# Defines a function to save the users dictionary to the JSON file
# Opens file in write mode ("w")
# Writes the users dictionary as formatted JSON (indent=4 for readability)
def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)


# Main Menu Loop
while True:
    # Creates an infinite loop that displays the menu options until user exits
    # Prints three menu choices
    print("1. Sign Up")
    print("2. Log In")
    print("3. Exit")

    choice = input("Select an option: ")

    # Loads the current users from the JSON file
    users = load_users()
    # Sign Up Section
    # If user chose sign up, prompts for username (converted to lowercase for consistency)
    # Securely prompts for password (hidden from view)
    if choice == "1":
        username = input("Enter username: ").lower()
        password = getpass.getpass("Enter password: ")
        # Checks if username already exists in the users dictionary
        # If it does, prints error message
        if username in users:
            print("Account already exists")

        else:
            # If username is new, hashes the password using bcrypt with a salt for security
            # Converts the hashed bytes to a UTF-8 string for storage

            hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            hashed_str = hashed.decode("utf-8")
            # Stores the hashed password in the users dictionary under the username
            # Saves the updated users dictionary to the JSON file
            # Confirms account creation
            users[username] = {"password": hashed_str}
            save_users(users)
            print("Account created successfully!")

    # Log In Section
    elif choice == "2":
        # If user chose login, prompts for username and password
        username = input("Enter username: ").lower()
        password = getpass.getpass("Enter password: ")

        # Checks if the username exists
        # If not, prints error message
        if username not in users:
            print("User not found")
        # Retrieves the stored hashed password from the users dictionary
        # Converts it back to bytes for comparison

        else:
            stored_hash = users[username]["password"]
            stored_hash_bytes = stored_hash.encode("utf-8")

            # Compares the entered password (hashed) with the stored hash
            # If they match, prints success message
            if bcrypt.checkpw(password.encode(), stored_hash_bytes):
                print("Login successful!")

            else:
                print("Wrong password")
    # If user chose exit, prints goodbye message
    # Breaks out of the infinite loop, ending the program
    elif choice == "3":
        print("Goodbye!")
        break

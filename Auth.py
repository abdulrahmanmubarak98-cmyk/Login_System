import json
import os 
import getpass
import bcrypt

USERS_FILE = "users.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open (USERS_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}
    
def save_users(users):
    with open (USERS_FILE, "w") as f:
      json.dump(users, f, indent=4)

while True:
    print("1. Sign Up")
    print("2. Log In")
    print("3. Exit")

    choice = input("Select an option: ")

    users = load_users()

    if choice == "1":
        username = input("Enter username: ").lower()
        password = getpass.getpass("Enter password: ")

        if username in users:
            print("Account already exists")

        else:

               hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
               hashed_str = hashed.decode("utf-8")

               users[username] = {"password": hashed_str}; save_users(users)
               print("Account created successfully!")

    elif choice == "2":
        username = input("Enter username: ").lower()
        password = getpass.getpass("Enter password: ")

        if username not in users:
            print("User not found")
        else:
            stored_hash = users[username]["password"]
            stored_hash_bytes = stored_hash.encode("utf-8")

            if bcrypt.checkpw(password.encode(), stored_hash_bytes):
                print("Login successful!")

            else:
                print("Wrong password")
    elif choice == "3":
        print("Goodbye!")
        break




   
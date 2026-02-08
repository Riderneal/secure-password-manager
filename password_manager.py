import json
import os
import hashlib

DATA_FILE = "passwords.json"
MASTER_FILE = "master.hash"

def hash_text(text):
    return hashlib.sha256(text.encode()).hexdigest()

def set_master_password():
    password = input("Set master password: ")
    with open(MASTER_FILE, "w") as f:
        f.write(hash_text(password))
    print("Master password set successfully.")

def authenticate():
    if not os.path.exists(MASTER_FILE):
        print("No master password found. Please set one.")
        set_master_password()
        return True

    password = input("Enter master password: ")
    with open(MASTER_FILE, "r") as f:
        stored_hash = f.read()

    if hash_text(password) == stored_hash:
        return True
    else:
        print("Authentication failed.")
        return False

def load_passwords():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_passwords(passwords):
    with open(DATA_FILE, "w") as f:
        json.dump(passwords, f, indent=4)

def add_password():
    site = input("Website: ")
    username = input("Username: ")
    password = hash_text(input("Password: "))
    passwords = load_passwords()
    passwords.append({
        "site": site,
        "username": username,
        "password": password
    })

    save_passwords(passwords)
    print("Password saved successfully.")

def view_passwords():
    passwords = load_passwords()
    if not passwords:
        print("No passwords stored.")
        return

    for entry in passwords:
        print(f"Site: {entry['site']}, Username: {entry['username']}, Password: {entry['password']}")

def main():
    if not authenticate():
        return

    while True:
        print("\n1. Add Password")
        print("2. View Passwords")
        print("3. Exit")

        choice = input("Choose option: ")

        if choice == "1":
            add_password()
        elif choice == "2":
            view_passwords()
        elif choice == "3":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()

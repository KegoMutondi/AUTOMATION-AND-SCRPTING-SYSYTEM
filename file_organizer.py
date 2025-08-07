import os
import shutil
import json
from datetime import datetime

# Load config
with open("config.json") as config_file:
    config = json.load(config_file)

TARGET_FOLDER = config["target_folder"]
CATEGORIES = config["categories"]
LOG_FILE = "log.txt"

# Logging function
def log_action(message):
    with open(LOG_FILE, "a") as log:
        time_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log.write(f"[{time_stamp}] {message}\n")

# Move file safely with renaming if duplicate
def move_file_safely(src, dest_folder, filename):
    original_name = filename
    base, ext = os.path.splitext(filename)
    count = 1

    while os.path.exists(os.path.join(dest_folder, filename)):
        filename = f"{base} ({count}){ext}"
        count += 1

    dest_path = os.path.join(dest_folder, filename)
    shutil.move(src, dest_path)
    log_action(f"Moved: {original_name} → {dest_folder} as {filename}")
    print(f"Moved: {original_name} → {dest_folder} as {filename}")

# Organize files
def organize_files():
    for filename in os.listdir(TARGET_FOLDER):
        file_path = os.path.join(TARGET_FOLDER, filename)

        if os.path.isfile(file_path):
            _, ext = os.path.splitext(filename)
            ext = ext.lower()

            for category, extensions in CATEGORIES.items():
                if ext in extensions:
                    dest_folder = os.path.join(TARGET_FOLDER, category)

                    if not os.path.exists(dest_folder):
                        os.makedirs(dest_folder)

                    move_file_safely(file_path, dest_folder, filename)
                    break

# Menu
def main_menu():
    while True:
        print("\n=== FILE ORGANIZER ===")
        print("1. Organize Files")
        print("2. View Log")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            organize_files()
        elif choice == "2":
            if os.path.exists(LOG_FILE):
                with open(LOG_FILE, "r") as log:
                    print("\n--- LOG ---")
                    print(log.read())
            else:
                print("Log file does not exist.")
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")

# Start
if __name__ == "__main__":
    main_menu()

import csv
import os
import platform

def determine_windows():
    """Determine if the operating system is Windows."""
    return platform.system() == "Windows"

def get_csv_path():
    """Returns the path to the CSV file based on the operating system."""
    if determine_windows():
        base_path = os.path.join(os.getenv('APPDATA'), "pt1_Lightweight_Notes")
    else:
        base_path = os.path.join(os.path.expanduser("~"), ".config", "pt1_Lightweight_Notes")

    # Ensure the directory exists
    os.makedirs(base_path, exist_ok=True)
    
    return os.path.join(base_path, "login.csv")

# Define the CSV file path
csv_file_path = get_csv_path()

def check_csv_exists():
    """Check if the CSV file exists."""
    return os.path.exists(csv_file_path)

def create_csv():
    """Creates the CSV file with a header if it doesn't exist."""
    if check_csv_exists():
        print(f"CSV already exists at {csv_file_path}")
        return
    
    # Create and populate the CSV file
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["uid", "first_name", "password"], delimiter=";")
        writer.writeheader()
        # Add any default user credentials if needed; example row:
        writer.writerow({"uid": "1", "first_name": "admin", "password": "localadminfern"})
    
    print(f"CSV created at {csv_file_path}")


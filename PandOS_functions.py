import os
import json
import logging
import matplotlib

#--------------------------------------------------------------------------------------

# Path to warnings file
WARNINGS_FILE = "warnings.json"

#--------------------------------------------------------------------------------------

# Function to load warnings data

def load_warnings():
    if not os.path.exists(WARNINGS_FILE):
        with open(WARNINGS_FILE, "w") as f:
            json.dump({}, f)
        return {}

    try:
        with open(WARNINGS_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("Error: The warnings file is corrupted. Reinitializing...")
        with open(WARNINGS_FILE, "w") as f:
            json.dump({}, f)
        return {}

#--------------------------------------------------------------------------------------

# Function to save warnings data

def save_warnings(warnings_data):
    with open(WARNINGS_FILE, "w") as f:
        json.dump(warnings_data, f, indent=4)


#--------------------------------------------------------------------------------------

# Function to add a warning

def add_warning(user_id, reason):
    warnings_data = load_warnings()

    if str(user_id) in warnings_data:
        warnings_data[str(user_id)]["count"] += 1
        warnings_data[str(user_id)]["reasons"].append(reason)
    else:
        warnings_data[str(user_id)] = {"count": 1, "reasons": [reason]}

    save_warnings(warnings_data)
    return warnings_data[str(user_id)]["count"]


#--------------------------------------------------------------------------------------

# Function to get the number of warnings

def get_warnings(user_id):
    warnings_data = load_warnings()
    return warnings_data.get(str(user_id), {"count": 0, "reasons": []})["count"]

#--------------------------------------------------------------------------------------

# Function to reset warnings

def reset_warnings(user_id):
    warnings_data = load_warnings()
    if str(user_id) in warnings_data:
        del warnings_data[str(user_id)]
        save_warnings(warnings_data)

#--------------------------------------------------------------------------------------

# Function to get detailed warnings
def get_warnings(user_id):
    """Pobiera ostrzeżenia użytkownika z pliku JSON."""
    with open("warnings.json", "r", encoding="utf-8") as f:
        warnings_data = json.load(f)

    return warnings_data.get(
        str(user_id), {"count": 0, "reasons": []}
    ) 

#--------------------------------------------------------------------------------------

# Function to generate a progress bar
def get_progress_bar(percent):
    total_blocks = 10
    filled_blocks = int(percent / 10)
    empty_blocks = total_blocks - filled_blocks
    return "█" * filled_blocks + "░" * empty_blocks
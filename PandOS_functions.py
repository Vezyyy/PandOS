# PandOS Functions Module
# This module contains various utility functions for the PandOS system,
# including warning management, progress bar generation, word handling,
# link removal, random sentence generation, gambling user management,
# and team points management.

#Libraries Imports
import os, json, logging, matplotlib, re, random, importlib
from collections import defaultdict
from PandOS_greetings_data  import greetings, conversations

#--------------------------------------------------------------------------------------

# Path to warnings file
WARNINGS_FILE = "warnings.json"

# Path to Pandocoin rate file
rate_file_path = "pandocoin_rate.json"
gambling_file_path = "gambling.json"


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

#--------------------------------------------------------------------------------------

# Function to load words from JSON file
def load_words_from_json():
    try:
        with open("words.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            return data["words"]
    except FileNotFoundError:
        print("Plik 'words.json' nie został znaleziony.")
        return []

#--------------------------------------------------------------------------------------

# Function to save words to JSON file

def save_words_to_json(words):
    data = {"words": words}
    with open("words.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print("Słowa zostały zapisane do pliku 'words.json'.")

#--------------------------------------------------------------------------------------

# function to remove links from text

def remove_links(text):
    return re.sub(r"http[s]?://\S+|www\.\S+", "", text)

#--------------------------------------------------------------------------------------

# Function to generate a random sentence
def generate_random_sentence():
    words = load_words_from_json()
    if not words:
        return "Sorry, no words available to generate a sentence."

    sentence_length = random.randint(3, 10)  
    sentence = random.sample(words, sentence_length)  
    return " ".join(sentence) 

#--------------------------------------------------------------------------------------

# NEW USER GAMBLING ACCOUNT IN PANDOS SYSTEM

# This function adds a new user to the gambling system with default values when they join.
# If the user already exists but has missing data fields, it adds those fields with default values.
# Finally, it saves the updated data back to the JSON file.

def add_user_on_join(user_id):
    user_id = str(user_id) 

    if os.path.exists(gambling_file_path):
        with open(gambling_file_path, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}  
    else:
        data = {}

    if user_id not in data:
        data[user_id] = {
            "balance": 0,
            "last_work": 0,
            "last_robbery": 0,
            "failed_rob_attempts": 0,
            "protection_end": 0,
            "inventory": {"PandoCoin": 0}, 
            "last_rob_time": 0,
            "pando_balance": 0,
        }
        print(
            f"✅ Użytkownik {user_id} został dodany do pliku z domyślnymi wartościami."
        )
    else:
        user_data = data[user_id]
        updated = False

        required_fields = {
            "balance": 0,
            "last_work": 0,
            "last_robbery": 0,
            "failed_rob_attempts": 0,
            "protection_end": 0,
            "inventory": {}, 
            "last_rob_time": 0,
            "pando_balance": 0,
        }

        for field, default_value in required_fields.items():
            if field not in user_data:
                user_data[field] = default_value
                updated = True

        if "inventory" not in user_data or not isinstance(user_data["inventory"], dict):
            user_data["inventory"] = {"PandoCoin": 0}
            updated = True
        elif "PandoCoin" not in user_data["inventory"]:
            user_data["inventory"]["PandoCoin"] = 0
            updated = True

        if updated:
            data[user_id] = user_data
            print(f"🔄 Użytkownik {user_id} miał brakujące dane, które zostały dodane.")
        else:
            print(f"✅ Użytkownik {user_id} ma już wszystkie wymagane dane.")

    with open(gambling_file_path, "w") as f:
        json.dump(data, f, indent=4)

#--------------------------------------------------------------------------------------

# GAMBLING LOAD
# This section handles loading and saving user data for the gambling system.
# The data is stored in a JSON file named "gambling.json".
# Functions are provided to load and save the data.
# Usage: load_data() and save_data(data)


def load_data():
    if not os.path.exists(gambling_file_path):
        with open(gambling_file_path, "w") as file:
            json.dump({}, file)

    if os.path.getsize(gambling_file_path) == 0:
        return {}

    with open(gambling_file_path, "r") as file:
        return json.load(file)

def save_data(data):
    with open(gambling_file_path, "w") as file:
        json.dump(data, file, indent=4)

#--------------------------------------------------------------------------------------

# GAMBLING LOAD USER DATA
# This section provides functions to load and save individual user data for the gambling system.
# The data is stored in a JSON file named "gambling.json".

def load_user_data():
    if not os.path.exists(gambling_file_path):
        return {}  
    with open(gambling_file_path, "r") as file:
        return json.load(file)


def save_user_data(data):
    with open(gambling_file_path, "w") as file:
        json.dump(data, file, indent=4)


def load_user_data():
    if not os.path.exists(gambling_file_path):
        return {}
    with open(gambling_file_path, "r") as file:
        return json.load(file)


def save_user_data(data):
    with open(gambling_file_path, "w") as file:
        json.dump(data, file, indent=4)


#--------------------------------------------------------------------------------------      

# PANDOS COIN LOAD USER DATA
# This section provides functions to load and save Pandocoin data for the gambling system.

def load_pandocoin_data():
    if not os.path.exists(rate_file_path):
        return {"rate": 1, "history": [1]} 
    with open(rate_file_path, "r") as file:
        return json.load(file)


def save_pandocoin_data(data):
    with open(rate_file_path, "w") as file:
        json.dump(data, file, indent=4)


def simulate_rate_change(current_rate):
    change_percentage = random.uniform(
        -0.02, 0.02
    )  
    new_rate = current_rate * (1 + change_percentage)
    return round(new_rate, 2)

#--------------------------------------------------------------------------------------  

# function to load team points from a file

def load_team_points():
    if os.path.exists("BSOG_Team.py"):
        team_data = importlib.import_module("BSOG_Team")
        logging.info("Successfully loaded team points from BSOG_Team.py")
        return team_data.team_points
    else:
        logging.warning("BSOG_Team.py not found. Initializing with default points.")
        return {
            "❤️ Team Red": 0,
            "💙 Team Blue": 0,
            "💚 Team Green": 0,
            "💛 Team Yellow": 0,
            "💜 Team Purple": 0,
            "🧡 Team Orange": 0,
            "💖 Team Pink": 0,
            "💠 Team Cyan": 0,
            "⚫ Team Black": 0,
            "⚪ Team White": 0,
        }


# Function to save the team points to a file

def save_team_points(team_points):
    try:
        with open("BSOG_Team.py", "w") as file:
            file.write("team_points = {\n")
            for team, points in team_points.items():
                file.write(f'    "{team}": {points},\n')
            file.write("}\n")
        logging.info("Successfully saved team points to BSOG_Team.py")
    except Exception as e:
        logging.error(f"Error saving team points to file: {e}")

#--------------------------------------------------------------------------------------  

# Function to get a random greeting response based on language

def get_greeting_response(lang):
    greetings_responses = {
        "en": ["Hello!", "Hi there!", "Hey, how's it going?", "Greetings!"],
        "pl": ["Cześć!", "Hejka!", "Witaj!", "Siema!", "Jak się masz?"],
        "de": ["Hallo!", "Servus!", "Guten Tag!", "Wie geht's?"],
        "es": ["¡Hola!", "¡Qué tal!", "¡Buenos días!", "¡Buenas tardes!"],
    }
    return random.choice(greetings_responses.get(lang, ["Hello!"]))

#--------------------------------------------------------------------------------------  

# function to detect greetings in different languages

def detect_greeting(message):
    logging.debug(f"Detecting greeting in message: {message.content}")
    user_message = (
        message.content.lower().strip()
    ) 

    for lang, words in greetings.items():
        for word in words:
            if re.search(
                rf"\b{re.escape(word)}\b", user_message
            ): 
                logging.debug(f"Greeting detected: {lang} with word: {word}")
                return lang
    logging.debug("No greeting detected.")
    return None

#--------------------------------------------------------------------------------------  

# Function to detect conversation keywords and respond

def get_conversation_response(message, lang):
    logging.debug(f"Processing message: {message.content} in language: {lang}")
    user_message = message.content.lower().strip()

    for keyword, responses in conversations.items():
        if re.search(rf"\b{re.escape(keyword)}\b", user_message):
            response_list = responses.get(lang, [])
            if response_list:
                return random.choice(response_list)
    return None

#--------------------------------------------------------------------------------------  

# Path to the JSON data file

DATA_FILE = "user_data.json"

# Initial load of user data

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as file:
        user_data = json.load(file)


# Fuction to save user data to JSON file

def save_user_data():
    with open(DATA_FILE, "w") as file:
        json.dump(user_data, file, indent=4)

#--------------------------------------------------------------------------------------  


# Keeping track of user XP and levels

user_data = defaultdict(
    lambda: {"xp": 0, "level": 1, "last_message_time": 0, "voice_start_time": 0}
)


# Function to calculate XP needed for next level
def xp_to_next_level(level):
    return 100 + (level - 1) * 50

#--------------------------------------------------------------------------------------  


# Function to get user data or initialize if not present
def get_user_data(user_id):
    if str(user_id) not in user_data:
        user_data[str(user_id)] = {
            "xp": 0,
            "level": 1,
            "last_message_time": 0,
            "voice_start_time": 0,
        }
    return user_data[str(user_id)]

#--------------------------------------------------------------------------------------  


# Function to check and handle level up
def check_level_up(user):
    leveled_up = False
    while user["xp"] >= xp_to_next_level(user["level"]):
        user["xp"] -= xp_to_next_level(user["level"])
        user["level"] += 1
        leveled_up = True
        print(f"Użytkownik awansował na poziom {user['level']}!")
    return leveled_up

#--------------------------------------------------------------------------------------  

# Function to add XP and check for level up
def add_xp(user_id, xp_amount):
    user = get_user_data(user_id)
    user["xp"] += xp_amount 
    leveled_up = check_level_up(user) 
    save_user_data() 
    return leveled_up 

#--------------------------------------------------------------------------------------  

# GOONER OF THE DAY COMMAND
# ----------------------------

COOLDOWN_FILE = "gooneroftheday.json"
CHANNEL_ID = 1295000603679916042 
gooneroftheday = ""


def load_cooldown():
    try:
        with open(COOLDOWN_FILE, "r") as f:
            return json.load(f)
    except:
        return {"last_used": 0, "last_user_id": None}


def save_cooldown(data):
    with open(COOLDOWN_FILE, "w") as f:
        json.dump(data, f)

#--------------------------------------------------------------------------------------  

# Function to format Steam price

def format_price(price, currency="EUR"):
    """Format Steam price (minor units) to currency string."""
    if price is None:
        return "No data"
    return f"{price / 100:.2f} {currency}"

#--------------------------------------------------------------------------------------  
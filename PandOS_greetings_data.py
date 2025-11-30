# greetings_data.py
# Words and phrases for greetings and conversations in multiple languages

greetings = {
    "en": [
        "hello",
        "hi",
        "hey",
        "good morning",
        "good evening",
        "greetings",
        "what's up",
        "howdy",
        "hi there",
        "yo",
        "hey there",
    ],
    "pl": [
        "cześć",
        "hej",
        "dzień dobry",
        "witaj",
        "siema",
        "hejka",
        "elo",
        "siemanko",
        "hejka, co tam?",
        "witam serdecznie",
    ],
    "de": [
        "hallo",
        "hi",
        "guten morgen",
        "guten abend",
        "servus",
        "moin",
        "grüß dich",
        "hiho",
    ],
    "es": [
        "hola",
        "buenos días",
        "buenas tardes",
        "qué tal",
        "buenas noches",
        "cómo va",
        "qué pasa",
    ],
    "fr": [
        "bonjour",
        "salut",
        "bonsoir",
        "salutations",
        "coucou",
        "hé",
    ],
    "it": [
        "ciao",
        "buongiorno",
        "buonasera",
        "salve",
        "ehi",
    ],
}

# Rozszerzony słownik pytań
conversations = {
    "how are you": {
        "en": [
            "I'm doing great, thanks for asking! How about you?",
            "I'm doing well! What about you?",
            "I'm fine, thank you! How's everything on your side?",
            "Feeling fantastic! How can I assist you today?",
            "I'm doing awesome, and you?",
            "All good here, what about you?",
        ],
        "pl": [
            "Dziękuję za zapytanie! Mam się świetnie. A Ty?",
            "Czuję się dobrze, a Ty?",
            "Wszystko w porządku, dziękuję! Jak u Ciebie?",
            "Czuję się świetnie! W czym mogę Ci pomóc?",
            "Dzięki, mam się świetnie! A Ty?",
            "Wszystko ok, a u Ciebie?",
        ],
    },
    "jak się masz": {
        "pl": [
            "Dziękuję, mam się świetnie! A Ty?",
            "Wszystko w porządku. Jak u Ciebie?",
            "Czuję się dobrze, dziękuję za pytanie!",
            "Mam się bardzo dobrze! A Ty?",
            "Wszystko ok, a u Ciebie?",
        ],
    },
    "hello": {
        "en": [
            "Hello! How can I help you today?",
            "Hi there! What's on your mind?",
            "Greetings! What can I do for you?",
            "Hey! How are you doing?",
            "Hello! What's up?",
            "Hi! How's it going?",
        ],
        "pl": [
            "Cześć! Jak mogę Ci pomóc?",
            "Witaj! Co mogę dla Ciebie zrobić?",
            "Hej! W czym mogę pomóc?",
            "Cześć! Co słychać?",
            "Witam! Jak się czujesz?",
        ],
    },
    "how's the weather": {
        "en": [
            "The weather is great! Sunny and warm.",
            "It's a bit cloudy, but still pleasant.",
            "The weather is rainy today.",
            "It's quite chilly outside, you might want to wear a jacket.",
            "It's really hot out there today!",
        ],
        "pl": [
            "Pogoda jest świetna! Słonecznie i ciepło.",
            "Jest trochę pochmurno, ale wciąż przyjemnie.",
            "Dziś pada deszcz.",
            "Jest dość chłodno na zewnątrz, chyba warto ubrać kurtkę.",
            "Dziś jest naprawdę gorąco!",
        ],
    },
    "what is your name": {
        "en": [
            "My name is PandOS. How can I assist you?",
            "I go by the name PandOS. How can I help you today?",
            "I am PandOS, your assistant. What can I do for you?",
        ],
        "pl": [
            "Mam na imię PandOS. Jak mogę Ci pomóc?",
            "Nazywam się PandOS. W czym mogę Ci pomóc?",
            "Jestem PandOS, twój asystent. Co mogę dla Ciebie zrobić?",
        ],
    },
    "goodbye": {
        "en": [
            "Goodbye! Have a great day!",
            "See you later! Take care!",
            "Goodbye, take care of yourself!",
            "Farewell! See you soon!",
        ],
        "pl": [
            "Do zobaczenia! Miłego dnia!",
            "Na razie! Trzymaj się!",
            "Żegnaj, dbaj o siebie!",
            "Do widzenia! Wkrótce się zobaczymy!",
        ],
    },
    "bye": {
        "en": [
            "Goodbye! Have a great day!",
            "See you later! Take care!",
            "Goodbye, take care of yourself!",
            "Farewell! See you soon!",
        ],
        "pl": [
            "Do zobaczenia! Miłego dnia!",
            "Na razie! Trzymaj się!",
            "Żegnaj, dbaj o siebie!",
            "Do widzenia! Wkrótce się zobaczymy!",
        ],
    },
    "how old are you": {
        "en": [
            "I don't have an age like humans, but I'm constantly learning!",
            "I am ageless, just a creation of knowledge and algorithms.",
            "I don't age, I just evolve.",
        ],
        "pl": [
            "Nie mam wieku jak ludzie, ale ciągle się uczę!",
            "Jestem bez wieku, po prostu tworzony z wiedzy i algorytmów.",
            "Nie starzeję się, po prostu ewoluuję.",
        ],
    },
    "what do you do": {
        "en": [
            "I assist people with various tasks and answer their questions.",
            "I'm here to help with anything you need.",
            "I provide information and support for various topics.",
        ],
        "pl": [
            "Pomagam ludziom w różnych zadaniach i odpowiadam na pytania.",
            "Jestem tu, aby pomóc w czymkolwiek potrzebujesz.",
            "Dostarczam informacji i wsparcia w różnych tematach.",
        ],
    },
    "thank you": {
        "en": [
            "You're welcome! Feel free to ask if you need anything else.",
            "No problem! Glad I could help.",
            "You're very welcome! Let me know if there's anything else.",
        ],
        "pl": [
            "Nie ma za co! Śmiało pytaj, jeśli potrzebujesz pomocy.",
            "Żaden problem! Cieszę się, że mogłem pomóc.",
            "Proszę bardzo! Daj znać, jeśli mogę pomóc w czymś jeszcze.",
        ],
    },
    "where are you from": {
        "en": [
            "I'm from the digital world, created by OpenAI!",
            "I exist in the cloud, I don't have a physical location.",
            "I don't have a specific place of origin, but I was created by OpenAI.",
        ],
        "pl": [
            "Jestem z cyfrowego świata, stworzony przez OpenAI!",
            "Istnieję w chmurze, nie mam fizycznej lokalizacji.",
            "Nie mam konkretnego miejsca pochodzenia, ale zostałem stworzony przez OpenAI.",
        ],
    },
}


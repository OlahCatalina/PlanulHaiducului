import json
import os

DATA_FILE = "data.json"

DEFAULT_DATA = {
    "cabana": {
        "nume": "Cazare cabana tip A",
        "locație": "Bologa, Cluj County 407471, România",
        "link_airbnb": "https://www.airbnb.com.ro/rooms/964314240212909855",
        "link_maps_destinatie": "https://www.google.com/maps/search/?api=1&query=Bologa,+Cluj+County+407471",
        "perioada": "28 - 30 Noiembrie",
        "nopți": 2,
        "utilizatori": ["Alexandra", "Cătălina", "Stefan", "Mihai"],
        "preț_total": 1128,
        "preț_pe_noapte": 564,
        "rute": {},
        "highlights": []
    },
    "poll_mâncare": {"locked": False, "opțiuni_existente": {}, "voturi_useri": {}, "custom_items": []},
    "shopping_list": [],
    "activități": [],
    "cheltuieli": []
}

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return DEFAULT_DATA
    return DEFAULT_DATA

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

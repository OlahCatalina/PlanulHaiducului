import json
import os

# Path to the local JSON database
DATA_FILE = "data.json"

# Default fallback data structure aligned with the English schema
DEFAULT_DATA = {
    "cabin": {
        "name": "A-frame Cabin Stay",
        "location": "Bologa, Cluj County 407471, Romania",
        "link_airbnb": "https://www.airbnb.com.ro/rooms/964314240212909855",
        "link_maps_destination": (
            "https://www.google.com/maps/search/?api=1&query=Bologa,+Cluj+County+407471"
        ),
        "period": "November 28 - 30",
        "nights": 2,
        "users": ["Alexandra", "Cătălina", "Stefan", "Mihai"],
        "price_total": 1128,
        "price_per_night": 564,
        "routes": {},
        "highlights": [],
    },
    "food_poll": {
        "locked": False,
        "existing_options": {},
        "user_votes": {},
        "custom_items": [],
    },
    "shopping_list": [],
    "activities": [],
    "expenses": [],
}


def load_data():
  """Loads the application state from data.json.

  Returns DEFAULT_DATA if the file does not exist or cannot be parsed.
  """
  if os.path.exists(DATA_FILE):
    try:
      with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
    except Exception:
      return DEFAULT_DATA
  return DEFAULT_DATA


def save_data(data):
  """Persists the current application state dictionary to data.json."""
  with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

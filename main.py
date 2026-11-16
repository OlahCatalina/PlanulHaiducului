import json
import os
import streamlit as st

# Import modular tabs from the 'tabs' folder package
from tabs import activities, budget, cabin, food, shopping

# Path definitions for the local JSON database and external CSS styling
DATA_FILE = "data.json"
STYLE_FILE = "style.css"


def load_data():
  """Loads data from the local data.json file.

  Returns a dictionary containing the app state or an empty dict if it fails.
  """
  if os.path.exists(DATA_FILE):
    try:
      with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
    except Exception:
      return {}
  return {}


def save_data(data):
  """Saves the updated state dictionary back to data.json with UTF-8 encoding

  and proper indentation.
  """
  with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)


# Load global application data from the root directory
data = load_data()

# Extract the fixed list of users from the cabin settings (with a fallback list)
USERS = data.get("cabin", {}).get(
    "users", ["Alexandra", "Cătălina", "Stefan", "Mihai"]
)

# Streamlit general page configuration
st.set_page_config(
    page_title="A-frame Cabin - Bologa 🏡", page_icon="🏔️", layout="centered"
)

# Load external CSS styling from style.css if available in root
if os.path.exists(STYLE_FILE):
  with open(STYLE_FILE, "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Main title display
st.title("🏔️ A-frame Cabin Weekend — Bologa")
st.markdown("---")

# Setup navigation tabs for the web interface
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏡 Cabin & Info",
    "🍔 Food Poll",
    "🛒 Shopping",
    "🎯 Activities",
    "💸 Budget",
])

# Render Tab 1: Cabin details, pricing breakdown, and logistics
with tab1:
  cabin.render(data, USERS)

# Render Tab 2: Food & Drink poll system and custom additions
with tab2:
  food.render(data, USERS, save_data)

# Render Tab 3: Unified shopping checklist generated from poll results
with tab3:
  shopping.render(data, USERS, save_data)

# Render Tab 4: Interactive group voting for weekend activities
with tab4:
  activities.render(data, USERS, save_data)

# Render Tab 5: Financial tracking, expense logging, and smart split calculations
with tab5:
  budget.render(data, USERS, save_data)

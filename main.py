import json
import os
import streamlit as st

# Importăm modulele din folderul tabs
from tabs import activitati, buget, cabana, cumparaturi, mancare

DATA_FILE = "data.json"
STYLE_FILE = "style.css"


def load_data():
  if os.path.exists(DATA_FILE):
    try:
      with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
    except Exception:
      return {}
  return {}


def save_data(data):
  with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)


# Încărcăm datele din json-ul din root
data = load_data()

# Extragem lista de utilizatori direct din structura de date (fallback la o listă goală dacă lipsește)
USERS = data.get("users", ["Alexandra", "Cătălina", "Stefan", "Mihai"])

st.set_page_config(
    page_title="Cabana tip A - Bologa 🏡", page_icon="🏔️", layout="centered"
)

# Încărcăm fișierul extern style.css
if os.path.exists(STYLE_FILE):
  with open(STYLE_FILE, "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("🏔️ Weekend la Cabană tip A — Bologa")
st.markdown("---")

# Generăm tab-urile aplicației
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏡 Cabana & Info",
    "🍔 Poll Mâncare",
    "🛒 Cumpărături",
    "🎯 Activități",
    "💸 Buget",
])

with tab1:
  cabana.render(data, USERS)

with tab2:
  mancare.render(data, USERS, save_data)

with tab3:
  cumparaturi.render(data, USERS, save_data)

with tab4:
  activitati.render(data, USERS, save_data)

with tab5:
  buget.render(data, USERS, save_data)

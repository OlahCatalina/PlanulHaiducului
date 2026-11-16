
import json
import os
import streamlit as st

DATA_FILE = "data.json"

# Date inițiale default (dacă fișierul nu există)
DEFAULT_DATA = {
    "cabana": {
        "nume": "Cabana Mountain View",
        "locație": "Răchițele, jud. Cluj",
        "link_airbnb": "https://airbnb.com",
        "link_maps": "https://maps.google.com",
        "perioada": "15 - 18 Septembrie 2027",
        "nopți": 3,
        "persoane": 4,
        "preț_total": 1200,
        "preț_pe_noapte": 400,
        "rute": {
            "cluj": (
                "Cluj-Napoca -> Huedin -> Răchițele (~1h 15m, 65 km)"
            ),
            "bucuresti": (
                "București -> Brașov -> Cluj -> Răchițele (sau A1 -> Sebeș ->"
                " Cluj)"
            ),
        },
        "highlights": [
            "Grătar / Grill exterior complet utilat",
            "Ciubăr cu hidromasaj",
            "Wi-Fi Starlink",
            "Living generos",
        ],
    },
    "poll_mâncare": {
        "locked": False,
        "opțiuni_existente": {
            "Carne & Grill": [
                "Ceafă de porc",
                "Mici",
                "Pui pentru grătar",
                "Cârnați afumați",
            ],
            "Garnituri & Salate": [
                "Cartofi pentru copt",
                "Roșii, castraveți, ceapă",
                "Brânză telemea",
                "Sosuri (ketchup, muștar, maioneză)",
            ],
            "Mic dejun & Snack-uri": [
                "Ouă",
                "Pâine / Focaccia",
                "Mezeluri / Pastramă",
                "Chipsuri / Alune",
            ],
        },
        "voturi_useri": {},
        "custom_items": [],
    },
    "shopping_list": [],
    "activități": [
        {
            "nume": "Drumeție la Cascadă Vălul Miresei",
            "voturi": [],
            "confirmat": False,
        },
        {"nume": "Seară de board games & mafia", "voturi": [], "confirmat": False},
        {
            "nume": "Concurs de gătit la ceaun / grill",
            "voturi": [],
            "confirmat": False,
        },
    ],
    "cheltuieli": [
        {"persoană": "Cătălina", "descriere": "Avans cabană", "sumă": 400}
    ],
}


def load_data():
  if os.path.exists(DATA_FILE):
    try:
      with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
    except:
      return DEFAULT_DATA
  return DEFAULT_DATA


def save_data(data):
  with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)


data = load_data()

st.set_page_config(
    page_title="Plan Cabană 🏡", page_icon="🏔️", layout="centered"
)

st.title("🏔️ Planificare Weekend la Cabană")
st.markdown("---")

# Tab-uri pentru organizare curată
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏡 Cabana & Info",
    "🍔 Poll Mâncare",
    "🛒 Lista Cumpărături",
    "🎯 Activități",
    "💸 Buget & Smart Split",
])

# ================= TAB 1: CABANA & INFO =================
with tab1:
  cabana = data.get("cabana", {})
  st.header(f"🏡 {cabana.get('nume', 'Cabana')}")

  col1, col2, col3 = st.columns(3)
  col1.metric("Preț Total", f"{cabana.get('preț_total', 0)} RON")
  col2.metric("Preț / Noapte", f"{cabana.get('preț_pe_noapte', 0)} RON")
  col3.metric(
      "Preț / Persoană",
      f"{cabana.get('preț_total', 0) // max(1, cabana.get('persoane', 1))} RON",
  )

  st.markdown(
      f"📅 **Perioada:** {cabana.get('perioada')} ({cabana.get('nopți')} nopți)"
  )
  st.markdown(f"📍 **Locație:** {cabana.get('locație')}")

  c_link1, c_link2 = st.columns(2)
  with c_link1:
    st.link_button("🔗 Vezi pe Airbnb", cabana.get("link_airbnb", "#"))
  with c_link2:
    st.link_button("🗺️ Deschide Google Maps", cabana.get("link_maps", "#"))

  st.subheader("🚗 Rute de acces")
  st.info(f"**Din Cluj:** {cabana.get('rute', {}).get('cluj')}")
  st.info(f"**Din București:** {cabana.get('rute', {}).get('bucuresti')}")

  st.subheader("✨ Highlights & Facilități")
  for h in cabana.get("highlights", []):
    st.write(f"- {h}")

# ================= TAB 2: POLL MÂNCARE =================
with tab2:
  st.header("🍔 Poll Mâncare & Băuturi")
  user_name = st.text_input(
      "Introdu numele tău ca să poți vota:", key="voter_name"
  )

  m_poll = data.get("poll_mâncare", {})

  if m_poll["locked"]:
    st.warning(
        "🔒 Poll-ul este blocat! Lista unificată de cumpărături a fost generată"
        " și o poți vedea în tab-ul dedicat."
    )
  else:
    if not user_name:
      st.info("Te rog introdu numele de mai sus pentru a putea bifa opțiunile.")
    else:
      if user_name not in m_poll["voturi_useri"]:
        m_poll["voturi_useri"][user_name] = []

      st.subheader("Ce vrei să punem pe listă?")
      selected_items = []
      for cat, items in m_poll["opțiuni_existente"].items():
        st.markdown(f"**{cat}**")
        for item in items:
          is_checked = item in m_poll["voturi_useri"][user_name]
          if st.checkbox(item, value=is_checked, key=f"poll_{cat}_{item}"):
            selected_items.append(item)

      m_poll["voturi_useri"][user_name] = selected_items
      save_data(data)

      # Adăugare custom item
      with st.form("add_custom_food", clear_on_submit=True):
        custom_add = st.text_input(
            "Adaugă altceva (ex: Maioneză, Halloumi, etc.)"
        )
        submitted_c = st.form_submit_button("Adaugă la opțiuni")
        if submitted_c and custom_add:
          m_poll["custom_items"].append(
              {"nume": custom_add, "adăugat_de": user_name}
          )
          save_data(data)
          st.success(f"S-a adăugat '{custom_add}'!")
          st.rerun()

      if m_poll["custom_items"]:
        st.markdown("**Alte opțiuni adăugate de grup:**")
        for ci in m_poll["custom_items"]:
          st.write(f"- {ci['nume']} *(de {ci['adăugat_de']})*")

    st.markdown("---")
    if st.button("🔒 LOCK POLL & Generează Lista de Cumpărături"):
      final_shopping = []
      all_chosen = set()
      for u, items in m_poll["voturi_useri"].items():
        all_chosen.update(items)
      for ci in m_poll["custom_items"]:
        all_chosen.add(ci["nume"])

      for item in all_chosen:
        final_shopping.append(
            {"item": item, "cumpărat": False, "responsabil": ""}
        )

      data["shopping_list"] = final_shopping
      m_poll["locked"] = True
      save_data(data)
      st.success("Lista de cumpărături a fost generată cu succes!")
      st.rerun()

# ================= TAB 3: LISTA CUMPĂRĂTURI =================
with tab3:
  st.header("🛒 Lista de Cumpărături Unificată")
  shopping = data.get("shopping_list", [])

  if not shopping:
    st.info(
        "Lista este goală. Mergi în tab-ul 'Poll Mâncare' și dă 'Lock' după ce"
        " ați votat!"
    )
  else:
    buyer = st.text_input("Numele tău (pentru a bifa ce cumperi):", key="buyer")
    for i, row in enumerate(shopping):
      col_chk, col_lbl, col_resp = st.columns([1, 4, 3])
      with col_chk:
        checked = st.checkbox("", value=row["cumpărat"], key=f"shop_{i}")
        if checked != row["cumpărat"]:
          data["shopping_list"][i]["cumpărat"] = checked
          if checked and buyer:
            data["shopping_list"][i]["responsabil"] = buyer
          save_data(data)
      with col_lbl:
        st.write(row["item"])
      with col_resp:
        if row["responsabil"]:
          st.caption(f"Cumpărat de: **{row['responsabil']}**")

# ================= TAB 4: ACTIVITĂȚI =================
with tab4:
  st.header("🎯 Idei & Votare Activități")
  st.markdown(
      "Votează ce vrei să faceți. Când o activitate are votul tuturor"
      " (4/4), devine bătută în cuie!"
  )

  act_user = st.text_input("Numele tău pentru vot:", key="act_user")
  activitati = data.get("activități", [])
  total_persoane = data["cabana"]["persoane"]

  for i, act in enumerate(activitati):
    voters = act.get("voturi", [])
    has_voted = act_user in voters if act_user else False

    col_v1, col_v2, col_v3 = st.columns([3, 1, 2])
    with col_v1:
      st.markdown(f"**{act['nume']}**")
    with col_v2:
      if act_user:
        voted_now = st.checkbox(
            "Vot", value=has_voted, key=f"act_vote_{i}"
        )
        if voted_now and not has_voted:
          if act_user not in data["activități"][i]["voturi"]:
            data["activități"][i]["voturi"].append(act_user)
            save_data(data)
            st.rerun()
        elif not voted_now and has_voted:
          if act_user in data["activități"][i]["voturi"]:
            data["activități"][i]["voturi"].remove(act_user)
            save_data(data)
            st.rerun()
    with col_v3:
      count = len(voters)
      if count >= total_persoane:
        st.success(f"✅ Confirmat ({count}/{total_persoane})")
      else:
        st.info(f"Voturi: {count}/{total_persoane}")

  with st.form("add_activity", clear_on_submit=True):
    new_act = st.text_input("Propune o nouă activitate:")
    submitted_act = st.form_submit_button("Adaugă idee")
    if submitted_act and new_act:
      data["activități"].append(
          {"nume": new_act, "voturi": [], "confirmat": False}
      )
      save_data(data)
      st.success("Propunere adăugată!")
      st.rerun()

# ================= TAB 5: BUGET & SMART SPLIT =================
with tab5:
  st.header("💸 Buget & Smart Split")
  cheltuieli = data.get("cheltuieli", [])
  total_platit = sum(ch["sumă"] for ch in cheltuieli)
  cost_cabana = data["cabana"]["preț_total"]
  total_general = cost_cabana + total_platit

  col_b1, col_b2 = st.columns(2)
  col_b1.metric("Cost Cabana", f"{cost_cabana} RON")
  col_b2.metric("Alte Cheltuieli", f"{total_platit} RON")

  st.markdown(f"### Total General: **{total_general} RON**")
  share_per_persoana = total_general / data["cabana"]["persoane"]
  st.info(
      f"💡 De plată / decontat per persoană (pentru 4 persoane): **"
      f"{share_per_persoana:.2f} RON**"
  )

  st.subheader("Istoric Plăți")
  for ch in cheltuieli:
    st.write(
        f"- **{ch['persoană']}**: a plătit *{ch['descriere']}* — **{ch['sumă']}"
        " RON**"
    )

  with st.form("add_expense_form", clear_on_submit=True):
    st.subheader("Adaugă o cheltuială nouă (ex: cumpărături magazin)")
    p_nume = st.text_input("Numele tău")
    p_desc = st.text_input("Ce ai plătit?")
    p_suma = st.number_input("Sumă (RON)", min_value=0.0, step=10.0)
    submitted_exp = st.form_submit_button("Adaugă cheltuiala")
    if submitted_exp and p_nume and p_desc:
      data["cheltuieli"].append(
          {"persoană": p_nume, "descriere": p_desc, "sumă": p_suma}
      )
      save_data(data)
      st.success("Cheltuială adăugată!")
      st.rerun()

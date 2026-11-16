import json
import os
import streamlit as st

DATA_FILE = "data.json"

# Lista fixă de participanți
USERS = ["Alexandra", "Cătălina", "Stefan", "Mihai"]

# Date reale ale cabanei și structura inițială
DEFAULT_DATA = {
    "cabana": {
        "nume": "Cazare cabana tip A",
        "locație": "Bologa, Cluj County 407471, România",
        "link_airbnb": (
            "https://www.airbnb.com.ro/rooms/964314240212909855?unique_share_id=a8335210-85f2-4a76-9667-38d7ebc3ac98&viralityEntryPoint=1&s=76"
        ),
        "link_maps_destinatie": (
            "https://www.google.com/maps/search/?api=1&query=Bologa,+Cluj+County+407471"
        ),
        "perioada": "28 - 30 Noiembrie",
        "nopți": 2,
        "persoane": len(USERS),
        "preț_total": 1128,
        "preț_pe_noapte": 564,
        "rute": {
            "cluj_text": (
                "Cluj-Napoca -> Huedin -> Bologa (~1h, 60 km pe E60)"
            ),
            "cluj_link": "https://goo.gl/maps/cfi335DZxiTX6zs19?g_st=ac",
            "bucuresti_text": (
                "București -> Brașov -> Sibiu -> Sebeș -> Turda -> Cluj ->"
                " Bologa (~6h 30m)"
            ),
            "bucuresti_link": (
                "https://www.google.com/maps/dir/București/Bologa,+407471"
            ),
        },
        "highlights": [
            "Cabana tip A-frame",
            "Grătar / Grill exterior",
            "Zonă liniștită aproape de Cetatea Bologa",
            "Wi-Fi & Parcare",
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
            "Băuturi": [
                "Bere la sticlă/doză",
                "Vin alb/roșu",
                "Tărie",
                "Apă plată / minerală",
                "Sucuri",
                "Cafea",
            ],
        },
        "voturi_useri": {u: [] for u in USERS},
        "custom_items": [],
    },
    "shopping_list": [],
    "activități": [
        {
            "nume": "Vizită la Cetatea Bologa & Moara de apă",
            "voturi": [],
            "confirmat": False,
        },
        {
            "nume": "Drumeție la Cascada Vălul Miresei (Răchițele)",
            "voturi": [],
            "confirmat": False,
        },
        {"nume": "Seară de board games & mafia", "voturi": [], "confirmat": False},
        {"nume": "Grătar & foc de tabără", "voturi": [], "confirmat": False},
    ],
    "cheltuieli": [],
}


def load_data():
  if os.path.exists(DATA_FILE):
    try:
      with open(DATA_FILE, "r", encoding="utf-8") as f:
        loaded = json.load(f)
        # Actualizăm mereu detaliile cabanei din cod ca să reflecte ultimele modificări
        loaded["cabana"] = DEFAULT_DATA["cabana"]
        return loaded
    except Exception:
      return DEFAULT_DATA
  return DEFAULT_DATA


def save_data(data):
  with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)


data = load_data()

st.set_page_config(
    page_title="Cabana tip A - Bologa 🏡", page_icon="🏔️", layout="centered"
)

st.title("🏔️ Weekend la Cabană tip A — Bologa")
st.markdown("---")

# Tab-uri pentru organizare curată
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏡 Cabana & Info",
    "🍔 Poll Mâncare & Băuturi",
    "🛒 Lista Cumpărături",
    "🎯 Activități",
    "💸 Buget & Smart Split",
])

# ================= TAB 1: CABANA & INFO =================
with tab1:
  cabana = data.get("cabana", {})
  st.header(f"🏡 {cabana.get('nume')}")

  col1, col2, col3 = st.columns(3)
  col1.metric("Preț Total", f"{cabana.get('preț_total')} RON")
  col2.metric("Preț / Noapte", f"{cabana.get('preț_pe_noapte')} RON")
  col3.metric(
      "Preț / Persoană",
      f"{cabana.get('preț_total') // len(USERS)} RON",
  )

  st.markdown(
      f"📅 **Perioada:** {cabana.get('perioada')} ({cabana.get('nopți')} nopți)"
  )
  st.markdown(f"📍 **Adresă:** {cabana.get('locație')}")

  c_link1, c_link2 = st.columns(2)
  with c_link1:
    st.link_button("🔗 Vezi pe Airbnb", cabana.get("link_airbnb"))
  with c_link2:
    st.link_button("📍 Locație pe Hartă", cabana.get("link_maps_destinatie"))

  st.subheader("🚗 Cum ajungem")
  rute = cabana.get("rute", {})

  col_r1, col_r2 = st.columns(2)
  with col_r1:
    st.info(f"**Din Cluj-Napoca:**\n\n{rute.get('cluj_text')}")
    st.link_button("🗺️ Traseu din Cluj", rute.get("cluj_link"))
  with col_r2:
    st.info(f"**Din București:**\n\n{rute.get('bucuresti_text')}")
    st.link_button("🗺️ Traseu din București", rute.get("bucuresti_link"))

  st.subheader("✨ Highlights & Facilități")
  for h in cabana.get("highlights", []):
    st.write(f"- {h}")

# ================= TAB 2: POLL MÂNCARE =================
with tab2:
  st.header("🍔 Poll Mâncare & Băuturi")
  user_name = st.selectbox("Cine ești?", USERS, key="voter_name")

  m_poll = data.get("poll_mâncare", {})

  if m_poll["locked"]:
    st.warning(
        "🔒 Poll-ul este blocat! Lista unificată de cumpărături a fost generată"
        " și o poți vedea în tab-ul următor."
    )
    if st.button("🔓 Deblochează Poll-ul (dacă mai vreți să modificați)"):
      m_poll["locked"] = False
      save_data(data)
      st.rerun()
  else:
    if user_name not in m_poll["voturi_useri"]:
      m_poll["voturi_useri"][user_name] = []

    st.subheader(f"Ce vrei să punem pe listă, {user_name}?")
    selected_items = []
    for cat, items in m_poll["opțiuni_existente"].items():
      st.markdown(f"**{cat}**")
      for item in items:
        is_checked = item in m_poll["voturi_useri"][user_name]
        if st.checkbox(item, value=is_checked, key=f"poll_{cat}_{item}"):
          selected_items.append(item)

    if selected_items != m_poll["voturi_useri"][user_name]:
      m_poll["voturi_useri"][user_name] = selected_items
      save_data(data)

    # Adăugare custom item
    with st.form("add_custom_food", clear_on_submit=True):
      custom_add = st.text_input(
          "Adaugă altceva (ex: Maioneză, Halloumi, Aperol etc.)"
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
        st.write(f"- {ci['nume']} *(adăugat de {ci['adăugat_de']})*")

    st.markdown("---")
    if st.button("🔒 LOCK POLL & Generează Lista de Cumpărături"):
      final_shopping = []
      all_chosen = set()
      for u, items in m_poll["voturi_useri"].items():
        all_chosen.update(items)
      for ci in m_poll["custom_items"]:
        all_chosen.add(ci["nume"])

      for item in sorted(all_chosen):
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
        "Lista este goală. Mergi în tab-ul 'Poll Mâncare' și apasă 'LOCK POLL'"
        " după ce ați votat!"
    )
  else:
    buyer = st.selectbox(
        "Cine bifează cumpărăturile?", USERS, key="buyer"
    )
    for i, row in enumerate(shopping):
      col_chk, col_lbl, col_resp = st.columns([1, 4, 3])
      with col_chk:
        checked = st.checkbox("", value=row["cumpărat"], key=f"shop_{i}")
        if checked != row["cumpărat"]:
          data["shopping_list"][i]["cumpărat"] = checked
          data["shopping_list"][i]["responsabil"] = buyer if checked else ""
          save_data(data)
          st.rerun()
      with col_lbl:
        if row["cumpărat"]:
          st.markdown(f"~~{row['item']}~~")
        else:
          st.write(row["item"])
      with col_resp:
        if row["responsabil"]:
          st.caption(f"Cumpărat de: **{row['responsabil']}**")

# ================= TAB 4: ACTIVITĂȚI =================
with tab4:
  st.header("🎯 Idei & Votare Activități")
  st.markdown(
      f"Votează ce vrei să faceți. Când o activitate are votul tuturor"
      f" ({len(USERS)}/{len(USERS)}), devine bătută în cuie!"
  )

  act_user = st.selectbox("Cine votează?", USERS, key="act_user")
  activitati = data.get("activități", [])
  total_persoane = len(USERS)

  for i, act in enumerate(activitati):
    voters = act.get("voturi", [])
    has_voted = act_user in voters

    col_v1, col_v2, col_v3 = st.columns([3, 1, 2])
    with col_v1:
      st.markdown(f"**{act['nume']}**")
      if voters:
        st.caption(f"Votat de: {', '.join(voters)}")
    with col_v2:
      voted_now = st.checkbox("Vot", value=has_voted, key=f"act_vote_{i}")
      if voted_now and not has_voted:
        data["activități"][i]["voturi"].append(act_user)
        save_data(data)
        st.rerun()
      elif not voted_now and has_voted:
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
          {"nume": new_act, "voturi": [act_user], "confirmat": False}
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
  share_per_persoana = total_general / len(USERS)

  col_b1, col_b2 = st.columns(2)
  col_b1.metric("Cost Cabana", f"{cost_cabana} RON")
  col_b2.metric("Alte Cheltuieli", f"{total_platit:.2f} RON")

  st.markdown(f"### Total General: **{total_general:.2f} RON**")
  st.info(
      f"💡 Parte egală per persoană ({len(USERS)} persoane): **"
      f"{share_per_persoana:.2f} RON**"
  )

  # Calcul cât a plătit fiecare vs cât are de dat/primit (pentru cheltuielile extra)
  st.subheader("Situație per persoană (cheltuieli extra)")
  share_extra = total_platit / len(USERS)
  for u in USERS:
    platit_u = sum(ch["sumă"] for ch in cheltuieli if ch["persoană"] == u)
    balanta = platit_u - share_extra
    if balanta > 0:
      st.write(
          f"- **{u}**: a plătit {platit_u:.2f} RON → **are de primit"
          f" {balanta:.2f} RON**"
      )
    elif balanta < 0:
      st.write(
          f"- **{u}**: a plătit {platit_u:.2f} RON → **are de dat"
          f" {abs(balanta):.2f} RON**"
      )
    else:
      st.write(f"- **{u}**: a plătit {platit_u:.2f} RON → **pe zero**")

  st.markdown("---")
  st.subheader("Istoric Plăți")
  if not cheltuieli:
    st.caption("Nu a fost adăugată nicio cheltuială încă.")
  for ch in cheltuieli:
    st.write(
        f"- **{ch['persoană']}**: a plătit *{ch['descriere']}* — **{ch['sumă']}"
        " RON**"
    )

  with st.form("add_expense_form", clear_on_submit=True):
    st.subheader("Adaugă o cheltuială nouă")
    p_nume = st.selectbox("Cine a plătit?", USERS)
    p_desc = st.text_input("Ce ai plătit? (ex: Avans cabană, Cumpărături Lidl)")
    p_suma = st.number_input("Sumă (RON)", min_value=0.0, step=10.0)
    submitted_exp = st.form_submit_button("Adaugă cheltuiala")
    if submitted_exp and p_desc and p_suma > 0:
      data["cheltuieli"].append(
          {"persoană": p_nume, "descriere": p_desc, "sumă": p_suma}
      )
      save_data(data)
      st.success("Cheltuială adăugată!")
      st.rerun()

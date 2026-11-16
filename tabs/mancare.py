import streamlit as st
from utils import save_data

def render(data):
    st.subheader("🍔 Poll Mâncare & Băuturi")
    users = data["cabana"].get("utilizatori", [])
    user_name = st.selectbox("Cine ești?", users, key="voter_name")

    m_poll = data.get("poll_mâncare", {})

    if m_poll["locked"]:
        st.warning("🔒 Poll-ul este blocat! Lista unificată de cumpărături a fost generată.")
        if st.button("🔓 Deblochează Poll-ul"):
            m_poll["locked"] = False
            save_data(data)
            st.rerun()
    else:
        if user_name not in m_poll["voturi_useri"]:
            m_poll["voturi_useri"][user_name] = []

        st.markdown(f"**Ce vrei să punem pe listă, {user_name}?**")
        selected_items = []
        for cat, items in m_poll["opțiuni_existente"].items():
            st.markdown(f"*{cat}*")
            for item in items:
                is_checked = item in m_poll["voturi_useri"][user_name]
                if st.checkbox(item, value=is_checked, key=f"poll_{cat}_{item}"):
                    selected_items.append(item)

        if selected_items != m_poll["voturi_useri"][user_name]:
            m_poll["voturi_useri"][user_name] = selected_items
            save_data(data)

        with st.form("add_custom_food", clear_on_submit=True):
            custom_add = st.text_input("Adaugă altceva (ex: Maioneză, Halloumi etc.)")
            submitted_c = st.form_submit_button("Adaugă la opțiuni")
            if submitted_c and custom_add:
                m_poll["custom_items"].append({"nume": custom_add, "adăugat_de": user_name})
                save_data(data)
                st.success(f"S-a adăugat '{custom_add}'!")
                st.rerun()

        if m_poll["custom_items"]:
            st.markdown("**Alte opțiuni adăugate:**")
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

            for item in sorted(all_chosen):
                final_shopping.append({"item": item, "cumpărat": False, "responsabil": ""})

            data["shopping_list"] = final_shopping
            m_poll["locked"] = True
            save_data(data)
            st.success("Lista generată cu succes!")
            st.rerun()

import streamlit as st
from utils import save_data

def render(data):
    st.subheader("🛒 Lista de Cumpărături Unificată")
    shopping = data.get("shopping_list", [])
    users = data["cabana"].get("utilizatori", [])

    if not shopping:
        st.info("Lista este goală. Blochează poll-ul în tab-ul anterior.")
    else:
        buyer = st.selectbox("Cine bifează cumpărăturile?", users, key="buyer")
        for i, row in enumerate(shopping):
            col_chk, col_lbl, col_resp = st.columns([1, 4, 3])
            with col_chk:
                checked = st.checkbox("", value=row["cumpărat"], key=f"shop_{i}")
                if checked != row["cumpărat"]:
                    data["shopping_list"][i]["cumpărat"] = checked
                    data["shopping_list"][i]["responsabil"] = buyer

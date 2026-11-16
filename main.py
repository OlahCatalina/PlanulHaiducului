import streamlit as st

st.set_page_config(
    page_title="Plan Cabană MVP", page_icon="🏔️", layout="centered"
)

st.title("🏔️ Planificare Weekend la Cabană")
st.success("Felicitări! Aplicația ta rulează cu succes pe Streamlit Cloud! 🚀")

st.markdown("---")
st.subheader("Test de interacțiune:")
nume = st.text_input("Cum te numești?")

if nume:
  st.write(
      f"Salut, **{nume}**! Infrastructura este pregătită. În pasul următor"
      " putem adăuga logica de cabană, mâncare și buget pe care am discutat-o."
  )

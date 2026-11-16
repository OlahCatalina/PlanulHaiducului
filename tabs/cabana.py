import streamlit as st

def render(data):
    cabana = data.get("cabana", {})
    users = cabana.get("utilizatori", [])
    
    st.subheader(f"🏡 {cabana.get('nume')}")

    # Secțiunea Preț (3 coloane pe un singur rând)
    st.markdown("### 💰 Preț")
    col_p1, col_p2, col_p3 = st.columns(3)
    col_p1.metric("Total", f"{cabana.get('preț_total')} RON")
    col_p2.metric("Pe noapte", f"{cabana.get('preț_pe_noapte')} RON", f"{cabana.get('nopți')} nopți")
    col_p3.metric("De persoană", f"{cabana.get('preț_total') // max(1, len(users))} RON")

    st.markdown("---")

    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.markdown(f"**📅 Perioada:** {cabana.get('perioada')} ({cabana.get('nopți')} nopți)")
        st.markdown(f"📍 **Adresă:** {cabana.get('locație')}")
    with col_d2:
        st.markdown(f"👥 **Grup:** {len(users)} persoane ({', '.join(users)})")

    c_link1, c_link2 = st.columns(2)
    with c_link1:
        st.link_button("🔗 Vezi pe Airbnb", cabana.get("link_airbnb"))
    with c_link2:
        st.link_button("📍 Locație Hartă", cabana.get("link_maps_destinatie"))

    st.markdown("---")
    st.subheader("🚗 Cum ajungem")
    rute = cabana.get("rute", {})
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        st.info(f"**Din Cluj:**\n{rute.get('cluj_text')}")
        st.link_button("🗺️ Traseu Cluj", rute.get("cluj_link"))
    with col_r2:
        st.info(f"**Din București:**\n{rute.get('bucuresti_text')}")
        st.link_button("🗺️ Traseu București", rute.get("bucuresti_link"))

    st.markdown("---")
    st.subheader("✨ Highlights")
    for h in cabana.get("highlights", []):
        st.write(f"- {h}")

import streamlit as st


def render(data, users, save_data):
  st.subheader("🎯 Votare Activități")
  act_user = st.selectbox("Cine votează?", users, key="act_user")
  activitati = data.get("activități", [])
  total_persoane = len(users)

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
    new_act = st.text_input("Propune o activitate:")
    submitted_act = st.form_submit_button("Adaugă idee")
    if submitted_act and new_act:
      data["activități"].append(
          {"nume": new_act, "voturi": [act_user], "confirmat": False}
      )
      save_data(data)
      st.success("Adăugat!")
      st.rerun()

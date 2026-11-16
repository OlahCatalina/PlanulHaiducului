import streamlit as st


def render(data, users, save_data):
  st.subheader("💸 Buget & Smart Split")
  cheltuieli = data.get("cheltuieli", [])
  total_platit = sum(ch["sumă"] for ch in cheltuieli)
  cost_cabana = data["cabana"]["preț_total"]
  total_general = cost_cabana + total_platit
  share_per_persoana = total_general / len(users)

  col_b1, col_b2 = st.columns(2)
  col_b1.metric("Cost Cabana", f"{cost_cabana} RON")
  col_b2.metric("Alte Cheltuieli", f"{total_platit:.2f} RON")

  st.markdown(f"### Total General: **{total_general:.2f} RON**")
  st.info(f"💡 De persoană: **{share_per_persoana:.2f} RON**")

  st.markdown("**Situație per persoană (extra):**")
  share_extra = total_platit / len(users)
  for u in users:
    platit_u = sum(ch["sumă"] for ch in cheltuieli if ch["persoană"] == u)
    balanta = platit_u - share_extra
    if balanta > 0:
      st.write(f"- **{u}**: are de primit **{balanta:.2f} RON**")
    elif balanta < 0:
      st.write(f"- **{u}**: are de dat **{abs(balanta):.2f} RON**")
    else:
      st.write(f"- **{u}**: pe zero")

  st.markdown("---")
  st.subheader("Istoric Plăți")
  for ch in cheltuieli:
    st.write(f"- **{ch['persoană']}**: *{ch['descriere']}* — **{ch['sumă']} RON**")

  with st.form("add_expense_form", clear_on_submit=True):
    st.subheader("Adaugă cheltuială")
    p_nume = st.selectbox("Cine a plătit?", users)
    p_desc = st.text_input("Descriere (ex: Cumpărături Lidl)")
    p_suma = st.number_input("Sumă (RON)", min_value=0.0, step=10.0)
    submitted_exp = st.form_submit_button("Adaugă")
    if submitted_exp and p_desc and p_suma > 0:
      data["cheltuieli"].append(
          {"persoană": p_nume, "descriere": p_desc, "sumă": p_suma}
      )
      save_data(data)
      st.success("Adăugat!")
      st.rerun()

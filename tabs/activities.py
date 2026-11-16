import streamlit as st


def render(data, users, save_data):
  """Renders the Activities voting tab where participants can vote on existing

  ideas or propose new ones.
  """
  st.subheader("🎯 Activity Voting")

  # Select the active user casting votes
  act_user = st.selectbox("Who is voting?", users, key="act_user")

  # Retrieve the list of activities and total participant count
  activities = data.get("activities", [])
  total_users = len(users)

  # Display each proposed activity along with its voting checkbox and status
  for i, act in enumerate(activities):
    voters = act.get("votes", [])
    has_voted = act_user in voters

    col_v1, col_v2, col_v3 = st.columns([3, 1, 2])

    # Column 1: Activity name and list of users who voted for it
    with col_v1:
      st.markdown(f"**{act['name']}**")
      if voters:
        st.caption(f"Voted by: {', '.join(voters)}")

    # Column 2: Interactive vote checkbox for the selected user
    with col_v2:
      voted_now = st.checkbox("Vote", value=has_voted, key=f"act_vote_{i}")
      if voted_now and not has_voted:
        data["activities"][i]["votes"].append(act_user)
        save_data(data)
        st.rerun()
      elif not voted_now and has_voted:
        data["activities"][i]["votes"].remove(act_user)
        save_data(data)
        st.rerun()

    # Column 3: Vote counter and confirmation badge when everyone agrees
    with col_v3:
      count = len(voters)
      if count >= total_users:
        st.success(f"✅ Confirmed ({count}/{total_users})")
      else:
        st.info(f"Votes: {count}/{total_users}")

  # Form to propose a new activity (automatically adds the proposer's vote)
  with st.form("add_activity", clear_on_submit=True):
    new_act = st.text_input("Propose a new activity:")
    submitted_act = st.form_submit_button("Add idea")
    if submitted_act and new_act:
      data["activities"].append(
          {"name": new_act, "votes": [act_user], "confirmed": False}
      )
      save_data(data)
      st.success("Added!")
      st.rerun()

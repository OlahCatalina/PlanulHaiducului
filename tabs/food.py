import streamlit as st
from utils import save_data


def render(data, users=None, save_fn=save_data):
  """Renders the Food & Drinks Poll tab where participants vote on existing

  categories, propose custom items, and lock the poll to generate the unified
  shopping list.
  """
  st.subheader("🍔 Food & Drinks Poll")

  # Fallback to users stored inside cabin data if not explicitly passed
  if users is None:
    users = data.get("cabin", {}).get("users", [])

  # Select the active participant casting votes
  user_name = st.selectbox("Who are you?", users, key="voter_name")

  # Retrieve the food poll dictionary from the main data state
  f_poll = data.get("food_poll", {})

  # If the poll is locked, prevent edits and allow unlocking
  if f_poll.get("locked", False):
    st.warning(
        "🔒 The poll is locked! The unified shopping list has been generated."
    )
    if st.button("🔓 Unlock Poll"):
      f_poll["locked"] = False
      save_fn(data)
      st.rerun()
  else:
    # Ensure the selected user has an entry in user_votes
    if "user_votes" not in f_poll:
      f_poll["user_votes"] = {}
    if user_name not in f_poll["user_votes"]:
      f_poll["user_votes"][user_name] = []

    st.markdown(f"**What should we put on the list, {user_name}?**")
    selected_items = []

    # Display existing food/drink categories and checkboxes for each item
    for cat, items in f_poll.get("existing_options", {}).items():
      st.markdown(f"*{cat}*")
      for item in items:
        is_checked = item in f_poll["user_votes"][user_name]
        if st.checkbox(item, value=is_checked, key=f"poll_{cat}_{item}"):
          selected_items.append(item)

    # Persist vote updates immediately when checkboxes change
    if selected_items != f_poll["user_votes"][user_name]:
      f_poll["user_votes"][user_name] = selected_items
      save_fn(data)

    # Form for proposing custom food or drink items
    with st.form("add_custom_food", clear_on_submit=True):
      custom_add = st.text_input(
          "Add something else (e.g., Mayo, Halloumi, etc.)"
      )
      submitted_c = st.form_submit_button("Add to options")
      if submitted_c and custom_add:
        f_poll.setdefault("custom_items", []).append(
            {"name": custom_add, "added_by": user_name}
        )
        save_fn(data)
        st.success(f"Added '{custom_add}'!")
        st.rerun()

    # Display all custom items proposed so far
    if f_poll.get("custom_items"):
      st.markdown("**Other added options:**")
      for ci in f_poll["custom_items"]:
        st.write(f"- {ci['name']} *(by {ci['added_by']})*")

    st.markdown("---")

    # Lock the poll and aggregate all voted and custom items into shopping_list
    if st.button("🔒 LOCK POLL & Generate Shopping List"):
      final_shopping = []
      all_chosen = set()

      for u, items in f_poll.get("user_votes", {}).items():
        all_chosen.update(items)
      for ci in f_poll.get("custom_items", []):
        all_chosen.add(ci["name"])

      for item in sorted(all_chosen):
        final_shopping.append(
            {"item": item, "purchased": False, "responsible": ""}
        )

      data["shopping_list"] = final_shopping
      f_poll["locked"] = True
      save_fn(data)
      st.success("Shopping list generated successfully!")
      st.rerun()
 
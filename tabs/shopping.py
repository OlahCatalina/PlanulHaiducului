import streamlit as st
from utils import save_data


def render(data, users=None, save_fn=save_data):
  """Renders the Unified Shopping List tab where participants can check off items

  and automatically assign themselves as the responsible buyer.
  """
  st.subheader("🛒 Unified Shopping List")

  # Retrieve the shopping list and fallback to cabin users if not passed directly
  shopping = data.get("shopping_list", [])
  if users is None:
    users = data.get("cabin", {}).get("users", [])

  if not shopping:
    st.info(
        "The list is empty. Lock the poll in the previous tab to generate it."
    )
  else:
    # Select the active user checking off items
    buyer = st.selectbox("Who is checking off items?", users, key="buyer")

    # Iterate through each shopping list item
    for i, row in enumerate(shopping):
      col_chk, col_lbl, col_resp = st.columns([1, 4, 3])

      # Column 1: Checkbox to toggle purchased status
      with col_chk:
        checked = st.checkbox(
            "Purchased",
            value=row.get("purchased", False),
            key=f"shop_{i}",
            label_visibility="collapsed",
        )
        if checked != row.get("purchased", False):
          data["shopping_list"][i]["purchased"] = checked
          data["shopping_list"][i]["responsible"] = buyer if checked else ""
          save_fn(data)
          st.rerun()

      # Column 2: Item name (strikethrough if already purchased)
      with col_lbl:
        if row.get("purchased", False):
          st.markdown(f"~~{row['item']}~~")
        else:
          st.write(row["item"])

      # Column 3: Badge showing who bought the item
      with col_resp:
        if row.get("responsible"):
          st.caption(f"By: **{row['responsible']}**")

import streamlit as st


def render(data, users, save_data):
  """Renders the Budget & Smart Split tab, calculating total costs,

  individual shares, balances for extra expenses, and a form to log new payments.
  """
  st.subheader("💸 Budget & Smart Split")

  # Retrieve expenses list and cabin cost from the structured dictionary
  expenses = data.get("expenses", [])
  total_paid = sum(exp["amount"] for exp in expenses)
  cabin_cost = data.get("cabin", {}).get("price_total", 0)

  # Calculate grand total and equal share per person
  grand_total = cabin_cost + total_paid
  share_per_person = grand_total / len(users)

  # Top summary metrics for cabin cost vs extra expenses
  col_b1, col_b2 = st.columns(2)
  col_b1.metric("Cabin Cost", f"{cabin_cost} RON")
  col_b2.metric("Other Expenses", f"{total_paid:.2f} RON")

  st.markdown(f"### Grand Total: **{grand_total:.2f} RON**")
  st.info(f"💡 Per person share: **{share_per_person:.2f} RON**")

  # Per-person balance breakdown for extra expenses
  st.markdown("**Per-person balance (extra expenses):**")
  share_extra = total_paid / len(users)
  for u in users:
    paid_u = sum(exp["amount"] for exp in expenses if exp["person"] == u)
    balance = paid_u - share_extra
    if balance > 0:
      st.write(f"- **{u}**: is owed **{balance:.2f} RON**")
    elif balance < 0:
      st.write(f"- **{u}**: owes **{abs(balance):.2f} RON**")
    else:
      st.write(f"- **{u}**: settled")

  st.markdown("---")
  st.subheader("Payment History")
  if not expenses:
    st.caption("No extra expenses added yet.")
  for exp in expenses:
    st.write(f"- **{exp['person']}**: *{exp['description']}* — **{exp['amount']} RON**")

  # Form to add a new expense entry
  with st.form("add_expense_form", clear_on_submit=True):
    st.subheader("Add new expense")
    p_name = st.selectbox("Who paid?", users)
    p_desc = st.text_input("Description (e.g., Lidl groceries)")
    p_sum = st.number_input("Amount (RON)", min_value=0.0, step=10.0)
    submitted_exp = st.form_submit_button("Add expense")
    if submitted_exp and p_desc and p_sum > 0:
      expenses.append(
          {"person": p_name, "description": p_desc, "amount": p_sum}
      )
      save_data(data)
      st.success("Expense added!")
      st.rerun()
 
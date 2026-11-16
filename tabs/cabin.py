import streamlit as st


def render(data, users=None):
  """Renders the Cabin & Info tab, displaying pricing breakdown, trip dates,

  group details, booking/location links, travel routes, and property highlights.
  """
  cabin = data.get("cabin", {})

  if users is None:
    users = cabin.get("users", [])

  # Cabin title rendered as an h2 header for a slightly larger appearance
  st.markdown(f"## 🏡 {cabin.get('name', 'A-frame Cabin Stay')}")

  # Price breakdown section explicitly structured into 3 horizontal columns
  st.markdown("### 💰 Price")
  col_p1, col_p2, col_p3 = st.columns(3)
  with col_p1:
    st.metric("Total", f"{cabin.get('price_total', 0)} RON")
  with col_p2:
    st.metric(
        "Per night",
        f"{cabin.get('price_per_night', 0)} RON",
        f"{cabin.get('nights', 0)} nights",
    )
  with col_p3:
    st.metric(
        "Per person",
        f"{cabin.get('price_total', 0) // max(1, len(users))} RON",
    )

  st.markdown("---")

  # Dates, location, and participant list
  col_d1, col_d2 = st.columns(2)
  with col_d1:
    st.markdown(
        f"**📅 Period:** {cabin.get('period')} ({cabin.get('nights')} nights)"
    )
    st.markdown(f"📍 **Address:** {cabin.get('location')}")
  with col_d2:
    st.markdown(f"👥 **Group:** {len(users)} people ({', '.join(users)})")

  # External action buttons for Airbnb listing and Google Maps destination
  c_link1, c_link2 = st.columns(2)
  with c_link1:
    if cabin.get("link_airbnb"):
      st.link_button("🔗 View on Airbnb", cabin.get("link_airbnb"))
  with c_link2:
    if cabin.get("link_maps_destination"):
      st.link_button("📍 Map Location", cabin.get("link_maps_destination"))

  st.markdown("---")

  # Travel routes section
  st.subheader("🚗 How to get there")
  routes = cabin.get("routes", {})
  col_r1, col_r2 = st.columns(2)
  with col_r1:
    st.info(f"**From Cluj:**\n{routes.get('cluj_text', '')}")
    if routes.get("cluj_link"):
      st.link_button("🗺️ Cluj Route", routes.get("cluj_link"))
  with col_r2:
    st.info(f"**From Bucharest:**\n{routes.get('bucharest_text', '')}")
    if routes.get("bucharest_link"):
      st.link_button("🗺️ Bucharest Route", routes.get("bucharest_link"))

  st.markdown("---")

  # Property highlights list
  st.subheader("✨ Highlights")
  for h in cabin.get("highlights", []):
    st.write(f"- {h}")

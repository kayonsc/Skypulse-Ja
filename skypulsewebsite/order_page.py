import streamlit as st

st.set_page_config(page_title="Order | SkyPulse Jamaica")

st.title("📦 Place Your Order")

# Ensure a service was selected
if "selected_service" not in st.session_state:
    st.error("⚠️ No service selected. Please go back to the Services page and choose a service.")
    st.stop()

# Retrieve selected service
service = st.session_state["selected_service"]

st.write(f"### You selected: **{service['name']}**")
st.write(f"💰 **Cost:** {service['price']}")

# Customer details
name = st.text_input("Full Name")
email = st.text_input("Email Address")
delivery_address = st.text_area("Delivery Address")

# Proceed to payment
if st.button("Proceed to Payment"):
    st.session_state["customer_info"] = {"name": name, "email": email, "delivery_address": delivery_address}
    st.switch_page("payment_page.py")
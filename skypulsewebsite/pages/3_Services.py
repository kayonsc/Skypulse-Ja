import streamlit as st
import pymysql
from datetime import datetime
import random
import string

st.set_page_config(page_title="Services | SkyPulse Jamaica", layout="wide")

st.title("Choose From Our Wide Range Of Services")

# Add extra spacing below the title
st.markdown("<br><br>", unsafe_allow_html=True)

# Function to connect to the database
def connect_db():
    return pymysql.connect(host="localhost", user="root", password="", database="drone_delivery")

# Function to generate a unique tracking number
def generate_tracking_number():
    return "SPJ-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=6))

# Check if an order has been selected
if "selected_service" not in st.session_state:
    st.session_state["selected_service"] = None

# Define services with names, descriptions, and prices
services = [
    {"name": "Same-Day Delivery", "desc": "Fast delivery of packages within the same day, ideal for urgent or time-sensitive shipments.", "price": 2500, "image": "Same-Day Delivery.jpg"},
    {"name": "Parcel Delivery", "desc": "Standard package delivery for items of various sizes and weights, both local and regional.", "price": 1800, "image": "Parcel Delivery.jpeg"},
    {"name": "Medical Deliveries", "desc": "Transport medical supplies, prescriptions, and emergency healthcare products (e.g., vaccines, blood samples).", "price": 3000, "image": "Medical Deliveries.jpg"},
    {"name": "E-Commerce Deliveries", "desc": "Partner with online stores to deliver products directly to consumers, enhancing customer satisfaction with fast and reliable service.", "price": 2200, "image": "E-Commerce Deliveries.jpg"},
    {"name": "Food and Beverage Delivery", "desc": "Provide fast and secure delivery of food, drinks, and groceries, catering to both individuals and businesses.", "price": 1500, "image": "Food and Beverage Delivery.jpg"},
    {"name": "Document Delivery", "desc": "Secure and confidential delivery of important documents, contracts, and legal papers.", "price": 2000, "image": "Document Delivery.png"},
    {"name": "Retail Product Deliveries", "desc": "Specialize in delivering consumer goods, such as clothing, electronics, and other retail products.", "price": 1800, "image": "Retail Product Deliveries.jpg"},
    {"name": "Gift and Flower Deliveries", "desc": "Send flowers, gifts, and special occasion packages for events like birthdays, anniversaries, or holidays.", "price": 2000, "image": "Gift and Flower Deliveries.jpg"},
    {"name": "Surprise Delivery Service", "desc": "A unique service that allows customers to send surprise gifts or special messages to loved ones or employees.", "price": 2500, "image": "Surprise Delivery Service.jpg"},
    {"name": "Return/Exchange Services", "desc": "Allow customers to return or exchange products via drone, enhancing e-commerce businesses' services.", "price": 2000, "image": "Return_Exchange Services.jpg"},
    {"name": "Drone Rental for Filming or Photography", "desc": "Rent out drones for media professionals who need aerial shots, allowing for scenic views, events, or promotional content.", "price": 10000, "image": "Drone Rental.jpeg"}
]

# If no service is selected, show the services list
if not st.session_state["selected_service"]:
    st.markdown("<br>", unsafe_allow_html=True)  # Adds spacing

    # Split the services into 3 columns
    cols = st.columns(3)

    # Loop to display services in rows of 3 services
    for i in range(0, len(services), 3):
        # For each column, display a service
        for j in range(3):
            service_index = i + j
            if service_index < len(services):
                with cols[j]:
                    service = services[service_index]
                    st.image(service["image"], width=300)
                    st.subheader(service["name"])
                    st.write(service["desc"])
                    st.write(f"💰 **Cost:** ${service['price']} JMD")
                    if st.button(f"Order {service['name']}", key=f"button_{service['name']}"):
                        # Redirect to Member Login page when button is clicked
                        st.session_state["selected_service"] = service
                        st.session_state["redirect_to_login"] = True
                        st.rerun()
                    # Add space **after** the button
                    st.markdown("<br><br>", unsafe_allow_html=True)

        # Add more space between rows
        st.markdown("<br><br><br>", unsafe_allow_html=True)

# If a service has been selected, show the order form and then redirect to login page
if "redirect_to_login" in st.session_state and st.session_state["redirect_to_login"]:
    st.session_state["selected_service"] = None
    st.session_state["redirect_to_login"] = False
    st.markdown('<meta http-equiv="refresh" content="0;URL=/Member_Login">', unsafe_allow_html=True)  # Redirect to 7_member login page
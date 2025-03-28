import streamlit as st
import pymysql
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Customer Reviews | SkyPulse Jamaica", layout="wide")

st.title("⭐ Customer Reviews")

# Function to connect to the database
def connect_db():
    return pymysql.connect(host="localhost", user="root", password="", database="drone_delivery")

# Function to fetch reviews from the database
def fetch_reviews():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT username, service_name, rating, review_text, DATE_FORMAT(review_date, '%b %d, %Y') FROM reviews ORDER BY review_date DESC")
    reviews = cursor.fetchall()
    conn.close()
    return pd.DataFrame(reviews, columns=["Username", "Service", "Rating", "Review", "Date"])

# Function to insert a new review into the database
def submit_review(username, service_name, rating, review_text):
    conn = connect_db()
    cursor = conn.cursor()
    review_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO reviews (username, service_name, rating, review_text, review_date) VALUES (%s, %s, %s, %s, %s)",
                   (username, service_name, rating, review_text, review_date))
    conn.commit()
    conn.close()

# Define available services
services = [
    "Same-Day Delivery", "Parcel Delivery", "Medical Deliveries", "E-Commerce Deliveries", 
    "Food and Beverage Delivery", "Document Delivery", "Retail Product Deliveries", 
    "Gift and Flower Deliveries", "Surprise Delivery Service", "Return/Exchange Services", 
    "Drone Rental for Filming or Photography"
]

# Fetch and display existing reviews
reviews_df = fetch_reviews()

if not reviews_df.empty:
    st.write("### 📝 What Our Customers Say")
    for index, row in reviews_df.iterrows():
        st.markdown(f"""
        <div style="border: 1px solid #ddd; padding: 15px; margin-bottom: 10px; border-radius: 8px;">
            <strong>{row["Username"]}</strong> - ⭐ {row["Rating"]}/5 for {row["Service"]}  
            <p>{row["Review"]}</p>
            <small>{row["Date"]}</small>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("No reviews yet. Be the first to leave a review!")

# Review Button to show the review form on the same page
if st.button("Leave a Review"):
    st.session_state["show_review_form"] = True

# If the review form is shown, display it
if "show_review_form" in st.session_state and st.session_state["show_review_form"]:
    # Review Form
    st.write("### ✍️ Submit Your Review")
    username = st.text_input("Your Name")
    review_text = st.text_area("Write your review here...")

    # Service selection dropdown
    service_name = st.selectbox("Select the service you used:", services)

    # Rating checkboxes
    st.write("Please select your rating:")
    rating = 0
    if st.checkbox("⭐ 1", key="rating_1"):
        rating = 1
    if st.checkbox("⭐ 2", key="rating_2"):
        rating = 2
    if st.checkbox("⭐ 3", key="rating_3"):
        rating = 3
    if st.checkbox("⭐ 4", key="rating_4"):
        rating = 4
    if st.checkbox("⭐ 5", key="rating_5"):
        rating = 5

    if st.button("Submit Review"):
        if username and review_text and service_name and rating > 0:
            submit_review(username, service_name, rating, review_text)
            st.success("✅ Thank you for your review! It has been submitted.")
            st.session_state["show_review_form"] = False  # Hide the form after submission
            st.experimental_rerun()  # Refresh the page to show the new review
        else:
            st.warning("⚠️ Please enter your name, review, select a service, and select a rating before submitting.")
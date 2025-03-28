import streamlit as st
import pymysql

# Set page config
st.set_page_config(page_title="Contact | SkyPulse Jamaica", layout="wide")

# Title and contact information
st.title("Contact Us")
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("<br><br>", unsafe_allow_html=True)

# Function to connect to the database
def connect_db():
    return pymysql.connect(host="localhost", user="root", password="", database="drone_delivery")

# Form to request a call back
st.subheader("Request a Call Back")

# Input fields for the callback form
with st.form(key="callback_form"):
    username = st.text_input("Your Name")
    phone_number = st.text_input("Your Phone Number")

    # Submit button
    submit_button = st.form_submit_button("Submit Request")
    st.markdown("<br><br>", unsafe_allow_html=True)

    st.write("For inquiries, reach us via email: skypulsejamaica@gmail.com or call us at 876-356-3319")

# Insert the callback request into the database
if submit_button:
    if username and phone_number:
        try:
            # Connect to the database and insert the data
            conn = connect_db()
            cursor = conn.cursor()
            
            cursor.execute("INSERT INTO callback_requests (username, phone_number) VALUES (%s, %s)",
                           (username, phone_number))
            conn.commit()
            conn.close()
            st.success("✅ Your request has been submitted. We will get back to you shortly!")
        except Exception as e:
            st.error(f"❌ Error: {e}")
    else:
        st.error("❌ Please fill out all the fields before submitting.")
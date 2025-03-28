import streamlit as st
import pymysql
from PIL import Image
import os

# Function to connect to the database
def connect_db():
    return pymysql.connect(host="localhost", user="root", password="", database="drone_delivery")

# Function to fetch user orders
def fetch_orders(username): 
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT order_id, tracking_no, username, order_date, edd, status, image_path FROM orders WHERE username = %s", (username,))
    orders = cursor.fetchall()
    conn.close()
    return orders

# If user is logged in, show the Orders Page
if st.session_state["logged_in"]:
    st.title("📦 My Orders")
    st.write(f"Welcome, **{st.session_state['username']}**! Here are your orders:")

    # Fetch and display orders
    orders = fetch_orders(st.session_state["username"])

    if orders:
        for order in orders:
            st.write(f"Order ID: {order[0]} - Status: {order[5]}")

            # Display uploaded image if available
            if order[6]:
                st.image(order[6], caption="Order Details Image", use_column_width=True)

    else:
        st.info("No orders found.")

    # Order Image Upload Section
    st.subheader("Upload Order Details Image")
    
    uploaded_image = st.file_uploader("Choose a .jpg file", type=["jpg", "jpeg"])
    
    if uploaded_image is not None:
        # Save the uploaded image
        image_path = f"order_images/{uploaded_image.name}"

        # Save the image to a folder on your server
        if not os.path.exists("order_images"):
            os.makedirs("order_images")
        
        with open(image_path, "wb") as f:
            f.write(uploaded_image.getbuffer())
        
        # Update the image path in the database
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE orders SET image_path = %s WHERE username = %s", (image_path, st.session_state['username']))
        conn.commit()
        conn.close()

        st.success(f"Image uploaded successfully! Image saved as {image_path}")

    # Logout Button
    if st.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state["username"] = ""
        st.rerun()

else:
    st.warning("Please log in to view your orders.")
import streamlit as st
import pymysql
import random
import string
import pandas as pd

# Initialize session state variables if they don't exist
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""

# Function to connect to database
def connect_db():
    return pymysql.connect(host="localhost", user="root", password="", database="drone_delivery")

# Function to fetch user orders
def fetch_orders(username):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT order_id, service_type, tracking_no, username, order_date, edd, status FROM orders WHERE username = %s", (username,))
    orders = cursor.fetchall()
    conn.close()
    return pd.DataFrame(orders, columns=["Order ID", "Service Type", "Tracking No", "Username", "Order Date", "EDD", "Status"])

# Function to generate a random order ID
def generate_order_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

# Function to generate a random 10-digit tracking number
def generate_tracking_number():
    return ''.join(random.choices(string.digits, k=10))

# Predefined service costs
service_prices = {
    'Same-Day Delivery': 2500.00,
    'Parcel Delivery': 1800.00,
    'Medical Supplies Deliveries': 3000.00,
    'E-Commerce Deliveries': 2200.00,
    'Food and Beverage Delivery': 1500.00,
    'Document Delivery': 2000.00,
    'Retail Product Deliveries': 1800.00,
    'Gift and Flower Deliveries': 2000.00,
    'Surprise Delivery Service': 2500.00,
    'Return/Exchange Services': 2000.00,
    'Drone Rental for Filming or Photography': 10000.00
}

# Function to handle order submission
def place_order(username, service_type, payment_method):
    order_id = generate_order_id()
    tracking_number = generate_tracking_number()  # Generate tracking number
    total_cost = service_prices.get(service_type, 0)  # Get price from dictionary
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO orders (order_id, tracking_no, username, service_type, payment_method, total_cost, status) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                   (order_id, tracking_number, username, service_type, payment_method, total_cost, "Pending"))
    conn.commit()
    conn.close()
    st.success(f"✅ Order {order_id} placed successfully! Tracking Number: {tracking_number}")

    # Display payment instructions
    email_address = "support@skypulsejamaica.com"  # Replace with actual email
    if payment_method == "PayPal":
        paypal_url = f"https://www.paypal.com/jm/home"
        st.markdown(f'<a href="{paypal_url}" target="_blank" style="color: blue; font-size: 18px;">Click here to pay with PayPal</a>', unsafe_allow_html=True)
        st.info(f"📧 Use the email **{email_address}** when making the payment through PayPal.")
    elif payment_method == "Bank Transfer":
        st.info(f"🏦 **Bank Transfer Details:**\n\n"
                f"**Bank:** NCB\n"
                f"**Account Name:** Kayon Swaby\n"
                f"**Branch:** 1-7 Knutsford Boulevard\n"
                f"**Account Type:** Personal\n"
                f"**Account Number:** 354398338\n\n"
                f"📧 Use the email **{email_address}** for inquiries.")

# Function to display order status with plane emoji
def show_order_status(order_status):
    statuses = ["Pending", "Processed", "Shipped", "Out for Delivery", "Delivered", "Cancelled"]
    status_positions = {
        "Pending": 0,
        "Processed": 1,
        "Shipped": 2,
        "Out for Delivery": 3,
        "Delivered": 4,
        "Cancelled": 5
    }

    # CSS for the status scale
    status_scale_html = """
        <div style="display: flex; justify-content: space-between; width: 100%; padding: 20px 0;">
            <div style="text-align: center;">Pending</div>
            <div style="text-align: center;">Processed</div>
            <div style="text-align: center;">Shipped</div>
            <div style="text-align: center;">Out for Delivery</div>
            <div style="text-align: center;">Delivered</div>
            <div style="text-align: center;">Cancelled</div>
        </div>
        <div style="position: relative; height: 30px; width: 100%; background-color: #f1f1f1; border-radius: 20px;">
            <div style="position: absolute; top: 5px; left: {left_position}%; font-size: 24px;">✈️</div>
        </div>
    """
    
    # Determine the position of the plane emoji
    left_position = status_positions.get(order_status, 0) * 20  # 0 to 100%

    # Display the status scale with the emoji at the correct position
    st.markdown(status_scale_html.format(left_position=left_position), unsafe_allow_html=True)

# If user is logged in, show dashboard options
if st.session_state["logged_in"]:
    st.title(f"Welcome, {st.session_state['username']}!")

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("📦 View My Orders"):
            st.session_state["view_orders"] = True
            st.session_state["place_order"] = False
            st.rerun()

    with col2:
        if st.button("🛒 Place an Order"):
            st.session_state["view_orders"] = False
            st.session_state["place_order"] = True
            st.rerun()

    # View Orders Page
    if "view_orders" in st.session_state and st.session_state["view_orders"]:
        st.title("📦 My Orders")
        orders_df = fetch_orders(st.session_state["username"])
        if not orders_df.empty:
            order_select = st.selectbox("Select Tracking Number", orders_df["Tracking No"].unique())
            selected_order = orders_df[orders_df["Tracking No"] == order_select]

            st.dataframe(orders_df)

            if not selected_order.empty:
                # Display only the tracking number and status scale
                st.subheader(f"Tracking No: {selected_order['Tracking No'].values[0]}")
                # Display the status scale with the plane emoji
                show_order_status(selected_order['Status'].values[0])

        else:
            st.info("No orders found.")
        
        if st.button("🔙 Back to Dashboard"):
            st.session_state["view_orders"] = False
            st.session_state["place_order"] = False
            st.rerun()

    # Place an Order Page
    if "place_order" in st.session_state and st.session_state["place_order"]:
        st.title("🛒 Place an Order")

        # Dropdown for service selection
        service_type = st.selectbox("📌 Select Service", list(service_prices.keys()))
        total_cost = service_prices.get(service_type, 0)  # Fetch price automatically

        # Display total cost
        st.markdown(f"### 💲 Total Cost: **${total_cost:.2f}**")

        # Payment Method Selection
        payment_method = st.selectbox("💳 Select Payment Method", ["PayPal", "Bank Transfer"])

        if st.button("✅ Submit Order"):
            place_order(st.session_state["username"], service_type, payment_method)

        if st.button("🔙 Back to Dashboard"):
            st.session_state["view_orders"] = False
            st.session_state["place_order"] = False
            st.rerun()

else:
    # Show Login Page
    st.title("🔐 User Login")
    st.markdown("<br><br>", unsafe_allow_html=True)  # Adds vertical space
    st.subheader("Login Here")

    login_username = st.text_input("Username")
    login_password = st.text_input("Password", type="password")

    if st.button("Login"):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (login_username, login_password))
        user = cursor.fetchone()
        conn.close()

        if user:
            st.session_state["logged_in"] = True
            st.session_state["username"] = login_username
            st.success(f"✅ Welcome, {login_username}!")
            st.rerun()
        else:
            st.error("⚠️ Invalid credentials. Please try again.")
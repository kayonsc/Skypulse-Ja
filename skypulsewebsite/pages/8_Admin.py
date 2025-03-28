import streamlit as st
import pymysql
import pandas as pd

# Database Connection Function
def connect_db():
    return pymysql.connect(host="localhost", user="root", password="", database="drone_delivery")

# Function to Fetch All Orders
def fetch_orders():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT order_id, tracking_no, username, "
                   "DATE_FORMAT(order_date, '%b %d, %Y') AS order_date, "
                   "DATE_FORMAT(edd, '%b %d, %Y') AS edd, status FROM orders")
    orders = cursor.fetchall()
    conn.close()
    return pd.DataFrame(orders, columns=["Order ID", "Tracking No", "Username", "Order Date", "EDD", "Status"])

# Admin Login Credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "skypulseadmin"

# Initialize session state if not set
if "admin_logged_in" not in st.session_state:
    st.session_state["admin_logged_in"] = False

# Show login form only if not logged in
if not st.session_state["admin_logged_in"]:
    st.title("🔐 Admin Login")
    
    login_username = st.text_input("Admin Username")
    login_password = st.text_input("Admin Password", type="password")

    if st.button("Login"):
        if login_username == ADMIN_USERNAME and login_password == ADMIN_PASSWORD:
            st.session_state["admin_logged_in"] = True
            st.session_state["admin_username"] = login_username
            st.success("✅ Login Successful!")
            st.rerun()  # Refresh to show orders
        else:
            st.error("❌ Invalid credentials. Please try again.")

# If logged in, show the dashboard
if st.session_state["admin_logged_in"]:
    st.title("📊 Admin Dashboard - Manage Orders")
    st.write(f"👤 Logged in as: **{st.session_state['admin_username']}**")

    # Fetch and display orders
    orders_df = fetch_orders()

    if not orders_df.empty:
        st.write("### 📋 Orders List")
        st.dataframe(orders_df)

        # Dropdown to select order ID
        order_ids = orders_df["Order ID"].tolist()
        selected_order_id = st.selectbox("📌 Select an Order to Update", order_ids, index=0)

        # Ensure selected order exists before accessing it
        selected_order = orders_df[orders_df["Order ID"] == selected_order_id]
        if not selected_order.empty:
            selected_order = selected_order.iloc[0]  # Get the first matching row

            # Display selected order details
            st.write(f"**Tracking No:** {selected_order['Tracking No']}")
            st.write(f"**Current Status:** {selected_order['Status']}")

            # Dropdown for updating status
            new_status = st.selectbox("🔄 Update Order Status", 
                                      ["Pending", "Processed", "Shipped", "Out for Delivery", "Delivered", "Cancelled"], 
                                      index=["Pending", "Processed", "Shipped", "Out for Delivery", "Delivered", "Cancelled"].index(selected_order["Status"]))

            if st.button("✅ Update Status"):
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute("UPDATE orders SET status=%s WHERE order_id=%s", (new_status, selected_order_id))
                conn.commit()
                conn.close()
                st.success(f"✅ Order {selected_order_id} updated to {new_status}")
                st.rerun()  # Refresh page to show update
        else:
            st.warning("⚠️ No order selected or invalid Order ID.")

    else:
        st.info("No orders found.")

    # Logout Button
    if st.button("🚪 Logout"):
        st.session_state["admin_logged_in"] = False
        st.rerun()  # Refresh to show login page again
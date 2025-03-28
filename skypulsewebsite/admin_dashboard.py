import streamlit as st
import pymysql
import pandas as pd

# Function to connect to database
def connect_db():
    return pymysql.connect(host="localhost", user="root", password="", database="drone_delivery")

# Function to fetch all orders
def fetch_orders():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT order_id, tracking_no, username, "
                   "DATE_FORMAT(order_date, '%b %d, %Y') AS order_date, "
                   "DATE_FORMAT(edd, '%b %d, %Y') AS edd, status FROM orders")
    orders = cursor.fetchall()
    conn.close()
    return pd.DataFrame(orders, columns=["Order ID", "Tracking No", "Username", "Order Date", "EDD", "Status"])

# Ensure admin is logged in
if "admin_logged_in" not in st.session_state or not st.session_state["admin_logged_in"]:
    st.error("🚫 Please log in as an admin first.")
    st.stop()  # Stop execution if not logged in

# Admin Dashboard UI
st.title("📊 Admin Dashboard - Manage Orders")
st.write(f"👤 Logged in as: **{st.session_state['admin_username']}**")

# Fetch and display orders
orders_df = fetch_orders()

if not orders_df.empty:
    st.write("### 📋 Orders List")
    st.dataframe(orders_df)
else:
    st.info("No orders found.")

# Order Status Update Section
st.write("### 🔄 Update Order Status")

for index, row in orders_df.iterrows():
    # Dropdown for selecting new status
    new_status = st.selectbox(f"Update status for Order {row['Order ID']}",
                              ["Pending", "Processed", "Shipped", "Out for Delivery", "Delivered", "Cancelled"],
                              index=["Pending", "Processed", "Shipped", "Out for Delivery", "Delivered", "Cancelled"].index(row["Status"]))

    # Button to update status
    if st.button(f"✅ Update Order {row['Order ID']}"):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE orders SET status=%s WHERE order_id=%s", (new_status, row["Order ID"]))
        conn.commit()
        conn.close()
        st.success(f"✅ Order {row['Order ID']} updated to {new_status}")
        st.rerun()  # Refresh page to reflect update

# Logout Button
if st.button("🚪 Logout"):
    st.session_state["admin_logged_in"] = False
    st.session_state["admin_username"] = ""
    st.rerun()
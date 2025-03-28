import mysql.connector
import pandas as pd
import streamlit as st

# Connect to database
conn = mysql.connector.connect(
    host="your_host",
    user="your_user",
    password="your_password",
    database="your_database"
)
cursor = conn.cursor()

# Fetch orders
cursor.execute("SELECT order_id, customer_name, status FROM orders")
orders = cursor.fetchall()
df = pd.DataFrame(orders, columns=["Order ID", "Customer Name", "Status"])

# Display orders
st.write("### Orders")
st.dataframe(df)
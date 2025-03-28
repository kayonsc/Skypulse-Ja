import streamlit as st
import requests
import folium
from streamlit_folium import st_folium

# Function to fetch drone locations from the Flask API
def fetch_drone_locations():
    response = requests.get("http://localhost:5000/get_locations")  # Connects to Flask backend
    if response.status_code == 200:
        return response.json()
    return []

# Streamlit UI
st.set_page_config(page_title="Drone Tracking | SkyPulse Jamaica", layout="wide")

st.title("🚁 Real-Time Drone Tracking")
st.write("This map shows the real-time location of all active drones delivering packages.")

# Fetch drone locations
drone_locations = fetch_drone_locations()

# Initialize Folium Map centered on Jamaica
m = folium.Map(location=[18.1096, -77.2975], zoom_start=8)

# Add Google Satellite Tiles
folium.TileLayer(
    tiles="https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
    attr="Google",
    name="Google Satellite",
    overlay=False,
    control=True
).add_to(m)

# Add drone markers to the map
for drone in drone_locations:
    folium.Marker(
        location=[drone["latitude"], drone["longitude"]],
        popup=f"Drone ID: {drone['drone_id']}",
        icon=folium.Icon(color="blue", icon="cloud")
    ).add_to(m)

# Display the map in Streamlit
st_folium(m, width=1200, height=600)
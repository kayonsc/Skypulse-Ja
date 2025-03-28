import streamlit as st
from PIL import Image

# Set the page title and icon
st.set_page_config(page_title="SkyPulse Jamaica", page_icon="🚀", layout="wide")

# Header (Logo and Menu)
col1, col2, col3 = st.columns([1, 2, 1])  # Center column is twice as large
with col2:
    # Load and display the logo
    logo = Image.open("skyPulse.jpg")  # Ensure the file exists in your directory
    st.image(logo, width=500)

# Home Image (Centered)
st.markdown("<br>", unsafe_allow_html=True)  # Adds spacing

col1, col2, col3 = st.columns([1, 4, 1])  # Middle column is larger
with col2:
    home_image = Image.open("home_image.jpg")  # Ensure the file exists
    st.image(home_image, caption="SkyPulse in Action!", width=800)

# Footer
st.markdown("---")
st.caption("© 2025 SkyPulse Jamaica. All rights reserved.")
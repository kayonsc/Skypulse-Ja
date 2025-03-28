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

# Center-align all content using HTML & CSS
st.markdown(
    """
    <style>
        .centered {
            text-align: center;
        }
        .stImage img {
            display: block;
            margin-left: auto;
            margin-right: auto;
        }
        .container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Centered Description
st.markdown(
    """
        
    ### **Our Mission**
    At **SkyPulse Jamaica**, we are revolutionizing the way deliveries are made. As a pioneering **drone-powered delivery service**, 
    we specialize in providing fast, reliable, and eco-friendly solutions for transporting packages across Jamaica.
    
    ### **Why Choose Us?**
    ✅ **Speed & Efficiency** – Our drones bypass traffic and deliver in record time.  
    ✅ **Real-Time Tracking** – Monitor your package’s journey from takeoff to drop-off.  
    ✅ **Eco-Friendly Solutions** – A greener alternative to traditional delivery methods.  
    ✅ **Reliable & Secure** – Each delivery is carefully monitored and verified upon arrival.  
    ✅ **Custom Services** – Tailored solutions for businesses, including membership tiers and insured deliveries.  
    
    ### **The Future of Delivery in Jamaica**
    At SkyPulse Jamaica, we’re not just delivering packages—we’re shaping the **future of logistics**. 
    Our cutting-edge technology and commitment to customer satisfaction make us the go-to choice for modern, efficient delivery solutions.
    
    Join us as we **take delivery to new heights!** 🚀
    """,
    unsafe_allow_html=True,
)
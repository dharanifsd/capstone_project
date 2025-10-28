"""
Phase 4: User Interface - Streamlit Web Application
Beautiful UI for predicting oxygen levels and optimal people count
"""

import streamlit as st
import requests
import pandas as pd
from PIL import Image
import time

# Page configuration
st.set_page_config(
    page_title="Green Skills AI - Location Safety Predictor",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Constants
import os
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #555;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #2E8B57;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 0.5rem 1rem;
    }
    .prediction-box {
        background-color: #f0f8ff;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #2E8B57;
        margin: 1rem 0;
    }
    .health-status {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        font-weight: bold;
        text-align: center;
    }
    .status-excellent { background-color: #90EE90; color: #006400; }
    .status-good { background-color: #87CEEB; color: #006400; }
    .status-fair { background-color: #FFD700; color: #8B4513; }
    .status-poor { background-color: #FFA500; color: #8B0000; }
    .status-critical { background-color: #FF6347; color: #8B0000; }
    </style>
""", unsafe_allow_html=True)

def check_api_connection():
    """Check if API server is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=2)
        if response.status_code == 200:
            return True, response.json()
        return False, None
    except:
        return False, None

def get_locations():
    """Get list of available locations"""
    try:
        response = requests.get(f"{API_BASE_URL}/locations")
        if response.status_code == 200:
            data = response.json()
            return data.get('locations', [])
        return []
    except:
        return []

def get_location_defaults(location):
    """Get default parameters for a location"""
    try:
        response = requests.get(f"{API_BASE_URL}/locations/{location}")
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def make_prediction(location, params=None):
    """Make prediction request to API"""
    try:
        payload = {"location": location}
        if params:
            payload.update(params)
        
        response = requests.post(f"{API_BASE_URL}/predict", json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.text}")
            return None
    except Exception as e:
        st.error(f"Connection Error: {str(e)}")
        return None

def main():
    # Header
    st.markdown('<p class="main-header">🌿 Green Skills AI</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Tourist Location Safety Predictor</p>', unsafe_allow_html=True)
    
    # Check API connection
    api_connected, health_data = check_api_connection()
    
    if not api_connected:
        st.error("⚠️ API Server is not running!")
        st.info("Please start the API server by running: `python start_server.py`")
        st.code("python start_server.py", language="bash")
        return
    
    # Show API status
    with st.expander("🔍 API Status", expanded=False):
        st.success("✓ API Server Connected")
        if health_data:
            st.json(health_data)
    
    # Sidebar for inputs
    with st.sidebar:
        st.header("📍 Location & Parameters")
        st.markdown("---")
        
        # Get locations
        locations = get_locations()
        if not locations:
            st.error("No locations available")
            return
        
        # Location selector
        selected_location = st.selectbox(
            "Select Location",
            locations,
            index=0
        )
        
        st.markdown("---")
        st.subheader("🌡️ Environmental Parameters")
        st.markdown("*Adjust parameters or use defaults*")
        
        # Get defaults for selected location
        defaults = get_location_defaults(selected_location)
        default_values = defaults.get('default_features', {}) if defaults else {}
        
        # Parameter inputs with defaults
        with st.form("prediction_form"):
            temperature = st.number_input(
                "Temperature (°C)",
                min_value=-20.0,
                max_value=50.0,
                value=float(default_values.get('Temperature', 15.0)),
                step=0.1
            )
            
            humidity = st.number_input(
                "Humidity (%)",
                min_value=0.0,
                max_value=100.0,
                value=float(default_values.get('Humidity', 70.0)),
                step=0.1
            )
            
            wind_speed = st.number_input(
                "Wind Speed (m/s)",
                min_value=0.0,
                max_value=50.0,
                value=float(default_values.get('WindSpeed', 8.0)),
                step=0.1
            )
            
            co2 = st.number_input(
                "CO₂ (ppm)",
                min_value=300.0,
                max_value=600.0,
                value=float(default_values.get('CO2', 420.0)),
                step=1.0
            )
            
            pm25 = st.number_input(
                "PM2.5 (μg/m³)",
                min_value=0.0,
                max_value=100.0,
                value=float(default_values.get('PM2.5', 15.0)),
                step=0.1
            )
            
            # Submit button
            submitted = st.form_submit_button("🔮 Predict", use_container_width=True)
            
            if submitted:
                st.session_state.submitted = True
                st.session_state.params = {
                    "temperature": temperature,
                    "humidity": humidity,
                    "wind_speed": wind_speed,
                    "co2": co2,
                    "pm25": pm25
                }
                st.session_state.location = selected_location
        
        # Reset button
        if st.button("🔄 Use Defaults", use_container_width=True):
            st.session_state.submitted = False
            st.rerun()
    
    # Main content area
    if st.session_state.get('submitted', False):
        # Show loading
        with st.spinner('Analyzing environmental conditions and making predictions...'):
            result = make_prediction(st.session_state.location, st.session_state.params)
        
        if result:
            # Display results
            st.success(f"✓ Predictions generated for **{result['location'].title()}**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="prediction-box">', unsafe_allow_html=True)
                st.markdown("### 💨 Oxygen Level")
                st.markdown(f"# **{result['predicted_oxygen_level']:.4f}%**")
                st.markdown("---")
                st.markdown("**Normal Range:** 20.9% - 21.0%")
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Health status with color coding
                health_status = result['health_status']
                status_class = ""
                if "Excellent" in health_status:
                    status_class = "status-excellent"
                elif "Good" in health_status:
                    status_class = "status-good"
                elif "Fair" in health_status:
                    status_class = "status-fair"
                elif "Poor" in health_status:
                    status_class = "status-poor"
                elif "Critical" in health_status:
                    status_class = "status-critical"
                
                st.markdown(f'<div class="health-status {status_class}">🩺 {health_status}</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="prediction-box">', unsafe_allow_html=True)
                st.markdown("### 👥 Recommended Capacity")
                st.markdown(f"# **{result['predicted_number_of_people']}**")
                st.markdown("---")
                st.markdown("**Maximum number of people**")
                st.markdown("for optimal air quality")
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Info box
                st.info(f"📍 Location: **{result['location'].title()}**")
            
            # Expandable details
            with st.expander("📊 View Input Parameters", expanded=False):
                st.json(result['input_features'])
            
            # Display data visually
            st.markdown("---")
            st.subheader("📈 Environmental Overview")
            
            # Create a simple chart
            chart_data = pd.DataFrame({
                'Parameter': ['Temperature', 'Humidity', 'Wind Speed', 'CO₂', 'PM2.5'],
                'Value': [
                    result['input_features'].get('Temperature', 0),
                    result['input_features'].get('Humidity', 0),
                    result['input_features'].get('WindSpeed', 0),
                    result['input_features'].get('CO2', 0),
                    result['input_features'].get('PM2.5', 0)
                ]
            })
            
            col3, col4, col5 = st.columns(3)
            
            with col3:
                st.metric("Temperature", f"{result['input_features'].get('Temperature', 0):.1f} °C")
                st.metric("Wind Speed", f"{result['input_features'].get('WindSpeed', 0):.1f} m/s")
            
            with col4:
                st.metric("Humidity", f"{result['input_features'].get('Humidity', 0):.1f} %")
                st.metric("CO₂", f"{result['input_features'].get('CO2', 0):.0f} ppm")
            
            with col5:
                st.metric("PM2.5", f"{result['input_features'].get('PM2.5', 0):.1f} μg/m³")
                st.metric("NDVI", f"{result['input_features'].get('NDVI', 0):.2f}")
            
    else:
        # Welcome screen
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("""
            ### 👋 Welcome to Green Skills AI
            
            This application helps you predict:
            - **Oxygen Levels** based on environmental conditions
            - **Optimal People Capacity** for safe air quality
            
            #### 🚀 How to Use:
            1. Select a location from the sidebar
            2. Adjust environmental parameters (or use defaults)
            3. Click **Predict** to get results
            
            #### 🌍 Available Locations:
            - Ooty, Manali, Shimla, Munnar
            - Kodaikanal, Gulmarg, Nainital
            - Mussoorie, Chikmagalur, Ponmudi
            - Valparai, Wagamon
            
            **Start by selecting a location in the sidebar →**
            """)
        
        # Show default values for selected location if available
        if defaults:
            with st.expander(f"ℹ️ Default values for {selected_location.title()}", expanded=False):
                st.json(defaults)
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
        🌿 Green Skills AI - Promoting Sustainable Tourism<br>
        Phase 4: User Interface | Built with Streamlit & FastAPI
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()


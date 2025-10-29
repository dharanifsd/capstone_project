import streamlit as st
import joblib
import pandas as pd

# Load models
model_oxygen = joblib.load("oxygen_model.pkl")
model_people = joblib.load("people_model.pkl")

st.title("Oxygen Level and Population Predictor")

# Input fields
alt = st.number_input("Altitude (m)")
pressure = st.number_input("Pressure (hPa)")
temp = st.number_input("Temperature (°C)")
humidity = st.number_input("Humidity (%)")
wind = st.number_input("Wind Speed (m/s)")
co2 = st.number_input("CO₂ (ppm)")
pm = st.number_input("PM2.5 (µg/m³)")
ndvi = st.number_input("NDVI")
pop_density = st.number_input("Population Density")

if st.button("Predict"):
    X = pd.DataFrame([[alt, pressure, temp, humidity, wind, co2, pm, ndvi, pop_density]],
                     columns=["Altitude","Pressure","Temperature","Humidity","WindSpeed","CO2","PM2.5","NDVI","PopulationDensity"])
    
    o2_pred = model_oxygen.predict(X)[0]
    people_pred = model_people.predict(X)[0]

    st.success(f"Oxygen Level: {o2_pred:.2f}%")
    st.info(f"Estimated Number of People: {int(people_pred)}")

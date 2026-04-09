import os
import pandas as pd
import pickle
import streamlit as st
import logging

# 1. Setup Logging
logging.basicConfig(
    filename='housing_app.log', 
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

st.title("Housing Price Predictor")
st.write("This application predicts the housing price based on historical characteristics.")

# Find the absolute path to the directory this script is in
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Join that directory with your filename
model_path = os.path.join(BASE_DIR, 'linearregression.pkl')

# 2. Error Handling for Model Loading
try:
    with open("linearregression.pkl", "rb") as lr_pickle:
        lr_model = pickle.load(lr_pickle)
    logging.info("Linear Regression model loaded successfully.")
except FileNotFoundError:
    st.error("Error: 'linearregression.pkl' not found. Please upload the model file.")
    logging.error("Model file missing.")
    st.stop()
except Exception as e:
    st.error(f"Error loading model: {e}")
    logging.error(f"Load error: {e}")
    st.stop()

# Prepare the form
with st.form("user_inputs"):
    st.subheader("Housing Characteristics")
    
    lotArea = st.number_input("Lot Area:", min_value=10, step=10, max_value=9999)
    numberOfRooms = st.number_input("Number of Rooms:", min_value=0, step=1, max_value=20)
    hasYard = st.selectbox("Does it have a yard?", options=["Yes", "No"])
    hasPool = st.selectbox("Does it have a pool?", options=["Yes", "No"])
    floors = st.number_input("Floors:", min_value=0, step=1, max_value=100)
    cityCode = st.number_input("City Code:", min_value=0, step=1, max_value=9999)
    cityPartRange = st.number_input("City Part Range:", min_value=0, step=1, max_value=9999)
    numberOfPreviousOwners = st.number_input("Number of Previous Owners:", min_value=0, step=1, max_value=9999)
    yearMade = st.number_input("Year Made:", min_value=0, step=1, max_value=9999)
    isNewlyBuilt = st.selectbox("Is it newly built?", options=["Yes", "No"])
    hasStormProtector = st.selectbox("Does it have storm protector?", options=["Yes", "No"])
    basement = st.number_input("Basement:", min_value=0, step=1, max_value=99999)
    attic = st.number_input("Attic:", min_value=0, step=1, max_value=99999)
    garage = st.number_input("Garage:", min_value=0, step=1, max_value=99999)
    hasStorageRoom = st.selectbox("Does it have a storage room?", options=["Yes", "No"])
    hasGuestRoom = st.selectbox("Does it have a guest room?", options=["Yes", "No"])
    
    submitted = st.form_submit_button("Predict Housing Price")

if submitted:
    # 3. Error Handling for Data Processing and Prediction
    try:
        # Convert categoricals
        hasYard_val = 1 if hasYard == "Yes" else 0
        hasPool_val = 1 if hasPool == "Yes" else 0
        isNewlyBuilt_val = 1 if isNewlyBuilt == "Yes" else 0
        hasStormProtector_val = 1 if hasStormProtector == "Yes" else 0
        hasStorageRoom_val = 1 if hasStorageRoom == "Yes" else 0
        hasGuestRoom_val = 1 if hasGuestRoom == "Yes" else 0

        # Prepare input array
        lr_prediction_input = [[
            lotArea, numberOfRooms, hasYard_val, hasPool_val,
            floors, cityCode, cityPartRange, numberOfPreviousOwners,
            yearMade, isNewlyBuilt_val, hasStormProtector_val, basement,
            attic, garage, hasStorageRoom_val, hasGuestRoom_val
        ]]

        # Make prediction
        lr_new_prediction = lr_model.predict(lr_prediction_input)

        # Display result
        st.subheader("Prediction Result:")
        st.success(f"The predicted housing price is: ${lr_new_prediction[0]:,.2f}")
        
        logging.info(f"Prediction successful: {lr_new_prediction[0]}")

    except Exception as e:
        st.error("An error occurred.")
        logging.error(f"Error: {e}")

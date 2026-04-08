import pandas as pd
import pickle
import streamlit as st
import logging


# 1. Setup Logging
logging.basicConfig(
    filename='survival_app.log', 
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Set the page title and description
st.title("Survival Probability Predictor")
st.write("""
This application predicts survivability based from
         historical datasets.
""")


# 2. Error Handling for Model Loading
try:
    with open("randomforest.pkl", "rb") as rf_pickle:
        rf_model = pickle.load(rf_pickle)
    logging.info("Random Forest model loaded successfully.")
except FileNotFoundError:
    st.error("Model file 'randomforest.pkl' not found. Please ensure it is in the directory.")
    logging.error("Model file missing.")
    st.stop()
except Exception as e:
    st.error(f"Error loading model: {e}")
    logging.error(f"Unexpected error: {e}")
    st.stop()


# Prepare the form to collect user inputs
with st.form("user_inputs"):
    st.subheader("Passenger Characteristics")
    
    # Passenger Class
    pclass = st.selectbox("Passenger Class:", 
                               options=["1", "2", "3"])
    
    # Gender
    gender = st.selectbox("Gender:", options=["Male", "Female"])

    # Place Embarked
    placeEmbarked = st.selectbox("Port Embarked Code:", options=["C", "Q", "S"])

    # Relatives 
    relatives = st.selectbox("Number of Relatives:", options=["None", "Few", "Many"])

    # Fare Group
    fareGroup = st.selectbox("Fare Class:", options=["Low", "Medium", "High", "Premium"])

    # Age Group
    ageGroup = st.selectbox("Age Class:", options=["Young", "Adult", "Elderly"])

    # Submit button
    submitted = st.form_submit_button("Predict Survibability")


# Handle the dummy variables to pass to the model
if submitted:
    try:    
        pclass1 = 1 if pclass == "1" else 0
        pclass2 = 1 if pclass == "2" else 0
        pclass3 = 1 if pclass == "3" else 0
        
        gender1 = 1 if gender == "Female" else 0
        gender2 = 1 if gender == "Male" else 0

        placeEmbarkedC = 1 if placeEmbarked == "C" else 0
        placeEmbarkedQ = 1 if placeEmbarked == "Q" else 0
        placeEmbarkedS = 1 if placeEmbarked == "S" else 0

        relativesNone = 1 if relatives == "None" else 0
        relativesFew  = 1 if relatives == "Few" else 0
        relativesMany = 1 if relatives == "Many" else 0
        
        fareGroupLow  = 1 if fareGroup == "Low" else 0
        fareGroupMedium = 1 if fareGroup == "Medium" else 0
        fareGroupHigh = 1 if fareGroup == "High" else 0
        fareGroupPremium = 1 if fareGroup == "Premium" else 0

        ageGroupYoung = 1 if ageGroup == "Young" else 0
        ageGroupAdult = 1 if ageGroup == "Adult" else 0
        ageGroupElderly = 1 if ageGroup == "Elderly" else 0

        # Prepare the input for prediction. 
        rf_prediction_input = [[ 
            pclass1, pclass2, pclass3, gender1, gender2, 
            placeEmbarkedC, placeEmbarkedQ, placeEmbarkedS,
            relativesFew, relativesMany, relativesNone, 
            fareGroupHigh, fareGroupLow, fareGroupMedium, fareGroupPremium,
            ageGroupAdult, ageGroupElderly, ageGroupYoung
        ]]

        # Make prediction
        rf_new_prediction = rf_model.predict(rf_prediction_input)

        # Display result
        st.subheader("Prediction Result:")
        if rf_new_prediction[0] == 1:
            st.success(f"The passenger will likely survive.")   
        else:
            st.warning(f"The passenger will not survive.")   
    except Exception as e:
        st.error("An error occurred.")
        logging.error(f"Error: {e}")
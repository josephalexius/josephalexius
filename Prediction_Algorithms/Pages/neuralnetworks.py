import pandas as pd
import pickle
import streamlit as st
import logging

# 1. Setup Logging
logging.basicConfig(
    filename='nn_admission_app.log', 
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

st.title("UCLA Admission Predictor")
st.write("This application predicts the probability of admission to UCLA.")

# 2. Error Handling for Model and Scaler Loading
try:
    with open("neuralnetworks.pkl", "rb") as nn_pickle:
        nn_model = pickle.load(nn_pickle)
    with open("scaler.pkl", "rb") as s_pickle:
        scaler = pickle.load(s_pickle)
    logging.info("Model and Scaler loaded successfully.")
except FileNotFoundError as e:
    st.error(f"Missing file: {e.filename}. Please ensure both 'neuralnetworks.pkl' and 'scaler.pkl' exist.")
    logging.error(f"File missing: {e}")
    st.stop()
except Exception as e:
    st.error(f"Error loading assets: {e}")
    logging.error(f"Unexpected load error: {e}")
    st.stop()

# Prepare the form
with st.form("user_inputs"):
    st.subheader("Student Circumstances")
    
    greScore = st.number_input("GRE Score (0-340):", min_value=0, max_value=340, step=1)
    toeflScore = st.number_input("TOEFL Score (0-120):", min_value=0, max_value=120, step=1)
    universityRating = st.number_input("University Rating (1-5):", min_value=1, max_value=5, step=1)
    sopStrength = st.number_input("Statement of Purpose Strength (1-5):", min_value=0.0, max_value=5.0, step=0.1, format="%.2f")
    lorStrength = st.number_input("Letter of Recommendation Strength (1-5):", min_value=0.0, max_value=5.0, step=0.1, format="%.2f")
    cgpa = st.number_input("Undergraduate GPA:", min_value=0.0, max_value=10.0, step=0.1, format="%.2f")
    hasResearchExperience = st.selectbox("Does the student have research experience?", options=["Yes", "No"])
    
    submitted = st.form_submit_button("Predict Admission Chance")

if submitted:
    # 3. Error Handling for Logic and Prediction
    try:
        # BUG FIX: Comparing integer input to integers (not strings)
        universityRating1 = 1 if universityRating == 1 else 0
        universityRating2 = 1 if universityRating == 2 else 0
        universityRating3 = 1 if universityRating == 3 else 0
        universityRating4 = 1 if universityRating == 4 else 0
        universityRating5 = 1 if universityRating == 5 else 0

        # BUG FIX: Research variables should map from 'hasResearchExperience', not 'universityRating'
        hasResearchExperience1 = 1 if hasResearchExperience == "Yes" else 0
        hasResearchExperience0 = 1 if hasResearchExperience == "No" else 0

        # Prepare raw input
        nn_raw_input = [[
            greScore, toeflScore, sopStrength, lorStrength, cgpa,
            universityRating1, universityRating2, universityRating3,
            universityRating4, universityRating5, hasResearchExperience0,
            hasResearchExperience1
        ]]

        # Scale the data
        scaled_input = scaler.transform(nn_raw_input)

        # Make prediction
        prediction = nn_model.predict(scaled_input)

        # Display result
        st.subheader("Prediction Result:")
        if prediction[0] == 1:
            st.success("The student will likely be admitted.")
        else:
            st.warning("The student will likely not be admitted.")
        
        logging.info(f"Successful Prediction: {prediction[0]} for inputs: {nn_raw_input}")

    except Exception as e:
        st.error("An error occurred.")
        logging.error(f"Error: {e}")

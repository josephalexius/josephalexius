import os
import pandas as pd
import pickle
import streamlit as st
import logging

# configure to enable logging for error handling
logging.basicConfig(
    filename='nn_admission_app.log', 
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# set code to locate file path same as the current directory of the code
pages_dir = os.path.dirname(__file__)

# configure path to navigate one directory up from the code location
root_dir = os.path.abspath(os.path.join(pages_dir, '..'))

#concatenate the directory with the filename
model_file = os.path.join(root_dir, 'neuralnetworks.pkl')
scaler_file = os.path.join(root_dir, 'scaler.pkl')

st.title("UCLA Admission Predictor")
st.write("This application predicts the probability of admission to UCLA.")

# set up error handling to catch potential errors
try:
    with open(model_file, "rb") as nn_pickle:
        nn_model = pickle.load(nn_pickle)
    with open(scaler_file, "rb") as s_pickle:
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

# design the form
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
    # set up error handling upon submit to catch and log information
    try:
        
        universityRating1 = 1 if universityRating == 1 else 0
        universityRating2 = 1 if universityRating == 2 else 0
        universityRating3 = 1 if universityRating == 3 else 0
        universityRating4 = 1 if universityRating == 4 else 0
        universityRating5 = 1 if universityRating == 5 else 0

        
        hasResearchExperience1 = 1 if hasResearchExperience == "Yes" else 0
        hasResearchExperience0 = 1 if hasResearchExperience == "No" else 0

        # arrange attributes to match algorithm input requirements
        nn_raw_input = [[
            greScore, toeflScore, sopStrength, lorStrength, cgpa,
            universityRating1, universityRating2, universityRating3,
            universityRating4, universityRating5, hasResearchExperience0,
            hasResearchExperience1
        ]]

        # scale inputs to conform with the input requirement of the algorith
        scaled_input = scaler.transform(nn_raw_input)

        # predict based from inputs
        prediction = nn_model.predict(scaled_input)

        # display result
        st.subheader("Prediction Result:")
        if prediction[0] == 1:
            st.success("The student will likely be admitted.")
        else:
            st.warning("The student will likely not be admitted.")
        
        logging.info(f"Successful Prediction: {prediction[0]} for inputs: {nn_raw_input}")

    except Exception as e:
        st.error("An error occurred.")
        logging.error(f"Error: {e}")

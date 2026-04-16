import os
import pandas as pd
import pickle
import streamlit as st
import logging

# configure to enable logging for error handling
logging.basicConfig(
    filename='clustering_app.log', 
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

st.title("Mall Customer Segmentation")
st.write("This application groups customers into segments based on their attributes.")

# set code to locate file path same as the current directory of the code
pages_dir = os.path.dirname(__file__)

# configure path to navigate one directory up from the code location
root_dir = os.path.abspath(os.path.join(pages_dir, '..'))

#concatenate the directory with the filename
model_file = os.path.join(root_dir, 'clustering.pkl')

# set up error handling to catch potential errors
try:
    with open(model_file, "rb") as cs_pickle:
        cs_model = pickle.load(cs_pickle)
    logging.info("Clustering model loaded successfully.")
except FileNotFoundError:
    st.error("Error: 'clustering.pkl' not found. Please ensure the model file is in the app directory.")
    logging.error("Clustering model file missing.")
    st.stop()
except Exception as e:
    st.error(f"An unexpected error occurred while loading the model: {e}")
    logging.error(f"Load error: {e}")
    st.stop()

# design the form
with st.form("user_inputs"):
    st.subheader("Customer Attributes")

    annualIncome = st.number_input("Annual Income (in thousand dollars):", min_value=0, step=1,max_value=999)
    spendingScore = st.number_input("Spending Score (1-100):", min_value=0, step=1, max_value=100)
    age = st.number_input("Age:", min_value=0, step=1,max_value=120)
    
    submitted = st.form_submit_button("Predict Customer Group")

if submitted:
    # set up error handling upon submit to catch and log information
    try:
        # arrange attributes to match algorithm input requirements
        cs_prediction_input = [[annualIncome, spendingScore, age]]

        # predict based from inputs
        cluster_result = cs_model.predict(cs_prediction_input)
        cluster_id = int(cluster_result[0])

        # display result
        st.subheader("Prediction Result:")
        st.success(f"The customer belongs to **Group {cluster_id}**.")
        
        logging.info(f"Successful. Input: {cs_prediction_input} Cluster: {cluster_id}")

    except Exception as e:
        st.error("An error occurred during the process.")
        logging.error(f"Clustering error: {e}")

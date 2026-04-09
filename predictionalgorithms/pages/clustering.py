import os
import pandas as pd
import pickle
import streamlit as st
import logging

# 1. Setup Logging
logging.basicConfig(
    filename='clustering_app.log', 
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

st.title("Mall Customer Segmentation")
st.write("This application groups customers into segments based on their attributes.")

pages_dir = os.path.dirname(__file__)
root_dir = os.path.abspath(os.path.join(pages_dir, '..'))
model_file = os.path.join(root_dir, 'clustering.pkl')

# 2. Error Handling for Model Loading
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

# Prepare the form
with st.form("user_inputs"):
    st.subheader("Customer Attributes") # Fixed header from 'Housing' to 'Customer'

    annualIncome = st.number_input("Annual Income (in thousand dollars):", 
                                   min_value=0, 
                                   step=1,
                                   max_value=999)

    spendingScore = st.number_input("Spending Score (1-100):", 
                                    min_value=0, 
                                    step=1,
                                    max_value=100)

    age = st.number_input("Age:", 
                          min_value=0, 
                          step=1,
                          max_value=120)
    
    submitted = st.form_submit_button("Predict Customer Group")

if submitted:
    # 3. Error Handling for Clustering Prediction
    try:
        # Prepare input
        cs_prediction_input = [[annualIncome, spendingScore, age]]

        # Make prediction (cluster assignment)
        cluster_result = cs_model.predict(cs_prediction_input)
        cluster_id = int(cluster_result[0])

        # Display result
        st.subheader("Prediction Result:")
        # Simplified display logic - no need for multiple elifs if just showing the ID
        st.success(f"The customer belongs to **Group {cluster_id}**.")
        
        logging.info(f"Successful. Input: {cs_prediction_input} Cluster: {cluster_id}")

    except Exception as e:
        st.error("An error occurred during the process.")
        logging.error(f"Clustering error: {e}")

import os
import pandas as pd
import streamlit as st
import logging

#import the modules
from src.features.lr_build_features import lr_build_features
from src.models.lr_train_model import train_LRmodel
from src.models.lr_predict_model import evaluate_model
from src.visualization.lr_visualizations import (
    plot_correlation_heatmap, 
    plot_feature_importance, 
    print_mse_results
)

#configure logging
logging.basicConfig(
    filename='housing_app.log', 
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

st.title("Housing Price Predictor")
st.write("This application predicts housing prices based on historical characteristics.")

#get path of dataset
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, 'src', 'data', 'housing.csv')

@st.cache_data
def load_and_train():
    
    #read csv
    df_raw = pd.read_csv(csv_path)
    
    #perform feature engineering
    df_processed = lr_build_features(df_raw)
    
    X = df_processed.drop('price', axis=1) 
    y = df_processed['price']
    
    #train the model
    model, X_test, y_test = train_LRmodel(X, y)
    
    return model, X, X_test, y_test

# train and test split
model, X_cols, X_test, y_test = load_and_train()

#show UI
with st.form("user_inputs"):
    st.subheader("Housing Characteristics")
    col1, col2 = st.columns(2)
    
    with col1:
        lotArea = st.number_input("Lot Area:", min_value=10, step=10, value=1000)
        numberOfRooms = st.number_input("Number of Rooms:", min_value=1, step=1, value=3)
        hasYard = st.selectbox("Does it have a yard?", options=["Yes", "No"])
        hasPool = st.selectbox("Does it have a pool?", options=["Yes", "No"])
        floors = st.number_input("Floors:", min_value=1, step=1, value=1)
        cityCode = st.number_input("City Code:", min_value=0, step=1)
        cityPartRange = st.number_input("City Part Range:", min_value=1, max_value=10)
        numberOfPreviousOwners = st.number_input("Previous Owners:", min_value=0, step=1)

    with col2:
        yearMade = st.number_input("Year Made:", min_value=1900, max_value=2026, value=2020)
        isNewlyBuilt = st.selectbox("Is it newly built?", options=["Yes", "No"])
        hasStormProtector = st.selectbox("Has storm protector?", options=["Yes", "No"])
        basement = st.number_input("Basement Area:", min_value=0)
        attic = st.number_input("Attic Area:", min_value=0)
        garage = st.number_input("Garage Area:", min_value=0)
        hasStorageRoom = st.selectbox("Has storage room?", options=["Yes", "No"])
        hasGuestRoom = st.selectbox("Has guest room?", options=["Yes", "No"])
    
    submitted = st.form_submit_button("Predict Housing Price")

if submitted:
    try:
        #input columns
        input_data = pd.DataFrame([{
            'lotArea': lotArea, 'numberOfRooms': numberOfRooms, 'hasYard': hasYard,
            'hasPool': hasPool, 'floors': floors, 'cityCode': cityCode,
            'cityPartRange': cityPartRange, 'numberOfPreviousOwners': numberOfPreviousOwners,
            'yearMade': yearMade, 'isNewBuilt': isNewlyBuilt, 
            'hasStormProtector': hasStormProtector, 'basement': basement,
            'attic': attic, 'garage': garage, 'hasStorageRoom': hasStorageRoom,
            'hasGuestRoom': hasGuestRoom
        }])

        #perform feature engineering
        input_processed = lr_build_features(input_data)

        #run_predictions
        prediction = model.predict(input_processed)

        st.subheader("Prediction Result:")
        st.success(f"The predicted housing price is: ${prediction[0]:,.2f}")
        
        logging.info(f"Successful prediction: {prediction[0]}")

    except Exception as e:
        st.error(f"An error occurred during prediction: {e}")
        logging.error(f"Prediction error: {e}")

st.divider()
if st.checkbox("Show Model Analytics"):
    st.write("### Model Performance")
    #evaluate
    mse, r2 = evaluate_model(model, X_test, y_test)
    st.metric("Mean Squared Error", f"{mse:,.2f}")
    st.metric("R-Squared Score", f"{r2:.4f}")
    
    st.write("### Feature Importance")
    #show visualization
    plot_feature_importance(model, X_cols)
    st.image("feature_importance.png")

import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pickle
import os

# Function to train the model
def train_LRmodel(X, y):
    # Splitting the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)

    # Scale the data using MinMaxScaler
    scaler = MinMaxScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Train the Linear Regression model
    model = LinearRegression().fit(X_train_scaled, y_train)
    
    # Ensure models directory exists
    os.makedirs('models', exist_ok=True)

    # Save the trained model
    with open('models/linearregression.pkl', 'wb') as f:
        pickle.dump(model, f)
        
    # Save the scaler
    with open('models/scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)

    return model, X_test_scaled, y_test

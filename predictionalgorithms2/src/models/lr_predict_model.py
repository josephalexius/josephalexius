# Import regression metrics
from sklearn.metrics import mean_squared_error, r2_score

# Function to predict and evaluate
def evaluate_model(model, X_test_scaled, y_test):
    # Predict the housing prices on the testing set
    y_pred = model.predict(X_test_scaled)

    # Calculate the Mean Squared Error
    mse = mean_squared_error(y_test, y_pred)

    # Calculate the R-squared score
    r2 = r2_score(y_test, y_pred)

    return mse, r2

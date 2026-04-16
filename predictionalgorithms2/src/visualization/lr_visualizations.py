import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.metrics import mean_squared_error

def print_mse_results(y_test, y_pred):
    mse = mean_squared_error(y_test, y_pred)
    print(f"Mean Squared Error: {mse}")
    return mse

def plot_correlation_heatmap(data):
    plt.figure(figsize=(12, 8))
    sns.heatmap(data.corr(), annot=True, cmap='coolwarm')
    plt.title('Correlation Heatmap', fontsize=16)
    plt.show()

def plot_feature_importance(model, x):
    fig, ax = plt.subplots(figsize=(10, 6))
    importance = pd.Series(model.coef_, index=x.columns).abs().sort_values(ascending=False)
    
    sns.barplot(x=importance.values, y=importance.index, ax=ax)
    ax.set_xscale('log')
    plt.title("Feature Importance (Log Scale)")
    plt.tight_layout()
    fig.savefig("feature_importance.png")


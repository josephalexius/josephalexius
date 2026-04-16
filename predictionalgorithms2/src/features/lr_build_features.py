import pandas as pd

def lr_build_features(df):
    
    binary_cols = [
        'hasYard', 'hasPool', 'isNewBuilt', 'hasStormProtector', 
        'hasStorageRoom', 'hasGuestRoom'
    ]
    
    for col in binary_cols:
        if col in df.columns:
            df[col] = df[col].map({'Yes': 1, 'No': 0}).fillna(0)
            df[col] = df[col].astype(int)
            
    return df

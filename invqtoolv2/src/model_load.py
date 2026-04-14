import pickle
import logging
import os

# Points to 'src'
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# Moves up to root
BASE_DIR = os.path.dirname(CURRENT_DIR)

def load_from_pickle(filename='scf_xgb_model.pkl'):
    try:
        # Changed 'models' to 'model' to match your folder name
        model_path = os.path.join(BASE_DIR, 'model', filename)
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found at {model_path}")
            
        with open(model_path, 'rb') as f:
            obj = pickle.load(f)
            
        logging.info(f"Successfully loaded model from: {model_path}")
        return obj
    except Exception as e:
        logging.error(f"Failed to load pickle file: {e}")
        raise

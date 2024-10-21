import os
import pickle
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import numpy as np

# COMMAND ----------

def load_model(dbfs_model_path):
    """
    Load the saved Random Forest model from DBFS.
    """
    # Load the model from DBFS
    with open(dbfs_model_path, 'rb') as f:
        loaded_model = pickle.load(f)
    return loaded_model

# COMMAND ----------

def predict_single(loaded_model, input_data):
    
    input_data = np.array(input_data).reshape(1, -1)

    prediction = loaded_model.predict(input_data)

    target_names = load_iris().target_names

    predicted_class_name = target_names[prediction[0]]

    return prediction[0], predicted_class_name

# COMMAND ----------

# mdl = load_model('/dbfs/FileStore/rf_iris_model.pkl')
# predict_single(mdl, [1.1, 3, 4, 2.0])

# COMMAND ----------



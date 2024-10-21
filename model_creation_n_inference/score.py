import json
import numpy as np
import joblib
from azureml.core.model import Model

def init():
    global model
    # Load the model from the registered model in AML
    model_path = Model.get_model_path('iris_model')  
    model = joblib.load(model_path)

def run(raw_data):
    data = np.array(json.loads(raw_data)['data'])
    
    predictions = model.predict(data)
    
    return json.dumps({"predictions": predictions.tolist()})

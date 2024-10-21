# Databricks notebook source
# Import necessary libraries
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle
import os

# COMMAND ----------

iris = load_iris()
X = iris.data
y = iris.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

pth = os.path.join('/dbfs/FileStore', 'rf_iris_model.pkl')

# Save model 
with open(pth, 'wb') as f:
    pickle.dump(rf_model, f)

# COMMAND ----------



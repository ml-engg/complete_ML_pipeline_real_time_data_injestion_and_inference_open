# Databricks notebook source
from azureml.core import Workspace

# COMMAND ----------

# AML workspace configuration
subscription_id= '<>'
resource_group='<>'
workspace_name='<>'
               
# Connect to the Azure ML workspace
ws = Workspace(subscription_id=subscription_id,
               resource_group=resource_group,
               workspace_name=workspace_name)

print(f"Workspace name: {ws.name}, Resource group: {ws.resource_group}, Location: {ws.location}")

# COMMAND ----------

from azureml.core import Model

model_path = '/dbfs/FileStore/rf_iris_model.pkl'

model = Model.register(workspace=ws,
                       model_name='iris_model',  # Name of the model in AML
                       model_path=model_path,  
                       description='iris model for classificatop')

print(f"Model registered: {model.name}, Version: {model.version}")

# COMMAND ----------



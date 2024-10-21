# Databricks notebook source
import pandas as pd
import json 

from azure.eventhub import EventHubProducerClient, EventHubConsumerClient, EventData
from azure.eventhub.exceptions import EventHubError
import time

from azure.cosmos import CosmosClient, PartitionKey
import uuid

# COMMAND ----------

# cosmos db details 
COSMOS_DB_ENDPOINT = ""
COSMOS_DB_KEY = ""
DATABASE_NAME = ""
CONTAINER_NAME = ""

# event hub connection details 
connection_str = ''
eventhub_name = ""    
consumer_group = ""  

# COMMAND ----------

client = CosmosClient(COSMOS_DB_ENDPOINT, COSMOS_DB_KEY)
database = client.create_database_if_not_exists(DATABASE_NAME)
container = database.create_container_if_not_exists(
    id=CONTAINER_NAME,
    partition_key=PartitionKey(path="/id"),
    offer_throughput=400
)

def insert_item(user, data, container):
    users = {
        "id": str(uuid.uuid4()),
        "user_id": user,
        "data": data
    }
    container.create_item(body=users)
    print("Item inserted successfully!")

# COMMAND ----------

def on_event(partition_context, event):

    print(f"Received event from partition: {partition_context.partition_id}")
    #print(f"Data: {event.body_as_str()}")
    event_data_str = event.body_as_str()
    event_data_dict = json.loads(event_data_str)
    data = event_data_dict.get("data")
    user = event_data_dict.get("user_id")
    #print(data, user)
    insert_item(str(user), str(data), container)
    partition_context.update_checkpoint(event)


try:
    consumer = EventHubConsumerClient.from_connection_string(
        conn_str=connection_str, 
        consumer_group=consumer_group, 
        eventhub_name=eventhub_name
    )
    
    with consumer:
        print("Waiting for events...")
        consumer.receive(
            on_event=on_event,
            starting_position="-1"  
        )
         
except KeyboardInterrupt:
    print("Receive operation stopped.")
finally:
    consumer.close()


# COMMAND ----------



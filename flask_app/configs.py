import pandas as pd
import json 

from azure.eventhub import EventHubProducerClient, EventHubConsumerClient, EventData
from azure.eventhub.exceptions import EventHubError
import time

from azure.cosmos import CosmosClient, PartitionKey
import uuid
import ast

import urllib.request
import os
import ssl
import configs


#  Cosmos db details
COSMOS_DB_ENDPOINT = ""
COSMOS_DB_KEY = ""
DATABASE_NAME = ""
CONTAINER_NAME = ""

# event hub details
connection_str = ''
eventhub_name = ""    
consumer_group = ""  

client = CosmosClient(COSMOS_DB_ENDPOINT, COSMOS_DB_KEY)
database = client.create_database_if_not_exists(DATABASE_NAME)
container = database.create_container_if_not_exists(
    id=CONTAINER_NAME,
    partition_key=PartitionKey(path="/id"),
    offer_throughput=400
)

url = ''
api_key = ''


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
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

@app.route('/get_user_predictions', methods=['GET'])
def get_predictions():
    
    user = request.args.get('user_id')
    
    if not user:
        return jsonify({"error": "user_id parameter is required"}), 400
    #user = 'user_30'
    query = f"SELECT * FROM c WHERE c.user_id='{user}'"
    items = list(configs.container.query_items(query=query, enable_cross_partition_query=True))
    x = [item['data'] for item in items][0]
    list_value = ast.literal_eval(x)

    def allowSelfSignedHttps(allowed):
        # bypass the server certificate verification on client side
        if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
            ssl._create_default_https_context = ssl._create_unverified_context

    allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.

    data = {"data": [list_value]}

    body = str.encode(json.dumps(data))

    if not configs.api_key:
        raise Exception("A key should be provided to invoke the endpoint")

    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ configs.api_key)}

    req = urllib.request.Request(configs.url, body, headers)
    response = urllib.request.urlopen(req)
    result = response.read()
    print(result)

    return (result)

# run app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

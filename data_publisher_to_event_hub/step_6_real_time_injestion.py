from azure.eventhub import EventHubProducerClient, EventHubConsumerClient, EventData
from azure.eventhub.exceptions import EventHubError
import time

# event hub connection details 
connection_str = ''
eventhub_name = ""    
consumer_group = ""  

# publisher code
producer = EventHubProducerClient.from_connection_string(conn_str=connection_str, eventhub_name=eventhub_name)

def send_event():
    try:
        event_data_batch = producer.create_batch()
        event_data_batch.add(EventData('{"data":"[6.0, 3.0, 4.0, 1.0]", "user_id" : "user_651"}'))
        producer.send_batch(event_data_batch)
        print("Message sent successfully!")
    except EventHubError as eh_err:
        print(f"Error sending message: {eh_err}")
    finally:
        producer.close()

# call function to send event 
send_event()
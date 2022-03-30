import json 
from kafka import KafkaConsumer


consumer = KafkaConsumer(
    'messages',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest'
)
for message in consumer:
    print(json.loads(message.value))

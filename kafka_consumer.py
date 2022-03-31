import json 
from pprint import pprint
from datetime import datetime
from data_development import (
    insert_used_db, 
    check_value_file,
    check_presence_used
)
from kafka import KafkaConsumer


check_value_file()
consumer = KafkaConsumer(
    'message',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest'
)
for message in consumer:
    k = json.loads(message.value)
    if not check_presence_used(k.get("uuid")):
        received = datetime.utcnow()
        send = datetime.strptime(k.get('date_created'), '%Y-%m-%d %H:%M:%S.%f')
        delta = received - send
        delta_used = delta.microseconds/1000000 + delta.seconds + delta.days*60*60*24 
        value_required = {
            "uuid": k.get('uuid'),
            'date_send': k.get('date_created'),
            'date_received': str(received),
            'delta': delta_used
        }    
        insert_used_db(value_required)
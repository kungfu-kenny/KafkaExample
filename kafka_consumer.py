import json 
from pprint import pprint
from datetime import datetime
from data_development import (
    check_value_file,
    develop_file_check,
    develop_file_insert
)
from kafka import KafkaConsumer


check_value_file()

consumer = KafkaConsumer(
    'message',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest'
)
for message in consumer:
    message_sent = json.loads(message.value)
    message_sent_uuid = message_sent.get('uuid', False)
    message_sent_date = message_sent.get('date_created', 'unknown')
    if message_sent.get('uuid'):
        message_check = {message_sent_uuid:message_sent_date}
        if not develop_file_check(message_sent_uuid):
            
            received = datetime.utcnow()
            send = datetime.strptime(message_sent.get('date_created'), '%Y-%m-%d %H:%M:%S.%f')
            delta = received - send
            delta_used = delta.microseconds/1000000 + delta.seconds + delta.days*60*60*24 
            value_required = {
                "uuid": message_sent.get('uuid'),
                'date_send': message_sent.get('date_created'),
                'date_received': str(received),
                'delta': delta_used
            }    
            develop_file_insert(
                value_required, 
                True
            )
            develop_file_insert(
                {
                    message_sent_uuid:message_sent_date
                }, 
                False
            )
            print(message_check)
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
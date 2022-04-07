import json
from datetime import datetime
from data_development import (
    check_value_file,
    develop_file_check,
    develop_file_insert
)
from kafka import KafkaConsumer



topic = 'message_test'
check_value_file(topic)

consumer = KafkaConsumer(
    topic,
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest'
)
for message in consumer:
    proccessed = datetime.utcnow()
    message_sent = json.loads(message.value)
    # print(message_sent)
    # print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    message_sent_uuid = message_sent.get('uuid', False)
    message_sent_date = message_sent.get('date_created', 'unknown')
    if message_sent.get('uuid'):
        if not develop_file_check(topic, message_sent_uuid):
            
            received = datetime.utcnow()
            send = datetime.strptime(message_sent.get('date_created'), '%Y-%m-%d %H:%M:%S.%f')
            delta = received - send
            delta_operated = received - proccessed
            delta_send = proccessed - send
            value_required = {
                "uuid": message_sent.get('uuid'),
                "name_person": message_sent.get("name_person"),
                'date_send': message_sent.get('date_created'),
                'date_received': str(received),
                'delta_send': delta_send.microseconds/1000000 + delta_send.seconds + delta_send.days*60*60*24,
                'delta_received': delta.microseconds/1000000 + delta.seconds + delta.days*60*60*24,
                'delta_operated': delta_operated.microseconds/1000000 + delta_operated.seconds + delta_operated.days*60*60*24, 
            }    
            develop_file_insert(
                value_required, 
                True,
                topic
            )
            develop_file_insert(
                {
                    message_sent_uuid:message_sent_date
                }, 
                False,
                topic
            )
            print(message_sent.get("index", -1), message_sent_uuid, message_sent_date)
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    else:
        print('Strange Message:')
        print(message_sent)
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
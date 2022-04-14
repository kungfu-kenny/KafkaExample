import json
from datetime import datetime
from data_development import (
    develop_file_check_new,
    develop_file_insert
)
from kafka import KafkaConsumer
from config import topic_test, value_add_check


def calculate_consumer(received, message_sent, message_sent_uuid, message_sent_date):
    proccessed = datetime.utcnow()
    send = datetime.strptime(message_sent.get('date_created'), '%Y-%m-%d %H:%M:%S.%f')
    delta_full = proccessed - send
    delta_proccessed = proccessed - received
    delta_send = received - send
    value_required = {
        "uuid": message_sent.get('uuid'),
        "name_person": message_sent.get("name_person"),
        'date_send': message_sent.get('date_created'),
        'date_received': received.strftime('%Y-%m-%d %H:%M:%S.%f'),
        'date_processed': proccessed.strftime('%Y-%m-%d %H:%M:%S.%f'),
        'delta_send': delta_send.microseconds/1000000 + delta_send.seconds + delta_send.days*60*60*24,
        'delta_full': delta_full.microseconds/1000000 + delta_full.seconds + delta_full.days*60*60*24,
        'delta_proccessed': delta_proccessed.microseconds/1000000 + delta_proccessed.seconds + delta_proccessed.days*60*60*24, 
    }    
    develop_file_insert(
        value_required, 
        True,
        topic_test
    )
    if value_add_check:
        develop_file_insert(
            {
                message_sent_uuid:message_sent_date
            }, 
            False,
            topic_test
        )
    print(message_sent.get("index", -1), message_sent_uuid, message_sent_date)
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')        

consumer = KafkaConsumer(
    topic_test,
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest'
)
for message in consumer:
    received = datetime.utcnow()
    message_sent = json.loads(message.value)
    message_sent_uuid = message_sent.get('uuid', False)
    message_sent_date = message_sent.get('date_created', 'unknown')
    if value_add_check and message_sent.get('uuid'):
        if not develop_file_check_new(topic_test, message_sent_uuid):
            calculate_consumer(
                received,
                message_sent,
                message_sent_uuid,
                message_sent_date
            )
    elif value_add_check and not message_sent.get('uuid'):
        print('Strange Message:')
        print(message_sent)
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    else:
        calculate_consumer(
            received,
            message_sent,
            message_sent_uuid,
            message_sent_date
        )
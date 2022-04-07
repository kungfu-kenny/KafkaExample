import time
from json import dumps
from datetime import datetime
from kafka import KafkaProducer
from data_development import develop_random_data
from config import (
    topic_test, 
    topic_start, 
    topic_finish
)

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: dumps(x).encode('utf-8')
)

print('Started at: ', datetime.utcnow())
print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')

for j in range(topic_start, topic_finish):
    data = develop_random_data(j)
    print(f"Sent parameter with index:", j)
    producer.send(topic_test, value=data)
    time.sleep(0.01)

print('Finished at: ', datetime.utcnow())
print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
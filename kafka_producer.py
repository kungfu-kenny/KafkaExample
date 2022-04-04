from pprint import pprint
from time import sleep
from json import dumps
from pprint import pprint
from kafka import KafkaProducer
from data_development import develop_random_data


producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: dumps(x).encode('utf-8')
)

for j in range(1, 100000):
    data = develop_random_data(j)
    print(f"Sent parameter with index:", j)
    producer.send('message', value=data)
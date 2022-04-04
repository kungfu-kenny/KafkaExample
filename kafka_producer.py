from json import dumps
from datetime import datetime
from kafka import KafkaProducer
from data_development import develop_random_data


producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: dumps(x).encode('utf-8')
)

print('Started at: ', datetime.utcnow())
print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')

for j in range(1, 100000):
    data = develop_random_data(j)
    print(f"Sent parameter with index:", j)
    producer.send('message', value=data)

print('Finished at: ', datetime.utcnow())
print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
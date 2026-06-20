from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
      'parking.events.raw',
      bootstrap_servers='localhost:9092',
      auto_offset_reset='earliest',
      value_deserializer=lambda val: json.loads(val.decode('utf-8'))
)

print("Consuming events from 'parking.events.raw' Kafka topic..")
for message in consumer:
      event = message.value
      print("Event: ")
      print(event)
      print("-" * 40)


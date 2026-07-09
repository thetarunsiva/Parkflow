from kafka import KafkaProducer
from config import KAFKA_BROKER, KAFKA_TOPIC
import json

producer = KafkaProducer(
      bootstrap_servers=KAFKA_BROKER,
      value_serializer=lambda val: json.dumps(val).encode("utf-8")
)

def publish_event(events):
      try:
            for ev in events:
                  producer.send(KAFKA_TOPIC, value=ev)
            producer.flush()
            return True
      except Exception as e:
            print(f"Error publishing event! Error: {e}")
            return False
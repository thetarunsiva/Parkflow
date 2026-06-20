from kafka import KafkaProducer
import uuid
import json
from datetime import datetime, UTC

producer = KafkaProducer(
      bootstrap_servers='localhost:9092',
      value_serializer=lambda val: json.dumps(val).encode('utf-8')
)

event =  {
      "event_id": str(uuid.uuid4()),
      "event_type": "ENTRY",
      "timestamp": datetime.now(UTC).isoformat(),
      "slot_id": "T1",
      "lot_id": "LOT_1"
}

producer.send('parking.events.raw', event)
producer.flush()

print("Produced event: ")
print(event)
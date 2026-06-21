from kafka import KafkaConsumer
from database.db_connection import get_db_connection
import json

consumer = KafkaConsumer(
      'parking.events.raw',
      bootstrap_servers='kafka:29092',
      auto_offset_reset='earliest',
      group_id='parking-db-writer',
      value_deserializer=lambda val: json.loads(val.decode('utf-8'))
)

print("Listening for parking events..")

connection = get_db_connection()
cursor = connection.cursor()

for message in consumer:
      event = message.value
      try:
            cursor.execute(
                  """INSERT INTO slot_events (
                        event_id, slot_id, lot_id, event_type, event_time
                  ) VALUES (%s, %s, %s, %s, %s)
                  ON CONFLICT (event_id) DO NOTHING;""",
                  (
                        event['event_id'],
                        event['slot_id'],
                        event['lot_id'],
                        event['event_type'],
                        event['timestamp']
                  )

            )
            connection.commit()
            print(f"Inserted event {event['event_id']} into the db..")
      except Exception as error:
            print(f"Failed to store event in the db: {error}")
            connection.rollback()

cursor.close()
connection.close()
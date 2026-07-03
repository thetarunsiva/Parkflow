from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

import psycopg2

spark = (
      SparkSession.builder
      .appName("ParkflowStreaming")
      .getOrCreate()
)
spark.sparkContext.setLogLevel("WARN")

events = (
      spark.readStream
      .format("kafka")
      .option(
            "kafka.bootstrap.servers", 
            "kafka:29092"
      )
      .option(
            "subscribe",
            "parkflow.events.raw"
      )
      .load()
)

# Creating a new data frame using the value column from the events data frame, casting it to a string..
json_events = events.select(
      col("value").cast("string").alias("json_string"),
      col("offset"),
      col("partition"),
      col("timestamp")
)

event_schema = StructType([
      StructField("event_id", StringType()),
      StructField("event_type", StringType()),
      StructField("slot_id", StringType()),
      StructField("lot_id", StringType()),
      StructField("timestamp", StringType())
])

# This has a nested struct type, needs flatening..
parsed_events = json_events.select(
      from_json(col("json_string"), event_schema).alias("event"),
      col("offset"),
      col("partition"),
      col("timestamp").alias("kafka_timestamp")
)

parsed_events = parsed_events.select("event.*", "offset", "partition", "kafka_timestamp")
parsed_events = parsed_events.withColumn("event_timestamp", to_timestamp("timestamp"))
parsed_events.printSchema()

status_events = parsed_events.withColumn(
      "occupied",
      when(col("event_type") == "ENTRY", True)
      .otherwise(False)
)

def process_batch(batch_df, batch_id):
      print(f"Processing batch {batch_id}..\n")
      batch_df.show(truncate=False)
      db_connection = psycopg2.connect(
            host="postgres",
            database="parkflow",
            user="parkflow_user",
            password="parkflow_password",
            port="5432"
      )
      db_cursor = db_connection.cursor()
      current_batch_events = batch_df.collect()
      for current_event in current_batch_events:
            db_cursor.execute(
                  """
                  INSERT INTO slot_events (event_id, slot_id, lot_id, event_type, event_time) VALUES (
                        %s, %s, %s, %s, %s
                  );
                  """,
                  (
                        current_event.event_id,
                        current_event.slot_id,
                        current_event.lot_id,
                        current_event.event_type,
                        current_event.event_timestamp
                  )
            )

            db_cursor.execute(
                  """
                  INSERT INTO slot_status (slot_id, lot_id, occupied, last_event_id, last_event_time) VALUES (
                        %s, %s, %s, %s, %s
                  )
                  ON CONFLICT (slot_id, lot_id) DO UPDATE SET 
                        occupied = EXCLUDED.occupied,
                        last_event_id = EXCLUDED.last_event_id,
                        last_event_time = EXCLUDED.last_event_time;
                  """,
                  (
                        current_event.slot_id,
                        current_event.lot_id,
                        current_event.occupied,
                        current_event.event_id,
                        current_event.event_timestamp
                  )
            )

      db_connection.commit()
      print(f"Processed {len(current_batch_events)} events in the db..\n")
      db_cursor.close()
      db_connection.close()

query = (
      status_events.writeStream
      .foreachBatch(process_batch)
      .outputMode("append")
      .start()
)

print("Spark connected to Kafka..")
query.awaitTermination()
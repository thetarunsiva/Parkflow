from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

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

query = (
      status_events.writeStream
      .foreachBatch(process_batch)
      .outputMode("append")
      .start()
)


print("Spark connected to Kafka..")
query.awaitTermination()
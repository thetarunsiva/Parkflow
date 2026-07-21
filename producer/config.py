import os

LOTS = {
      "LOT_1": 10,
      "LOT_2": 25,
      "LOT_3": 20,
      "LOT_4": 10,
      "LOT_5": 20,
      "LOT_6": 40
}

KAFKA_BROKERS = os.getenv("KAFKA_BROKERS", "localhost:9092, localhost:9093, localhost:9094").split(",")
KAFKA_TOPIC = "parkflow.events.raw"

MIN_DELAY_SECONDS = 2
MAX_DELAY_SECONDS = 10

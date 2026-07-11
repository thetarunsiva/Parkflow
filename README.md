# ParkFlow

Distributed, fault-tolerant parking analytics data pipeline with a Natural-language query layer (Ask Parkflow) feature on top

```
Parking simulators → Kafka (3-Broker, KRaft) → Spark Structured Streaming → PostgreSQL → FastAPI → React
```

## Run it

```bash
git clone https://github.com/thetarunsiva/Parkflow.git
cd ParkFlow
```

```env
# Add .env File
KAFKA_CLUSTER_ID=<Generate: docker run --rm confluentinc/cp-kafka:7.6.1 kafka-storage random-uuid>
GEMINI_API_KEY=<Your-gemini-api-key>
```

```bash
docker compose up --build
```

Dashboard → `localhost`   ·   API docs → `localhost:8000/docs`

## What’s interesting here

- **Fault tolerance proved under failure**  
  With one broker down, Kafka elected a new leader and the pipeline kept running. With two brokers down, writes were rejected because `min.insync.replicas=2`, preventing unsafe under-replicated data.

- **Per-lot ordering with parallel processing**  
  Events are keyed by `lot_id`, so each lot’s events stay ordered within a partition while the topic is processed across three partitions and replicated across three brokers.

- **Safe natural-language analytics**  
  Gemini converts parking questions into PostgreSQL queries, but only single-statement `SELECT` queries are accepted and executed through a read-only database session.

- **History and current state are separated**  
  The `slot_events` relation stores the immutable event log, while `slot_status` and `lot_occupancy` store precomputed live state for fast dashboard reads.

**Stack:** Kafka (KRaft) · Spark Structured Streaming · PostgreSQL · FastAPI · React/TS · Docker Compose · Gemini API

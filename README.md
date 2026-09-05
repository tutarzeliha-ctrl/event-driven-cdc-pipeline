# Event-Driven Change Data Capture (CDC) Pipeline

A real-time, event-driven data pipeline built with Docker, PostgreSQL, Debezium, and Apache Kafka. This project captures row-level database changes (inserts, updates, deletes) instantly and streams them as events to Kafka topics.

## Architecture & Tech Stack

* **Database**: PostgreSQL 15 (configured with logical replication and `wal_level=logical`)
* **CDC Tool**: Debezium Connector 2.4.0.Final (`pgoutput` plugin)
* **Messaging / Streaming**: Apache Kafka 7.4.0 & Apache Zookeeper 7.4.0
* **Containerization**: Docker & Docker Compose

[ PostgreSQL (Source DB) ]
│ (WAL / Logical Replication)
▼
[ Debezium Connector ]
│ (JSON CDC Events)
▼
[ Apache Kafka Broker ] ──> [ Kafka Topics (postgres_cedb.public.customers) ]


## Prerequisites

* Docker and Docker Compose installed on your machine.
* PowerShell or any terminal supporting Docker CLI.

## Quick Start / Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/event-driven-cdc-pipeline.git](https://github.com/your-username/event-driven-cdc-pipeline.git)
   cd event-driven-cdc-pipeline
Start the infrastructure:

Bash
docker compose up -d
Create the test table and enable replication identity:

Bash
docker exec -it cdc_postgres psql -U postgres -d cedb -c "CREATE TABLE customers (id SERIAL PRIMARY KEY, first_name VARCHAR(50), last_name VARCHAR(50), email VARCHAR(100), created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);"
docker exec -it cdc_postgres psql -U postgres -d cedb -c "ALTER TABLE customers REPLICA IDENTITY FULL;"
Register the Debezium Connector:

Bash
curl.exe -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" http://localhost:8083/connectors/ -d "@connector-config.json"
Testing the Pipeline
Insert data into PostgreSQL:

Bash
docker exec -it cdc_postgres psql -U postgres -d cedb -c "INSERT INTO customers (first_name, last_name, email) VALUES ('Zeliha', 'Tutar', 'zeliha@example.com');"
Consume events from Kafka:

Bash
docker exec -it cdc_kafka kafka-console-consumer --bootstrap-server localhost:9092 --to
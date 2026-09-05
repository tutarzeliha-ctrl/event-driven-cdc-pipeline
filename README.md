# Real-Time Event-Driven CDC Dashboard

A real-time data streaming and Change Data Capture (CDC) monitoring pipeline built with PostgreSQL, Kafka, Debezium, and Streamlit.

## Architecture & Tech Stack
* **Database**: PostgreSQL (`cedb`) with logical replication (`wal_level=logical`)
* **Streaming / CDC**: Apache Kafka & Debezium Connect
* **Frontend / Visualization**: Streamlit (Real-time polling & live monitoring dashboard)

## Project Structure
* `app.py`: Real-time Streamlit dashboard application tracking live database changes.
* `producer.py`: Python script simulating real-time transactional inserts into the PostgreSQL database.
* `docker-compose.yml`: Container orchestration for Zookeeper, Kafka, PostgreSQL, and Debezium Connect.

## Getting Started

1. **Start Infrastructure**:
   ```bash
   
   docker-compose up -d
Initialize Database Table:

Bash
docker exec -it cdc_postgres psql -U postgres -d cedb -c "CREATE TABLE IF NOT EXISTS customers (id SERIAL PRIMARY KEY, first_name VARCHAR(50), last_name VARCHAR(50), email VARCHAR(100));"
Run the Streamlit Dashboard:

Bash
streamlit run app.py
Simulate Live Data Feed:

Bash
python producer.py

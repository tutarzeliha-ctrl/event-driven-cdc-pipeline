# 🚀 Event-Driven Real-Time CDC Pipeline (PostgreSQL, Debezium, Kafka, Python)

An end-to-end modern data pipeline project that captures all data modifications (`INSERT`, `UPDATE`, `DELETE`) in a relational database (`PostgreSQL`) in real-time and processes them as event streams over Apache Kafka using a **Change Data Capture (CDC)** architecture.

## 🏗️ Architecture & Tech Stack

* **Database**: PostgreSQL 15 (WAL - Write-Ahead Logging based CDC source)
* **CDC Engine**: Debezium 2.4.0 (Kafka Connect based PostgreSQL connector)
* **Message Broker**: Apache Kafka & Zookeeper
* **Containerization**: Docker Compose
* **Python Ecosystem**: 
  * `psycopg2-binary` & `Faker` (Simulated live data generation and DB operations)
  * `kafka-python` (Real-time Kafka topic consumer and event processor)

---

## ⚙️ System Workflow

1. **Producer (`producer.py`)**: Continuously generates random customer data (`INSERT`) into the `customers` table within PostgreSQL using the `Faker` library.
2. **Debezium Connector**: Monitors PostgreSQL transaction logs (`WAL`) to instantly detect any database modifications (`INSERT`, `UPDATE`, `DELETE`).
3. **Apache Kafka**: Securely and sequentially streams these captured event payloads to the designated Kafka topic (`postgres_cedb.public.customers`).
4. **Consumer (`consumer.py`)**: Subscribes to the Kafka topic to consume and log events in real-time.

---

## 🛠️ Setup & Execution Guide

Follow these steps to set up and run the project locally on your machine:

### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/event-driven-cdc-pipeline.git](https://github.com/your-username/event-driven-cdc-pipeline.git)
cd event-driven-cdc-pipeline
2. Spin Up the Docker Infrastructure
Bash
docker-compose up -d
3. Create a Python Virtual Environment & Install Dependencies
Bash
python -m venv .venv
# For Windows:
.venv\Scripts\Activate.ps1
# For Mac/Linux:
# source .venv/bin/activate

pip install -r requirements.txt
4. Create the PostgreSQL Table
Connect to the PostgreSQL container and create the customers table:

Bash
docker exec -it cdc_postgres psql -U postgres -d cedb
SQL
CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
(Type \q to exit)

5. Register the Debezium Connector
POST the configuration payload to register the connector and start monitoring the database:

Bash
curl.exe -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" http://localhost:8083/connectors/ --data "@connector-config.json"
6. Run the Pipeline
Start the Data Producer (producer.py):

Bash
python producer.py
Start the Kafka Consumer (consumer.py) in a Separate Terminal:

Bash
python consumer.py
🧪 CDC Test Scenarios
To test the UPDATE and DELETE event-driven capabilities of the pipeline, connect to the PostgreSQL database and run manual operations:

Bash
docker exec -it cdc_postgres psql -U postgres -d cedb
Update Test:

SQL
UPDATE customers SET first_name = 'Zeliha_Test' WHERE id = 2011;
Deletion Test:

SQL
DELETE FROM customers WHERE id = 3040;
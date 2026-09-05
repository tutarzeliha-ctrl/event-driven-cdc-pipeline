import json
from kafka import KafkaConsumer

TOPIC_NAME = "postgres_cedb.public.customers"
BOOTSTRAP_SERVERS = ["127.0.0.1:29092"]

def consume_events():
    consumer = KafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='cdc-consumer-group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8')) if x else None
    )

    print(f"🎧 Kafka Dinleniyor... Topik: {TOPIC_NAME}\n")

    try:
        for message in consumer:
            payload = message.value
            if payload and "payload" in payload:
                data = payload["payload"]
                op = data.get("op")
                after = data.get("after")
                
                op_type = {"c": "INSERT", "u": "UPDATE", "d": "DELETE"}.get(op, "UNKNOWN")
                print(f"📢 [EVENT - {op_type}] -> Veri: {after}")
    except KeyboardInterrupt:
        print("\n🛑 Consumer durduruldu.")
    finally:
        consumer.close()

if __name__ == "__main__":
    consume_events()
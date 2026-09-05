import time
import psycopg2
from faker import Faker

fake = Faker()


DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "cedb"
DB_USER = "postgres"
DB_PASSWORD = "postgres"

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

def generate_data(num_records=10, interval=2):
    print("🚀 Veri üreticisi başlatıldı. Çıkmak için CTRL+C tuşlarına basın.")
    conn = get_connection()
    conn.autocommit = True
    cursor = conn.cursor()

    try:
        while True:
            for _ in range(num_records):
                first_name = fake.first_name()
                last_name = fake.last_name()
                email = fake.email()

                query = "INSERT INTO customers (first_name, last_name, email) VALUES (%s, %s, %s);"
                cursor.execute(query, (first_name, last_name, email))
                print(f"➕ Eklendi: {first_name} {last_name} ({email})")
            
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n🛑 Veri üretimi durduruldu.")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    generate_data()
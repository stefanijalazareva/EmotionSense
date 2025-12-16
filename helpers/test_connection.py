"""Quick test to verify PostgreSQL connection"""
import psycopg2

try:
    conn = psycopg2.connect(
        host='localhost',
        port='5432',
        user='postgres',
        password='stefanija',
        database='emotionsense_dev'
    )
    print("✓ Connection successful!")
    print(f"Connected to: {conn.info.dbname}")
    conn.close()
except psycopg2.OperationalError as e:
    print(f"✗ Connection failed: {e}")
    print("\nPossible issues:")
    print("1. Wrong password - check pgAdmin password")
    print("2. Wrong port - PostgreSQL 17 might use 5433")
    print("3. Server not running")

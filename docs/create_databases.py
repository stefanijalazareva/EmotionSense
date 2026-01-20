"""
Script to create PostgreSQL databases for EmotionSense
"""
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_databases():
    config = {
        'host': 'localhost',
        'port': '5432',
        'user': 'postgres',
        'password': 'stefanija'  # Change this to your PostgreSQL password
    }
    
    databases = ['emotionsense_dev', 'emotionsense_prod']
    
    try:
        print("Connecting to PostgreSQL server...")
        conn = psycopg2.connect(
            host=config['host'],
            port=config['port'],
            user=config['user'],
            password=config['password'],
            database='postgres'
        )
        
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        for db_name in databases:
            try:
                print(f"\nCreating database: {db_name}")
                cursor.execute(sql.SQL("CREATE DATABASE {}").format(
                    sql.Identifier(db_name)
                ))
                print(f"Database '{db_name}' created successfully")
            except psycopg2.errors.DuplicateDatabase:
                print(f"Database '{db_name}' already exists")
            except Exception as e:
                print(f"Error creating '{db_name}': {e}")
        
        print("EmotionSense Databases:")
        cursor.execute("""
            SELECT datname FROM pg_database 
            WHERE datname LIKE 'emotionsense%' 
            ORDER BY datname
        """)
        for row in cursor.fetchall():
            print(f"  • {row[0]}")
        
        cursor.close()
        conn.close()
        print("\nDatabase setup completed successfully!")
        return True
        
    except psycopg2.OperationalError as e:
        print(f"\nConnection Error: {e}")
        return False
    except Exception as e:
        print(f"\nUnexpected Error: {e}")
        return False

if __name__ == "__main__":
    print("EmotionSense Database Setup")
    create_databases()

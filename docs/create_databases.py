"""
Script to create PostgreSQL databases for EmotionSense
Run this after PostgreSQL is installed and configured
"""
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_databases():
    # Database configuration
    config = {
        'host': 'localhost',
        'port': '5432',
        'user': 'postgres',
        'password': 'stefanija'  # Change this to your PostgreSQL password
    }
    
    databases = ['emotionsense_dev', 'emotionsense_prod']
    
    try:
        # Connect to PostgreSQL server
        print("Connecting to PostgreSQL server...")
        conn = psycopg2.connect(
            host=config['host'],
            port=config['port'],
            user=config['user'],
            password=config['password'],
            database='postgres'  # Connect to default database
        )
        
        # Set isolation level for CREATE DATABASE command
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Create databases
        for db_name in databases:
            try:
                print(f"\nCreating database: {db_name}")
                cursor.execute(sql.SQL("CREATE DATABASE {}").format(
                    sql.Identifier(db_name)
                ))
                print(f"✓ Database '{db_name}' created successfully")
            except psycopg2.errors.DuplicateDatabase:
                print(f"⚠ Database '{db_name}' already exists")
            except Exception as e:
                print(f"✗ Error creating '{db_name}': {e}")
        
        # List all EmotionSense databases
        print("\n" + "="*50)
        print("EmotionSense Databases:")
        print("="*50)
        cursor.execute("""
            SELECT datname FROM pg_database 
            WHERE datname LIKE 'emotionsense%' 
            ORDER BY datname
        """)
        for row in cursor.fetchall():
            print(f"  • {row[0]}")
        
        cursor.close()
        conn.close()
        print("\n✓ Database setup completed successfully!")
        return True
        
    except psycopg2.OperationalError as e:
        print(f"\n✗ Connection Error: {e}")
        print("\nTroubleshooting:")
        print("1. Ensure PostgreSQL is installed and running")
        print("2. Check your password in this script")
        print("3. Verify PostgreSQL is listening on port 5432")
        print("4. Check PostgreSQL authentication settings (pg_hba.conf)")
        return False
    except Exception as e:
        print(f"\n✗ Unexpected Error: {e}")
        return False

if __name__ == "__main__":
    print("="*50)
    print("EmotionSense Database Setup")
    print("="*50)
    create_databases()

#!/usr/bin/env python3
"""
Quick PostgreSQL test
"""
def test_postgres():
    try:
        import psycopg2
        conn = psycopg2.connect(
            host="localhost",
            port=5432, 
            database="mlflow",
            user="postgres", 
            password="postgres"
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';")
        count = cursor.fetchone()[0]
        print(f"✅ PostgreSQL: Connected! Found {count} tables")
        
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' LIMIT 5;")
        tables = cursor.fetchall()
        print("📋 Tables:")
        for table in tables:
            print(f"  - {table[0]}")
            
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ PostgreSQL Error: {e}")
        return False

if __name__ == "__main__":
    test_postgres()
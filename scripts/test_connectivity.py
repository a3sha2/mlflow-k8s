#!/usr/bin/env python3
"""
Simple MLflow connectivity test
"""
import requests
import json

def test_mlflow_connection():
    """Test MLflow server connectivity"""
    tracking_uri = "http://localhost:30500"
    
    try:
        # Test health endpoint
        print(f"🔗 Testing connection to {tracking_uri}")
        response = requests.get(f"{tracking_uri}/health")
        
        if response.status_code == 200:
            print("✅ MLflow server is healthy!")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
        
        # Test experiments endpoint
        response = requests.get(f"{tracking_uri}/api/2.0/mlflow/experiments/list")
        
        if response.status_code == 200:
            data = response.json()
            experiments = data.get('experiments', [])
            print(f"📊 Found {len(experiments)} experiments:")
            for exp in experiments[:3]:  # Show first 3
                print(f"  - {exp['name']} (ID: {exp['experiment_id']})")
            return True
        else:
            print(f"❌ Experiments API failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def test_postgres_connection():
    """Test PostgreSQL connectivity"""
    try:
        import psycopg2
        
        print("🐘 Testing PostgreSQL connection...")
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database="mlflow",
            user="postgres",
            password="postgres"
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
        tables = cursor.fetchall()
        
        print(f"✅ PostgreSQL connected! Found {len(tables)} tables:")
        for table in tables[:5]:  # Show first 5 tables
            print(f"  - {table[0]}")
            
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ PostgreSQL connection failed: {e}")
        print("💡 Try: kubectl port-forward -n mlflow svc/postgres-service 5432:5432")
        return False

if __name__ == "__main__":
    print("🚀 MLflow + PostgreSQL Connectivity Test")
    print("=" * 40)
    
    mlflow_ok = test_mlflow_connection()
    print()
    postgres_ok = test_postgres_connection()
    
    print("\n📋 Summary:")
    print(f"  MLflow Server: {'✅' if mlflow_ok else '❌'}")
    print(f"  PostgreSQL: {'✅' if postgres_ok else '❌'}")
    
    if mlflow_ok and postgres_ok:
        print("\n🎉 All systems operational!")
        print("🌐 Access MLflow UI: http://localhost:30500")
        print("🔧 Access PgAdmin: http://localhost:30800")
    else:
        print("\n🔧 Troubleshooting:")
        print("  - Check if services are running: kubectl get pods -n mlflow")
        print("  - Check service endpoints: kubectl get svc -n mlflow")
        print("  - Port forward if needed: kubectl port-forward -n mlflow svc/mlflow-service 5000:5000")
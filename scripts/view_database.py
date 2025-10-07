#!/usr/bin/env python3
"""
PostgreSQL MLflow Database Viewer
Direct access to MLflow's PostgreSQL backend
"""
import sys

def view_mlflow_database():
    """View MLflow database tables and data"""
    try:
        import psycopg2
        from datetime import datetime
        
        print("🐘 Connecting to MLflow PostgreSQL Database")
        print("=" * 45)
        
        # Connect to database
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database="mlflow",
            user="postgres",
            password="postgres"
        )
        cursor = conn.cursor()
        
        print("✅ Connected to PostgreSQL!")
        
        # 1. Show database schema
        print("\n📋 Database Tables:")
        cursor.execute("""
            SELECT table_name, table_type 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        
        for table_name, table_type in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            count = cursor.fetchone()[0]
            print(f"  📁 {table_name} ({count} rows)")
        
        # 2. Show experiments
        print("\n🧪 Experiments:")
        cursor.execute("""
            SELECT experiment_id, name, lifecycle_stage, creation_time
            FROM experiments 
            ORDER BY creation_time DESC;
        """)
        experiments = cursor.fetchall()
        
        for exp_id, name, stage, created in experiments:
            created_dt = datetime.fromtimestamp(created/1000) if created else "Unknown"
            print(f"  🔬 {name} (ID: {exp_id}) - {stage} - Created: {created_dt}")
        
        # 3. Show recent runs
        print("\n🏃 Recent Runs:")
        cursor.execute("""
            SELECT r.run_uuid, r.experiment_id, r.status, r.start_time, r.end_time,
                   e.name as experiment_name
            FROM runs r
            JOIN experiments e ON r.experiment_id = e.experiment_id
            ORDER BY r.start_time DESC
            LIMIT 10;
        """)
        runs = cursor.fetchall()
        
        for run_id, exp_id, status, start, end, exp_name in runs:
            start_dt = datetime.fromtimestamp(start/1000) if start else "Unknown"
            duration = f"{(end-start)/1000:.1f}s" if end and start else "Running"
            print(f"  🏃 {run_id[:8]}... - {exp_name} - {status} - {start_dt} ({duration})")
        
        # 4. Show parameters for latest run
        if runs:
            latest_run_id = runs[0][0]
            print(f"\n📊 Parameters for latest run ({latest_run_id[:8]}...):")
            cursor.execute("""
                SELECT key, value
                FROM params
                WHERE run_uuid = %s
                ORDER BY key;
            """, (latest_run_id,))
            params = cursor.fetchall()
            
            for key, value in params:
                print(f"  🔧 {key}: {value}")
        
        # 5. Show metrics for latest run
        if runs:
            print(f"\n📈 Metrics for latest run ({latest_run_id[:8]}...):")
            cursor.execute("""
                SELECT key, value, step
                FROM metrics
                WHERE run_uuid = %s
                ORDER BY key, step;
            """, (latest_run_id,))
            metrics = cursor.fetchall()
            
            current_key = None
            for key, value, step in metrics:
                if key != current_key:
                    print(f"  📊 {key}:")
                    current_key = key
                print(f"    Step {step}: {value:.4f}")
        
        # 6. Show database statistics
        print("\n📊 Database Statistics:")
        cursor.execute("SELECT COUNT(*) FROM experiments;")
        exp_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM runs;")
        run_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM params;")
        param_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM metrics;")
        metric_count = cursor.fetchone()[0]
        
        print(f"  🧪 Experiments: {exp_count}")
        print(f"  🏃 Runs: {run_count}")
        print(f"  🔧 Parameters: {param_count}")
        print(f"  📊 Metrics: {metric_count}")
        
        cursor.close()
        conn.close()
        print("\n✅ Database analysis complete!")
        
    except ImportError:
        print("❌ psycopg2 not installed. Install with: pip install psycopg2-binary")
        return
    except Exception as e:
        print(f"❌ Database error: {e}")
        print("\n🔧 Troubleshooting:")
        print("  1. Ensure PostgreSQL port forwarding is active:")
        print("     kubectl port-forward -n mlflow svc/postgres-service 5432:5432")
        print("  2. Check if PostgreSQL pod is running:")
        print("     kubectl get pods -n mlflow")
        return

def main():
    view_mlflow_database()

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
MLflow REST API Client - Works without MLflow Python library
"""
import requests
import json
import time
import random

class MLflowRESTClient:
    def __init__(self, tracking_uri="http://localhost:30500"):
        self.tracking_uri = tracking_uri.rstrip('/')
        self.api_base = f"{self.tracking_uri}/api/2.0/mlflow"
        
    def test_connection(self):
        """Test connection to MLflow server"""
        try:
            response = requests.get(f"{self.tracking_uri}/health")
            if response.status_code == 200:
                print(f"✅ Connected to MLflow: {self.tracking_uri}")
                return True
            else:
                print(f"❌ Connection failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Connection error: {e}")
            return False
    
    def create_experiment(self, name):
        """Create a new experiment"""
        data = {"name": name}
        response = requests.post(f"{self.api_base}/experiments/create", json=data)
        
        if response.status_code == 200:
            result = response.json()
            exp_id = result.get('experiment_id')
            print(f"📊 Created experiment: {name} (ID: {exp_id})")
            return exp_id
        elif response.status_code == 400 and "already exists" in response.text:
            # Get existing experiment
            exp_id = self.get_experiment_by_name(name)
            print(f"📊 Using existing experiment: {name} (ID: {exp_id})")
            return exp_id
        else:
            print(f"❌ Failed to create experiment: {response.text}")
            return None
    
    def get_experiment_by_name(self, name):
        """Get experiment ID by name"""
        response = requests.get(f"{self.api_base}/experiments/get-by-name", params={"experiment_name": name})
        if response.status_code == 200:
            return response.json()["experiment"]["experiment_id"]
        return None
    
    def list_experiments(self):
        """List all experiments"""
        response = requests.get(f"{self.api_base}/experiments/search", params={"max_results": 100})
        if response.status_code == 200:
            experiments = response.json().get("experiments", [])
            print(f"\n📋 Experiments ({len(experiments)}):")
            for exp in experiments:
                print(f"  - {exp['name']} (ID: {exp['experiment_id']})")
            return experiments
        else:
            print(f"❌ Failed to list experiments: {response.text}")
            return []
    
    def create_run(self, experiment_id):
        """Create a new run"""
        data = {
            "experiment_id": experiment_id,
            "start_time": int(time.time() * 1000)
        }
        response = requests.post(f"{self.api_base}/runs/create", json=data)
        
        if response.status_code == 200:
            run_id = response.json()["run"]["info"]["run_id"]
            print(f"🏃 Created run: {run_id}")
            return run_id
        else:
            print(f"❌ Failed to create run: {response.text}")
            return None
    
    def log_param(self, run_id, key, value):
        """Log a parameter"""
        data = {
            "run_id": run_id,
            "key": key,
            "value": str(value)
        }
        response = requests.post(f"{self.api_base}/runs/log-parameter", json=data)
        return response.status_code == 200
    
    def log_metric(self, run_id, key, value, step=0):
        """Log a metric"""
        data = {
            "run_id": run_id,
            "key": key,
            "value": float(value),
            "timestamp": int(time.time() * 1000),
            "step": step
        }
        response = requests.post(f"{self.api_base}/runs/log-metric", json=data)
        return response.status_code == 200
    
    def finish_run(self, run_id):
        """Finish a run"""
        data = {
            "run_id": run_id,
            "status": "FINISHED",
            "end_time": int(time.time() * 1000)
        }
        response = requests.post(f"{self.api_base}/runs/update", json=data)
        return response.status_code == 200
    
    def demo_ml_tracking(self):
        """Run a complete ML tracking demo"""
        print("🚀 MLflow Demo - REST API Approach")
        print("=" * 40)
        
        # Test connection
        if not self.test_connection():
            return
        
        # Create experiment
        exp_id = self.create_experiment("demo-ml-project-rest")
        if not exp_id:
            return
        
        # Simulate ML training runs
        algorithms = ["RandomForest", "XGBoost", "SVM", "LogisticRegression"]
        
        for i, algorithm in enumerate(algorithms):
            print(f"\n🔬 Training {algorithm}...")
            
            # Create run
            run_id = self.create_run(exp_id)
            if not run_id:
                continue
            
            # Simulate parameters
            params = {
                "algorithm": algorithm,
                "n_estimators": random.randint(50, 200),
                "max_depth": random.randint(3, 10),
                "learning_rate": round(random.uniform(0.01, 0.3), 3)
            }
            
            # Log parameters
            for key, value in params.items():
                self.log_param(run_id, key, value)
            
            # Simulate training metrics
            epochs = 10
            for epoch in range(epochs):
                accuracy = 0.7 + (epoch * 0.02) + random.uniform(-0.05, 0.05)
                loss = 1.0 - (epoch * 0.08) + random.uniform(-0.1, 0.1)
                
                self.log_metric(run_id, "accuracy", accuracy, epoch)
                self.log_metric(run_id, "loss", max(loss, 0.1), epoch)
            
            # Final metrics
            final_accuracy = 0.85 + random.uniform(-0.1, 0.1)
            self.log_metric(run_id, "final_accuracy", final_accuracy)
            
            # Finish run
            self.finish_run(run_id)
            print(f"  ✅ Completed {algorithm} - Final Accuracy: {final_accuracy:.3f}")
        
        # List all experiments
        self.list_experiments()
        
        print(f"\n🌐 View results at: {self.tracking_uri}")
        print("📊 Navigate to your experiment to see:")
        print("  - Parameter comparison across algorithms")
        print("  - Metric progression over epochs")
        print("  - Model performance comparison")

def main():
    # Initialize client
    client = MLflowRESTClient()
    
    # Run demo
    client.demo_ml_tracking()

if __name__ == "__main__":
    main()
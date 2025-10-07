#!/usr/bin/env python3
"""
MLflow Client Examples - Access from different environments
"""

import mlflow
import mlflow.sklearn
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

class MLflowClient:
    def __init__(self, tracking_uri="http://localhost:30500"):
        """
        Initialize MLflow client with tracking URI
        
        Options:
        - Local: http://localhost:30500 (NodePort)
        - Port Forward: http://localhost:5000 
        - Inside Cluster: http://mlflow-service.mlflow.svc.cluster.local:5000
        """
        self.tracking_uri = tracking_uri
        mlflow.set_tracking_uri(tracking_uri)
        print(f"🔗 Connected to MLflow: {tracking_uri}")
    
    def create_experiment_demo(self):
        """Create a demo experiment with sample model"""
        experiment_name = "demo-ml-project"
        
        try:
            # Create experiment
            experiment_id = mlflow.create_experiment(experiment_name)
            print(f"📊 Created experiment: {experiment_name} (ID: {experiment_id})")
        except mlflow.exceptions.MlflowException:
            print(f"📊 Using existing experiment: {experiment_name}")
        
        mlflow.set_experiment(experiment_name)
        
        # Generate sample data
        X, y = make_classification(n_samples=1000, n_features=10, random_state=42)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train model with MLflow tracking
        with mlflow.start_run(run_name="random_forest_demo"):
            # Parameters
            n_estimators = 100
            max_depth = 10
            
            # Log parameters
            mlflow.log_param("n_estimators", n_estimators)
            mlflow.log_param("max_depth", max_depth)
            mlflow.log_param("algorithm", "RandomForest")
            
            # Train model
            model = RandomForestClassifier(
                n_estimators=n_estimators,
                max_depth=max_depth,
                random_state=42
            )
            model.fit(X_train, y_train)
            
            # Evaluate
            y_pred = model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            
            # Log metrics
            mlflow.log_metric("accuracy", accuracy)
            mlflow.log_metric("test_samples", len(X_test))
            
            # Log model
            mlflow.sklearn.log_model(
                model, 
                "model",
                registered_model_name="demo-classifier"
            )
            
            print(f"✅ Model logged with accuracy: {accuracy:.4f}")
            return mlflow.active_run().info.run_id
    
    def list_experiments(self):
        """List all experiments"""
        experiments = mlflow.search_experiments()
        print("\n📋 Experiments:")
        for exp in experiments:
            print(f"  - {exp.name} (ID: {exp.experiment_id})")
    
    def list_models(self):
        """List registered models"""
        from mlflow.tracking import MlflowClient
        client = MlflowClient()
        
        models = client.search_registered_models()
        print("\n🤖 Registered Models:")
        for model in models:
            print(f"  - {model.name}")
            for version in model.latest_versions:
                print(f"    Version {version.version}: {version.current_stage}")

def main():
    print("🚀 MLflow Client Demo")
    print("====================")
    
    # Initialize client
    client = MLflowClient()
    
    # Run demo
    run_id = client.create_experiment_demo()
    print(f"🏃 Run ID: {run_id}")
    
    # List experiments and models
    client.list_experiments()
    client.list_models()
    
    print(f"\n🌐 View in UI: {client.tracking_uri}")

if __name__ == "__main__":
    main()
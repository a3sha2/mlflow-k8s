#!/bin/bash

echo "🚀 Deploying MLflow Registry to Kubernetes..."

# Create namespace
echo "📦 Creating MLflow namespace..."
kubectl apply -f manifests/01-namespace.yaml

# Wait for namespace
kubectl wait --for=condition=Ready namespace mlflow --timeout=60s

# Deploy PostgreSQL
echo "🐘 Deploying PostgreSQL database..."
kubectl apply -f manifests/02-postgres.yaml

# Wait for PostgreSQL to be ready
echo "⏳ Waiting for PostgreSQL to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/postgres -n mlflow

# Deploy MLflow Server
echo "🔬 Deploying MLflow Server..."
kubectl apply -f manifests/03-mlflow-server.yaml

# Wait for MLflow to be ready
echo "⏳ Waiting for MLflow Server to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/mlflow-server -n mlflow

echo "✅ MLflow Registry deployed successfully!"
echo ""
echo "🌐 Access MLflow UI:"
echo "   Local: http://localhost:30500"
echo "   Cluster: http://<node-ip>:30500"
echo ""
echo "📋 Useful commands:"
echo "   kubectl get pods -n mlflow"
echo "   kubectl logs -f deployment/mlflow-server -n mlflow"
echo "   kubectl port-forward -n mlflow svc/mlflow-service 5000:5000"
echo ""
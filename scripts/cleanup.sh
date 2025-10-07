#!/bin/bash

echo "🧹 Cleaning up MLflow Registry from Kubernetes..."

# Delete MLflow components
kubectl delete -f manifests/03-mlflow-server.yaml
kubectl delete -f manifests/02-postgres.yaml
kubectl delete -f manifests/01-namespace.yaml

echo "✅ MLflow Registry cleanup completed!"
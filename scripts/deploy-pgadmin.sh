#!/bin/bash

echo "🔧 Deploying PgAdmin for PostgreSQL Management"
echo "=============================================="

# Deploy PgAdmin
kubectl apply -f manifests/04-pgadmin.yaml

# Wait for deployment
echo "⏳ Waiting for PgAdmin to be ready..."
kubectl wait --for=condition=available --timeout=180s deployment/pgadmin -n mlflow

echo "✅ PgAdmin deployed successfully!"
echo ""
echo "🌐 Access PgAdmin:"
echo "   URL: http://localhost:30800"
echo "   Email: admin@mlflow.local"
echo "   Password: admin123"
echo ""
echo "🔗 PostgreSQL Connection in PgAdmin:"
echo "   Host: postgres-service"
echo "   Port: 5432"
echo "   Database: mlflow"
echo "   Username: postgres"
echo "   Password: postgres"
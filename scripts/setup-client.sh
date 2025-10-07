#!/bin/bash

echo "🔧 Setting up MLflow Client Environment"
echo "======================================"

# Install required Python packages
echo "📦 Installing MLflow and dependencies..."
pip install mlflow psycopg2-binary pandas scikit-learn

# Create environment file
cat > ~/.mlflow_env << 'EOF'
# MLflow Environment Configuration
export MLFLOW_TRACKING_URI=http://localhost:30500
export MLFLOW_REGISTRY_URI=http://localhost:30500

# Database access
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432
export POSTGRES_DB=mlflow
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=postgres
EOF

echo "📝 Created ~/.mlflow_env"
echo ""
echo "🔗 Setup port forwarding for direct access:"
echo "kubectl port-forward -n mlflow svc/mlflow-service 5000:5000 &"
echo "kubectl port-forward -n mlflow svc/postgres-service 5432:5432 &"
echo ""
echo "📋 Load environment variables:"
echo "source ~/.mlflow_env"
echo ""
echo "🐍 Test Python connection:"
echo "python3 scripts/mlflow_client_demo.py"
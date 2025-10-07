#!/bin/bash

echo "🐘 PostgreSQL Access Options for MLflow"
echo "========================================"

echo ""
echo "1️⃣  Port Forward to PostgreSQL:"
echo "kubectl port-forward -n mlflow svc/postgres-service 5432:5432"
echo ""

echo "2️⃣  Connect via psql:"
echo "psql -h localhost -p 5432 -U postgres -d mlflow"
echo "Password: postgres"
echo ""

echo "3️⃣  Connect via Python:"
cat << 'EOF'
import psycopg2
import pandas as pd

# Connection parameters
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="mlflow",
    user="postgres",
    password="postgres"
)

# Query experiments
df = pd.read_sql("SELECT * FROM experiments;", conn)
print(df)

# Query runs
df = pd.read_sql("SELECT * FROM runs LIMIT 10;", conn)
print(df)
EOF

echo ""
echo "4️⃣  Deploy PostgreSQL Admin UI (pgAdmin):"
echo "./scripts/deploy-pgadmin.sh"
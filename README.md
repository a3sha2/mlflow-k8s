# MLflow Model Registry on Kubernetes

A complete MLflow Model Registry deployment for Kubernetes with PostgreSQL backend, persistent storage, and comprehensive management tools. Built for production ML workflows with REST API access and database management capabilities.

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   MLflow UI     │    │  MLflow Server   │    │   PostgreSQL    │
│   (NodePort)    │◄──►│   (Registry)     │◄──►│   (Backend)     │
│   Port: 30500   │    │   Port: 5000     │    │   Port: 5432    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │  Artifact Store │
                       │ (Persistent Vol)│
                       └─────────────────┘
                                │
                       ┌─────────────────┐
                       │    PgAdmin      │
                       │ (Optional UI)   │
                       │   Port: 30800   │
                       └─────────────────┘
```

## ✨ Key Features

✅ **Production-Ready MLflow Registry**: Kubernetes-native deployment  
✅ **PostgreSQL Backend**: Robust metadata storage with persistence  
✅ **REST API Support**: No Python library dependencies needed  
✅ **Web Management**: MLflow UI + PgAdmin for database management  
✅ **Direct Database Access**: Port forwarding and connection scripts  
✅ **Comprehensive Tooling**: Deployment, monitoring, and demo scripts  
✅ **Persistent Storage**: Data survives pod restarts and scaling  
✅ **Scalable Architecture**: Ready for multi-replica deployments  

## 🚀 Quick Start

### 1. Deploy MLflow Registry

```bash
# Clone the repository
git clone <your-repo-url>
cd mlflow-k8s

# Make scripts executable
chmod +x scripts/*.sh

# Deploy complete MLflow stack
./scripts/deploy.sh

# Optional: Deploy PgAdmin for database management
./scripts/deploy-pgadmin.sh
```

### 2. Access Services

- **🌐 MLflow UI**: http://localhost:30500
- **🔧 PgAdmin**: http://localhost:30800 (admin@mlflow.local / admin123)
- **🐘 PostgreSQL**: Port forward with `kubectl port-forward -n mlflow svc/postgres-service 5432:5432`

### 3. Quick Test

```bash
# Test connectivity and create demo experiments
python3 scripts/mlflow_rest_demo.py

# View database contents directly
python3 scripts/view_database.py
```

## � Available Scripts

### Core Management
- **`deploy.sh`** - Complete MLflow deployment to Kubernetes
- **`cleanup.sh`** - Clean removal of all MLflow components
- **`deploy-pgadmin.sh`** - Deploy PostgreSQL management UI

### Development & Testing
- **`mlflow_rest_demo.py`** - Complete ML experiment demo using REST API
- **`view_database.py`** - Direct PostgreSQL database inspection
- **`test_connectivity.py`** - Connection testing for all services
- **`setup-client.sh`** - Environment setup for MLflow clients

### Access & Configuration
- **`postgres-access.sh`** - PostgreSQL connection guide
- **`configs/mlflow.env`** - Environment variables
- **`configs/external-access.conf`** - External access configuration  

## 🔧 Usage Examples

### REST API Approach (Recommended)

```python
import requests
import json

# MLflow REST API Client - No library dependencies
class MLflowClient:
    def __init__(self, tracking_uri="http://localhost:30500"):
        self.api_base = f"{tracking_uri}/api/2.0/mlflow"
    
    def create_experiment(self, name):
        response = requests.post(f"{self.api_base}/experiments/create", 
                               json={"name": name})
        return response.json()["experiment_id"]
    
    def create_run(self, experiment_id):
        response = requests.post(f"{self.api_base}/runs/create", 
                               json={"experiment_id": experiment_id})
        return response.json()["run"]["info"]["run_id"]
    
    def log_metric(self, run_id, key, value):
        requests.post(f"{self.api_base}/runs/log-metric", 
                     json={"run_id": run_id, "key": key, "value": value})

# Usage
client = MLflowClient()
exp_id = client.create_experiment("my-project")
run_id = client.create_run(exp_id)
client.log_metric(run_id, "accuracy", 0.95)
```

### Direct Database Access

```python
import psycopg2

# Connect to MLflow PostgreSQL backend
conn = psycopg2.connect(
    host="localhost", port=5432, 
    database="mlflow", user="postgres", password="postgres"
)

# Query experiments directly
cursor = conn.cursor()
cursor.execute("SELECT name, experiment_id FROM experiments;")
experiments = cursor.fetchall()
print("Experiments:", experiments)
```

### Quick Demo Script

```bash
# Run complete ML experiment demo
python3 scripts/mlflow_rest_demo.py

# Output:
# ✅ Connected to MLflow: http://localhost:30500
# 📊 Created experiment: demo-ml-project-rest (ID: 1)
# 🔬 Training RandomForest... ✅ Completed - Final Accuracy: 0.884
# 🔬 Training XGBoost... ✅ Completed - Final Accuracy: 0.950
# 🌐 View results at: http://localhost:30500
```

## 🔍 Monitoring & Management

```bash
# Check deployment status
kubectl get all -n mlflow

# Monitor pods and services
kubectl get pods -n mlflow -w
kubectl get svc -n mlflow

# View logs
kubectl logs -f deployment/mlflow-server -n mlflow
kubectl logs -f deployment/postgres -n mlflow

# Database management
kubectl port-forward -n mlflow svc/postgres-service 5432:5432
python3 scripts/view_database.py

# Scale MLflow server
kubectl scale deployment mlflow-server --replicas=2 -n mlflow

# Check resource usage
kubectl top pods -n mlflow
```

## 🌐 External Access

### From Outside Kubernetes Cluster

```bash
# NodePort access (if cluster accessible)
curl http://<node-ip>:30500/health

# Port forwarding for local development
kubectl port-forward -n mlflow svc/mlflow-service 5000:5000
export MLFLOW_TRACKING_URI=http://localhost:5000
```

### From Within Kubernetes Cluster

```yaml
# Use service DNS names in your applications
MLFLOW_TRACKING_URI: http://mlflow-service.mlflow.svc.cluster.local:5000
POSTGRES_HOST: postgres-service.mlflow.svc.cluster.local
```

## 🗂️ Project Structure

```
mlflow-k8s/
├── manifests/                    # Kubernetes YAML definitions
│   ├── 01-namespace.yaml        # MLflow namespace
│   ├── 02-postgres.yaml         # PostgreSQL database + PVC
│   ├── 03-mlflow-server.yaml    # MLflow server + services
│   └── 04-pgadmin.yaml          # PostgreSQL management UI
├── scripts/                      # Management and demo scripts
│   ├── deploy.sh                # Complete deployment automation
│   ├── cleanup.sh               # Clean removal of all components
│   ├── deploy-pgadmin.sh        # PostgreSQL UI deployment
│   ├── setup-client.sh          # Environment setup
│   ├── mlflow_rest_demo.py      # ML experiment demo (REST API)
│   ├── view_database.py         # Direct database inspection
│   ├── test_connectivity.py     # Connection testing
│   └── postgres-access.sh       # Database access guide
├── configs/                      # Configuration files
│   ├── mlflow.env               # Environment variables
│   └── external-access.conf     # External access configuration
└── README.md                     # Complete documentation
```

## 🔧 Troubleshooting

### Common Issues

**MLflow UI not accessible:**
```bash
kubectl get svc -n mlflow
curl http://localhost:30500/health
```

**Database connection issues:**
```bash
kubectl get pods -n mlflow
kubectl port-forward -n mlflow svc/postgres-service 5432:5432
python3 scripts/test_connectivity.py
```

**PgAdmin not loading:**
```bash
kubectl logs deployment/pgadmin -n mlflow
# PgAdmin might have resource constraints, check pod status
```

### Performance Tuning

**Scale MLflow server:**
```bash
kubectl scale deployment mlflow-server --replicas=3 -n mlflow
```

**Increase PostgreSQL resources:**
```bash
# Edit manifests/02-postgres.yaml
# Update resource requests/limits
kubectl apply -f manifests/02-postgres.yaml
```

## 🧹 Cleanup

```bash
# Complete cleanup of all MLflow components
./scripts/cleanup.sh

# Manual cleanup if needed
kubectl delete namespace mlflow
```

## ⚙️ Configuration

### Environment Variables (`configs/mlflow.env`)
```bash
MLFLOW_TRACKING_URI=http://localhost:30500
MLFLOW_REGISTRY_URI=http://localhost:30500
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=mlflow
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
```

### Kubernetes Resources
- **MLflow Server**: 500m CPU, 1Gi RAM (configurable)
- **PostgreSQL**: Default resources (upgrade in production)
- **Storage**: 10Gi for PostgreSQL, 20Gi for artifacts

## � Requirements

- **Kubernetes cluster** (tested on v1.31+)
- **kubectl** configured and connected
- **Python 3.6+** for demo scripts
- **curl** for API testing

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **MLflow Team** for the excellent ML platform
- **PostgreSQL Community** for robust database backend
- **Kubernetes Community** for container orchestration
- **Python Community** for ecosystem support

---

**Built with ❤️ for Production ML Workflows**
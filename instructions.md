# 🛠️ Kubernetes & Docker Deployment Instructions

This guide provides step-by-step instructions for containerizing and deploying "The Evolution of Todo" application to a local Kubernetes cluster using Docker and Helm.

## 📦 1. Docker Deployment (Local Containerization)

### Build Docker Images
Ensure you are in the project root directory.

```bash
# Build Backend Image
docker build -f Dockerfile.backend -t todo-backend:latest .

# Build Frontend Image
docker build -f Dockerfile.frontend -t todo-frontend:latest .
```

### Run with Docker Compose
For a quick local test of the containerized stack:

```bash
docker-compose up -d
```
- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000

---

## ☸️ 2. Kubernetes Deployment (Phase IV Core)

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) with Kubernetes enabled OR [Minikube](https://minikube.sigs.k8s.io/docs/start/)
- [Helm 3.x](https://helm.sh/docs/intro/install/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)

### Step 1: Start Minikube (Recommended)
```bash
minikube start --driver=docker
# Configure terminal to use Minikube's Docker daemon
eval $(minikube docker-env)
```

### Step 2: Secrets Management
Create a Kubernetes secret for sensitive environment variables. This avoids hardcoding secrets in your manifests.

```bash
kubectl create secret generic todo-app-secrets \
  --from-literal=DATABASE_URL="your_postgresql_url" \
  --from-literal=BETTER_AUTH_SECRET="your_auth_secret" \
  --from-literal=OPENAI_API_KEY="your_openai_key" \
  --from-literal=GITHUB_TOKEN="your_github_token"
```

### Step 3: Deploy via Helm
The project includes a ready-to-use Helm chart in the `helm-chart/` directory.

```bash
cd helm-chart

# Install the chart
helm install todo-app .

# Verify deployment
kubectl get pods
kubectl get svc
```

### Step 4: Accessing the Application (Tunneling)
Since Kubernetes runs in an isolated network, you need to expose the services to your localhost.

**Option A: Unified Management Script (Recommended)**
```bash
uv run python manage_phase_4.py tunnel
```

**Option B: Manual Port-Forwarding**
```bash
# Terminal 1: Frontend
kubectl port-forward svc/todo-app-frontend-service 3000:3000

# Terminal 2: Backend
kubectl port-forward svc/todo-app-backend-service 8000:8000
```

---

## 🤖 3. AI-Assisted Operations

Use AI to manage and monitor your cluster:

### Using `kubectl-ai`
```bash
# Scale your backend
kubectl-ai "scale deployment todo-app-backend to 3 replicas"

# Check pod health
kubectl-ai "why is my frontend pod failing?"
```

### Using `kagent`
```bash
# Analyze cluster resources
kagent "analyze resource usage and suggest optimizations"
```

## 🧪 Verification Checklist
- [ ] Pods are in `Running` state: `kubectl get pods`
- [ ] Services are accessible via tunnel: http://localhost:3000
- [ ] Data persists after pod restart: `kubectl delete pod -l app=todo-backend`
- [ ] AI Chat is functional within the K8s environment
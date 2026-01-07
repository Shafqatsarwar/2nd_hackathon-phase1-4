# Docker and Kubernetes Deployment Instructions

## Prerequisites
- Docker Desktop/Engine with Docker Compose
- Kubernetes cluster (Minikube/Docker Desktop with Kubernetes)
- Helm 3.x and kubectl
- Node.js 18+, Python 3.12+

## Docker Deployment

### 1. Build Images
```bash
# Build backend
docker build -f Dockerfile.backend -t todo-backend:latest .

# Build frontend
docker build -f Dockerfile.frontend -t todo-frontend:latest .
```

### 2. Set Environment Variables
```bash
export DATABASE_URL="your_postgres_connection_string"
export BETTER_AUTH_SECRET="your_32_char_secret"
export OPENAI_API_KEY="your_openai_api_key"
export GITHUB_TOKEN="your_github_token"
export GITHUB_OWNER="your_github_username"
export GITHUB_REPO="your_repository_name"
```

### 3. Run with Docker Compose
```bash
# Start services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

## Kubernetes Deployment

### 1. Set Environment Variables (same as above)
```bash
export DATABASE_URL="your_postgres_connection_string"
export BETTER_AUTH_SECRET="your_32_char_secret"
export OPENAI_API_KEY="your_openai_api_key"
export GITHUB_TOKEN="your_github_token"
export GITHUB_OWNER="your_github_username"
export GITHUB_REPO="your_repository_name"
```

### 2. Create Kubernetes Secrets
```bash
kubectl create secret generic todo-app-secrets \
  --from-literal=DATABASE_URL="$DATABASE_URL" \
  --from-literal=BETTER_AUTH_SECRET="$BETTER_AUTH_SECRET" \
  --from-literal=OPENAI_API_KEY="$OPENAI_API_KEY" \
  --from-literal=GITHUB_TOKEN="$GITHUB_TOKEN" \
  --from-literal=GITHUB_OWNER="$GITHUB_OWNER" \
  --from-literal=GITHUB_REPO="$GITHUB_REPO"
```

### 3. Deploy with Helm
```bash
# Navigate to helm chart
cd helm-chart

# Install release
helm install todo-release .

# Check status
kubectl get pods
kubectl get svc
kubectl rollout status deployment/todo-release-backend
kubectl rollout status deployment/todo-release-frontend
```

### 4. Access Application
```bash
# Port forward for local access
kubectl port-forward svc/todo-release-frontend-service 3000:3000
kubectl port-forward svc/todo-release-backend-service 8000:8000

# Or get external IPs
kubectl get svc todo-release-frontend-service
kubectl get svc todo-release-backend-service
```

### 5. Scaling & Management
```bash
# Scale deployments
kubectl scale deployment todo-release-backend --replicas=3
kubectl scale deployment todo-release-frontend --replicas=2

# Upgrade deployment
helm upgrade todo-release .

# Check logs
kubectl logs -l app=todo-backend
kubectl logs -l app=todo-frontend
```

### 6. Cleanup
```bash
# Uninstall Helm release
helm uninstall todo-release

# Delete secrets
kubectl delete secret todo-app-secrets
```
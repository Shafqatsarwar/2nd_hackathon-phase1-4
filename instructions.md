# Instructions for Docker and Kubernetes Deployment

This document provides instructions for deploying the Todo application using Docker and Kubernetes.

## Docker Setup

### Prerequisites
- Docker Desktop or Docker Engine
- Docker Compose (for local testing)

### Building Docker Images

1. **Build Backend Image:**
   ```bash
   docker build -f Dockerfile.backend -t todo-backend:latest .
   ```

2. **Build Frontend Image:**
   ```bash
   docker build -f Dockerfile.frontend -t todo-frontend:latest .
   ```

### Running with Docker Compose

1. **Set up environment variables:**
   ```bash
   export DATABASE_URL="your_database_url"
   export BETTER_AUTH_SECRET="your_auth_secret"
   export OPENAI_API_KEY="your_openai_key"
   export GITHUB_TOKEN="your_github_token"
   export GITHUB_OWNER="your_github_username"
   export GITHUB_REPO="your_repository_name"
   ```

2. **Start the application:**
   ```bash
   docker-compose up -d
   ```

3. **Check the logs:**
   ```bash
   docker-compose logs -f
   ```

## Kubernetes Setup

### Prerequisites
- Kubernetes cluster (Minikube, Docker Desktop with Kubernetes, or cloud provider)
- Helm 3.x
- kubectl

### Deploying to Kubernetes

1. **Set up environment variables:**
   ```bash
   export DATABASE_URL="your_database_url"
   export BETTER_AUTH_SECRET="your_auth_secret"
   export OPENAI_API_KEY="your_openai_key"
   export GITHUB_TOKEN="your_github_token"
   export GITHUB_OWNER="your_github_username"
   export GITHUB_REPO="your_repository_name"
   ```

2. **Create Kubernetes secrets:**
   ```bash
   kubectl create secret generic todo-app-secrets \
     --from-literal=DATABASE_URL="$DATABASE_URL" \
     --from-literal=BETTER_AUTH_SECRET="$BETTER_AUTH_SECRET" \
     --from-literal=OPENAI_API_KEY="$OPENAI_API_KEY" \
     --from-literal=GITHUB_TOKEN="$GITHUB_TOKEN" \
     --from-literal=GITHUB_OWNER="$GITHUB_OWNER" \
     --from-literal=GITHUB_REPO="$GITHUB_REPO"
   ```

3. **Deploy using Helm:**
   ```bash
   cd helm-chart
   helm install todo-release .
   ```

4. **Check deployment status:**
   ```bash
   kubectl get pods
   kubectl get services
   kubectl rollout status deployment/todo-release-backend
   kubectl rollout status deployment/todo-release-frontend
   ```

### Scaling the Application

1. **Scale backend replicas:**
   ```bash
   kubectl scale deployment todo-release-backend --replicas=3
   ```

2. **Scale frontend replicas:**
   ```bash
   kubectl scale deployment todo-release-frontend --replicas=2
   ```

### Accessing the Application

1. **Port forward to access locally:**
   ```bash
   kubectl port-forward svc/todo-release-frontend-service 3000:3000
   kubectl port-forward svc/todo-release-backend-service 8000:8000
   ```

2. **Check service endpoints:**
   ```bash
   kubectl get svc todo-release-frontend-service
   kubectl get svc todo-release-backend-service
   ```

### Updating the Deployment

1. **Update Helm values:**
   Edit `helm-chart/values.yaml` with new image tags or configurations

2. **Upgrade the release:**
   ```bash
   cd helm-chart
   helm upgrade todo-release .
   ```

### Troubleshooting

1. **Check pod logs:**
   ```bash
   kubectl logs -l app=todo-backend
   kubectl logs -l app=todo-frontend
   ```

2. **Describe pods for details:**
   ```bash
   kubectl describe pod <pod-name>
   ```

3. **Check events:**
   ```bash
   kubectl get events --sort-by=.metadata.creationTimestamp
   ```

### Cleanup

1. **Uninstall Helm release:**
   ```bash
   helm uninstall todo-release
   ```

2. **Delete secrets:**
   ```bash
   kubectl delete secret todo-app-secrets
   ```
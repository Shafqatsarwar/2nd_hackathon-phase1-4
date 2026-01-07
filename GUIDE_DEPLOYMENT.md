# Deployment Instructions for The Evolution of Todo - Phase IV

This document provides instructions for deploying the Todo application to Kubernetes.

## Prerequisites

- **Docker Desktop** with Kubernetes enabled (or Minikube)
- **Helm 3.x**
- **kubectl**
- **Environment variables** set for your infrastructure

## Environment Variables

Before deploying, ensure you have the following environment variables set:

```bash
export DATABASE_URL="your_database_connection_string"
export BETTER_AUTH_SECRET="your_better_auth_secret"
export OPENAI_API_KEY="your_openai_api_key"
```

## Quick Deployment

Use the automated deployment script:

```bash
# Make sure environment variables are set
export DATABASE_URL="your_database_connection_string"
export BETTER_AUTH_SECRET="your_better_auth_secret"
export OPENAI_API_KEY="your_openai_api_key"

# Run the full deployment
./scripts/deploy.sh
```

## Step-by-Step Deployment

### 1. Build Images
```bash
./scripts/deploy.sh build
```

### 2. Create Secrets
```bash
./scripts/deploy.sh secrets
```

### 3. Deploy to Kubernetes
```bash
./scripts/deploy.sh deploy
```

### 4. Verify Deployment
```bash
./scripts/deploy.sh verify
```

## Manual Deployment (Alternative Method)

If you prefer to deploy manually:

### 1. Build Docker Images
```bash
docker build -f Dockerfile.backend -t todo-backend:latest .
docker build -f Dockerfile.frontend -t todo-frontend:latest .
```

### 2. Create Kubernetes Secrets
```bash
kubectl create secret generic todo-app-secrets \
    --from-literal=DATABASE_URL="$DATABASE_URL" \
    --from-literal=BETTER_AUTH_SECRET="$BETTER_AUTH_SECRET" \
    --from-literal=OPENAI_API_KEY="$OPENAI_API_KEY"
```

### 3. Deploy with Helm
```bash
cd helm-chart
helm install todo-release .
```

### 4. Verify Deployment
```bash
kubectl get pods
kubectl get services
kubectl rollout status deployment/todo-release-backend
kubectl rollout status deployment/todo-release-frontend
```

## Accessing the Application

After deployment, you can access the services in the following ways:

### Local Access (Port Forwarding)
```bash
# Frontend
kubectl port-forward svc/todo-release-frontend-service 3000:3000

# Backend
kubectl port-forward svc/todo-release-backend-service 8000:8000
```

Then access:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000

### Ingress (if configured)
If you have ingress configured, you can access the application via the configured domain.

## Troubleshooting

### Check Pod Status
```bash
kubectl get pods
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

### Check Services
```bash
kubectl get services
kubectl describe service <service-name>
```

### Check Deployment Status
```bash
kubectl rollout status deployment/todo-release-backend
kubectl rollout status deployment/todo-release-frontend
```

### Redeploy
```bash
cd helm-chart
helm upgrade todo-release .
```

### Clean Up
```bash
helm uninstall todo-release
kubectl delete secret todo-app-secrets
```

## Scaling

To scale the deployments:

```bash
# Scale backend
kubectl scale deployment todo-release-backend --replicas=3

# Scale frontend
kubectl scale deployment todo-release-frontend --replicas=2
```

## GitHub Integration

The application includes GitHub MCP tools for integration with GitHub. Ensure the following environment variables are set if you plan to use GitHub integration:

```bash
export GITHUB_TOKEN="your_github_personal_access_token"
export GITHUB_OWNER="your_github_username"
export GITHUB_REPO="your_repository_name"
```

These can be added to the Kubernetes secrets if GitHub integration is needed in the deployed environment.
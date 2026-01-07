# Phase IV: Docker and Kubernetes Setup Instructions

This document provides temporary instructions for setting up Docker and Kubernetes for the Phase IV deployment of the "Evolution of Todo" project.

## Prerequisites

- Docker Desktop or Docker Engine installed
- Minikube installed
- kubectl installed
- Helm installed
- Node.js 18+ installed
- Python 3.12+ installed

## Docker Setup

### 1. Build Docker Images

First, build the Docker images for both frontend and backend:

```bash
# Build backend image
docker build -f Dockerfile.backend -t todo-backend:latest .

# Build frontend image
docker build -f Dockerfile.frontend -t todo-frontend:latest .
```

### 2. Test Docker Images Locally

You can test the Docker images using docker-compose:

```bash
# Start the full application stack
docker-compose up --build

# Access the application:
# - Frontend: http://localhost:3000
# - Backend: http://localhost:8000
# - Backend API docs: http://localhost:8000/docs
```

## Kubernetes Setup

### 1. Start Minikube

```bash
# Start Minikube cluster
minikube start

# Verify cluster is running
kubectl cluster-info
```

### 2. Install Helm Chart

```bash
# Navigate to the helm chart directory
cd helm-chart

# Install the Helm chart
helm install todo-app . --set backend.image.tag=latest --set frontend.image.tag=latest

# Verify installation
kubectl get pods
kubectl get services
```

### 3. Access the Application

```bash
# Port forward the frontend service
kubectl port-forward service/todo-frontend-service 3000:3000

# Or use Minikube tunnel for external access
minikube tunnel
```

## Configuration

### Environment Variables

The application is configured via environment variables in the Helm chart values:

- `NEXT_PUBLIC_BACKEND_URL`: URL for the backend API
- `NEXT_PUBLIC_BETTER_AUTH_URL`: URL for Better Auth
- `DATABASE_URL`: PostgreSQL connection string
- `BETTER_AUTH_SECRET`: Secret key for authentication
- `OPENAI_API_KEY`: OpenAI API key for AI features

These are configured in `helm-chart/values.yaml`.

## Troubleshooting

### Common Issues

1. **ImagePullBackOff**: Make sure Docker images are built locally before deploying to Kubernetes
2. **Service unavailable**: Check that all pods are running with `kubectl get pods`
3. **Database connection errors**: Verify PostgreSQL is running and accessible

### Useful Commands

```bash
# Check pod status
kubectl get pods

# View pod logs
kubectl logs -l app=todo-backend
kubectl logs -l app=todo-frontend

# Check service endpoints
kubectl get services

# Scale deployments
kubectl scale deployment todo-backend --replicas=3
kubectl scale deployment todo-frontend --replicas=2

# Update Helm deployment
helm upgrade todo-app .

# Uninstall Helm release
helm uninstall todo-app
```

## Deployment Notes

- The application is designed to be cloud-native with immutable containers
- All configuration is done via environment variables (no hardcoded values)
- The system supports multi-replica deployments for scalability
- Kubernetes is the source of truth for infrastructure
- The application survives pod restarts with zero data loss
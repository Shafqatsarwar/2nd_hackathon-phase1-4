# 🎯 Quick Reference - Docker & Kubernetes

## 🚀 Quick Start

### Option 1: Automated Deployment (Easiest)
```bash
chmod +x deploy.sh
./deploy.sh
# Select option 1 for Docker or 2 for Kubernetes
```

### Option 2: Manual Docker Deployment
```bash
# 1. Build images
docker build -f Dockerfile.backend -t todo-backend:latest .
docker build -f Dockerfile.frontend -t todo-frontend:latest .

# 2. Start services
docker-compose up -d

# 3. Access
# Frontend: http://localhost:3000
# Backend: http://localhost:8000/docs
```

### Option 3: Manual Kubernetes Deployment
```bash
# 1. Start Minikube
minikube start --driver=docker

# 2. Use Minikube's Docker
eval $(minikube docker-env)

# 3. Build images
docker build -f Dockerfile.backend -t todo-backend:latest .
docker build -f Dockerfile.frontend -t todo-frontend:latest .

# 4. Create secrets
kubectl create secret generic todo-app-secrets \
  --from-literal=OPENAI_API_KEY="your-key-here" \
  --from-literal=DATABASE_URL="postgresql://postgres:postgres@postgres-service:5432/todo_db" \
  --from-literal=BETTER_AUTH_SECRET="your-secret"

# 5. Deploy with Helm
helm install todo-app ./helm-chart

# 6. Port forward
kubectl port-forward svc/todo-app-frontend-service 3000:3000
kubectl port-forward svc/todo-app-backend-service 8000:8000
```

---

## 📋 Essential Commands

### Docker
```bash
# Build
docker build -f Dockerfile.backend -t todo-backend:latest .
docker build -f Dockerfile.frontend -t todo-frontend:latest .

# Run
docker-compose up -d          # Start in background
docker-compose logs -f        # View logs
docker-compose ps             # Check status
docker-compose down           # Stop all services
docker-compose down -v        # Stop and remove volumes

# Debug
docker logs <container-id>
docker exec -it <container-id> /bin/sh
```

### Kubernetes
```bash
# Cluster
minikube start                # Start cluster
minikube status               # Check status
minikube stop                 # Stop cluster
minikube delete               # Delete cluster
minikube dashboard            # Open dashboard

# Pods
kubectl get pods              # List pods
kubectl describe pod <name>   # Pod details
kubectl logs <pod-name>       # View logs
kubectl logs -f <pod-name>    # Follow logs
kubectl delete pod <name>     # Delete pod

# Services
kubectl get svc               # List services
kubectl describe svc <name>   # Service details

# Secrets
kubectl get secrets           # List secrets
kubectl describe secret <name>
kubectl delete secret <name>

# Helm
helm list                     # List releases
helm install <name> <chart>   # Install
helm upgrade <name> <chart>   # Upgrade
helm uninstall <name>         # Uninstall
```

---

## 🔍 Troubleshooting

### Docker Issues

**Container won't start:**
```bash
docker-compose logs <service-name>
docker inspect <container-id>
```

**Port already in use:**
```bash
# Linux/WSL
lsof -i :3000
lsof -i :8000

# Windows
netstat -ano | findstr :3000
netstat -ano | findstr :8000
```

**Clean rebuild:**
```bash
docker-compose down -v
docker system prune -a
docker-compose up -d --build
```

### Kubernetes Issues

**Pods not starting (ImagePullBackOff):**
```bash
# Make sure using Minikube's Docker
eval $(minikube docker-env)

# Rebuild images
docker build -f Dockerfile.backend -t todo-backend:latest .
docker build -f Dockerfile.frontend -t todo-frontend:latest .

# Update pullPolicy
helm upgrade todo-app ./helm-chart \
  --set backend.image.pullPolicy=IfNotPresent \
  --set frontend.image.pullPolicy=IfNotPresent
```

**Pods crashing (CrashLoopBackOff):**
```bash
# Check logs
kubectl logs <pod-name>

# Check events
kubectl describe pod <pod-name>

# Check secrets
kubectl get secret todo-app-secrets -o yaml
```

**Can't access services:**
```bash
# Check if port-forward is running
kubectl port-forward svc/todo-app-frontend-service 3000:3000

# Or use Minikube service
minikube service todo-app-frontend-service
```

---

## 🧪 Testing

### Health Checks
```bash
# Backend health
curl http://localhost:8000/health

# Frontend
curl http://localhost:3000

# In Kubernetes (after port-forward)
curl http://localhost:8000/health
curl http://localhost:3000
```

### Database Connection
```bash
# Docker
docker exec -it <postgres-container> psql -U postgres -d todo_db

# Kubernetes
kubectl exec -it <postgres-pod> -- psql -U postgres -d todo_db
```

---

## 📊 Monitoring

### Docker
```bash
# Resource usage
docker stats

# Logs
docker-compose logs -f --tail=100

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Kubernetes
```bash
# Pod status
kubectl get pods -w

# Resource usage
kubectl top pods
kubectl top nodes

# Events
kubectl get events --sort-by=.metadata.creationTimestamp

# Dashboard
minikube dashboard
```

---

## 🔐 Secrets Management

### Update Secrets
```bash
# Delete old secret
kubectl delete secret todo-app-secrets

# Create new secret
kubectl create secret generic todo-app-secrets \
  --from-literal=OPENAI_API_KEY="new-key" \
  --from-literal=DATABASE_URL="new-url" \
  --from-literal=BETTER_AUTH_SECRET="new-secret"

# Restart pods to pick up new secrets
kubectl rollout restart deployment/todo-app-backend
kubectl rollout restart deployment/todo-app-frontend
```

---

## 📦 Scaling

### Docker Compose
```bash
# Scale a service
docker-compose up -d --scale backend=3
```

### Kubernetes
```bash
# Manual scaling
kubectl scale deployment todo-app-backend --replicas=3
kubectl scale deployment todo-app-frontend --replicas=3

# Auto-scaling
helm upgrade todo-app ./helm-chart \
  --set autoscaling.enabled=true \
  --set autoscaling.minReplicas=2 \
  --set autoscaling.maxReplicas=10
```

---

## 🗑️ Cleanup

### Docker
```bash
# Stop services
docker-compose down

# Remove volumes
docker-compose down -v

# Remove images
docker rmi todo-backend:latest todo-frontend:latest

# Full cleanup
docker system prune -a --volumes
```

### Kubernetes
```bash
# Uninstall Helm release
helm uninstall todo-app

# Delete secrets
kubectl delete secret todo-app-secrets

# Stop Minikube
minikube stop

# Delete Minikube cluster
minikube delete
```

---

## 🎓 Learning Resources

- **Full Guide**: `DOCKER_KUBERNETES_DEPLOYMENT.md`
- **Streaming Fix**: `STREAMING_FIX_APPLIED.md`
- **Instructions**: `instructions.md`
- **Project Guide**: `guide.md`

---

## 🆘 Getting Help

1. Check logs: `docker-compose logs` or `kubectl logs`
2. Review documentation: `DOCKER_KUBERNETES_DEPLOYMENT.md`
3. Check pod status: `kubectl describe pod <name>`
4. Verify secrets: `kubectl get secrets`
5. Test connectivity: `curl http://localhost:8000/health`

---

**Need more help?** See the full deployment guide in `DOCKER_KUBERNETES_DEPLOYMENT.md`

# 🚀 Docker & Kubernetes Deployment Guide

Complete guide for containerizing and deploying "The Evolution of Todo" application to Kubernetes.

---

## 📋 Prerequisites

### Required Tools:
- ✅ **Docker Desktop** (with Kubernetes enabled) OR **Minikube**
- ✅ **kubectl** (Kubernetes CLI)
- ✅ **Helm 3.x** (Kubernetes package manager)
- ✅ **WSL2** (for Windows users)

### Verify Installation:
```bash
# Check Docker
docker --version
# Expected: Docker version 24.x.x or higher

# Check Kubernetes
kubectl version --client
# Expected: Client Version: v1.28.x or higher

# Check Helm
helm version
# Expected: version.BuildInfo{Version:"v3.x.x"}
```

---

## 🐳 Part 1: Docker Deployment

### Step 1: Generate requirements.txt

The `requirements.txt` file is currently empty. We need to generate it from `pyproject.toml`:

```bash
cd ~/Projects/2nd_hackathon-phase1-4

# Generate requirements.txt from pyproject.toml
uv pip compile pyproject.toml -o requirements.txt
```

**Alternative (if uv compile doesn't work):**
```bash
# Export from current environment
uv pip freeze > requirements.txt
```

### Step 2: Build Docker Images

```bash
# Build Backend Image
docker build -f Dockerfile.backend -t todo-backend:latest .

# Build Frontend Image
docker build -f Dockerfile.frontend -t todo-frontend:latest .
```

**Expected Output:**
```
Successfully built <image-id>
Successfully tagged todo-backend:latest
Successfully tagged todo-frontend:latest
```

**Verify Images:**
```bash
docker images | grep todo
# Should show:
# todo-backend    latest    <id>    <time>    <size>
# todo-frontend   latest    <id>    <time>    <size>
```

### Step 3: Create Environment File

Create `.env` file in project root (if not exists):

```bash
cat > .env << 'EOF'
# Database Configuration
DATABASE_URL=postgresql://postgres:postgres@db:5432/todo_db

# Authentication
BETTER_AUTH_SECRET=your-secret-key-change-in-production

# OpenAI API Key
OPENAI_API_KEY=your-openai-api-key-here

# GitHub Integration (Optional)
GITHUB_TOKEN=your-github-token-here
GITHUB_OWNER=your-github-username
GITHUB_REPO=your-repo-name
EOF
```

**⚠️ Important:** Replace placeholder values with your actual credentials!

### Step 4: Run with Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Check running containers
docker ps
```

**Expected Services:**
- `backend` - Running on port 8000
- `frontend` - Running on port 3000
- `db` - PostgreSQL on port 5432

### Step 5: Test Docker Deployment

```bash
# Test Backend Health
curl http://localhost:8000/health
# Expected: {"status":"healthy","database":"connected"}

# Test Frontend
curl http://localhost:3000
# Expected: HTML response

# Open in Browser
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000/docs
```

### Step 6: Stop Docker Compose

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (clean slate)
docker-compose down -v
```

---

## ☸️ Part 2: Kubernetes Deployment

### Prerequisites: Start Minikube

**Option A: Using Minikube (Recommended for local development)**

```bash
# Start Minikube with Docker driver
minikube start --driver=docker --cpus=4 --memory=8192

# Verify Minikube is running
minikube status
# Expected:
# minikube: Running
# kubelet: Running
# apiserver: Running

# Configure Docker to use Minikube's daemon
eval $(minikube docker-env)

# Verify
echo $DOCKER_HOST
# Should show: tcp://...
```

**Option B: Using Docker Desktop Kubernetes**

```bash
# Enable Kubernetes in Docker Desktop:
# 1. Open Docker Desktop
# 2. Go to Settings → Kubernetes
# 3. Check "Enable Kubernetes"
# 4. Click "Apply & Restart"

# Verify
kubectl config current-context
# Expected: docker-desktop
```

### Step 1: Rebuild Images for Kubernetes

**Important:** When using Minikube, rebuild images in Minikube's Docker daemon:

```bash
# Make sure you're using Minikube's Docker
eval $(minikube docker-env)

# Rebuild images
docker build -f Dockerfile.backend -t todo-backend:latest .
docker build -f Dockerfile.frontend -t todo-frontend:latest .

# Verify images are in Minikube
docker images | grep todo
```

### Step 2: Create Kubernetes Secrets

Kubernetes secrets store sensitive configuration:

```bash
# Create secrets for the application
kubectl create secret generic todo-app-secrets \
  --from-literal=DATABASE_URL="postgresql://postgres:postgres@postgres-service:5432/todo_db" \
  --from-literal=BETTER_AUTH_SECRET="your-secret-key-change-in-production" \
  --from-literal=OPENAI_API_KEY="your-openai-api-key-here" \
  --from-literal=GITHUB_TOKEN="your-github-token-here" \
  --from-literal=GITHUB_OWNER="your-github-username" \
  --from-literal=GITHUB_REPO="your-repo-name"

# Verify secret was created
kubectl get secrets
# Should show: todo-app-secrets
```

**⚠️ Important:** Replace placeholder values with your actual credentials!

**To update secrets later:**
```bash
# Delete old secret
kubectl delete secret todo-app-secrets

# Create new secret with updated values
kubectl create secret generic todo-app-secrets ...
```

### Step 3: Deploy with Helm

```bash
# Navigate to project root
cd ~/Projects/2nd_hackathon-phase1-4

# Install the Helm chart
helm install todo-app ./helm-chart

# Verify deployment
helm list
# Should show: todo-app deployed

# Check pods
kubectl get pods
# Expected: All pods in Running state
```

**Expected Output:**
```
NAME                                READY   STATUS    RESTARTS   AGE
todo-app-backend-xxxxxxxxx-xxxxx    1/1     Running   0          30s
todo-app-backend-xxxxxxxxx-xxxxx    1/1     Running   0          30s
todo-app-frontend-xxxxxxxxx-xxxxx   1/1     Running   0          30s
todo-app-frontend-xxxxxxxxx-xxxxx   1/1     Running   0          30s
```

### Step 4: Verify Services

```bash
# Check services
kubectl get svc
# Expected services:
# - todo-app-backend-service
# - todo-app-frontend-service

# Describe backend service
kubectl describe svc todo-app-backend-service

# Describe frontend service
kubectl describe svc todo-app-frontend-service
```

### Step 5: Access the Application

**Option A: Port Forwarding (Recommended)**

```bash
# Terminal 1: Forward Frontend
kubectl port-forward svc/todo-app-frontend-service 3000:3000

# Terminal 2: Forward Backend
kubectl port-forward svc/todo-app-backend-service 8000:8000
```

Now access:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/docs

**Option B: Using Minikube Tunnel**

```bash
# Start Minikube tunnel (requires sudo/admin)
minikube tunnel

# Get service URLs
minikube service todo-app-frontend-service --url
minikube service todo-app-backend-service --url
```

**Option C: Using Management Script**

```bash
# Use the provided management script
uv run python manage_phase_4.py tunnel
```

### Step 6: Monitor Deployment

```bash
# Watch pods in real-time
kubectl get pods -w

# View logs for a specific pod
kubectl logs -f <pod-name>

# Example: View backend logs
kubectl logs -f $(kubectl get pods -l app=todo-backend -o jsonpath='{.items[0].metadata.name}')

# View frontend logs
kubectl logs -f $(kubectl get pods -l app=todo-frontend -o jsonpath='{.items[0].metadata.name}')

# View all pod logs
kubectl logs -l app=todo-backend --tail=50
kubectl logs -l app=todo-frontend --tail=50
```

---

## 🔧 Troubleshooting

### Issue 1: Pods in ImagePullBackOff or ErrImagePull

**Cause:** Kubernetes can't find the Docker images

**Solution:**
```bash
# Make sure you're using Minikube's Docker daemon
eval $(minikube docker-env)

# Rebuild images
docker build -f Dockerfile.backend -t todo-backend:latest .
docker build -f Dockerfile.frontend -t todo-frontend:latest .

# Update Helm values to use IfNotPresent
helm upgrade todo-app ./helm-chart \
  --set backend.image.pullPolicy=IfNotPresent \
  --set frontend.image.pullPolicy=IfNotPresent
```

### Issue 2: Pods in CrashLoopBackOff

**Cause:** Application is crashing on startup

**Solution:**
```bash
# Check pod logs
kubectl logs <pod-name>

# Common issues:
# 1. Missing environment variables
kubectl describe pod <pod-name>

# 2. Database connection issues
kubectl get secret todo-app-secrets -o yaml

# 3. Check if secrets are properly mounted
kubectl exec -it <pod-name> -- env | grep DATABASE_URL
```

### Issue 3: requirements.txt is Empty

**Cause:** The file wasn't generated from pyproject.toml

**Solution:**
```bash
# Generate requirements.txt
uv pip compile pyproject.toml -o requirements.txt

# Or manually create it
cat > requirements.txt << 'EOF'
fastapi>=0.115.0
uvicorn>=0.30.0
pydantic>=2.8.0
sqlmodel>=0.0.14
psycopg2-binary>=2.9.9
pyjwt>=2.8
python-dotenv>=1.0
requests>=2.31
openai>=1.12.0
anthropic>=0.21.0
modelcontextprotocol>=1.0.1
duckduckgo-search>=6.2.6
EOF

# Rebuild backend image
docker build -f Dockerfile.backend -t todo-backend:latest .
```

### Issue 4: Frontend Can't Connect to Backend

**Cause:** Incorrect backend URL in frontend

**Solution:**
```bash
# Update Helm values
helm upgrade todo-app ./helm-chart \
  --set frontend.env.NEXT_PUBLIC_BACKEND_URL="http://todo-app-backend-service:8000"

# Or for local testing with port-forward
helm upgrade todo-app ./helm-chart \
  --set frontend.env.NEXT_PUBLIC_BACKEND_URL="http://localhost:8000"
```

### Issue 5: Database Connection Failed

**Cause:** PostgreSQL not running or wrong connection string

**Solution:**
```bash
# Check if using external database or need to deploy PostgreSQL
# Option 1: Deploy PostgreSQL in Kubernetes
kubectl apply -f - <<EOF
apiVersion: v1
kind: Service
metadata:
  name: postgres-service
spec:
  selector:
    app: postgres
  ports:
    - port: 5432
      targetPort: 5432
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:15
        env:
        - name: POSTGRES_DB
          value: todo_db
        - name: POSTGRES_USER
          value: postgres
        - name: POSTGRES_PASSWORD
          value: postgres
        ports:
        - containerPort: 5432
EOF

# Option 2: Use SQLite for testing
# Update backend to use SQLite instead
```

---

## 🧪 Verification Checklist

After deployment, verify:

### Docker Deployment:
- [ ] Backend image built successfully
- [ ] Frontend image built successfully
- [ ] Docker Compose starts all services
- [ ] Backend health check passes: `curl http://localhost:8000/health`
- [ ] Frontend accessible: http://localhost:3000
- [ ] Can login and use chat feature
- [ ] Database persists data after restart

### Kubernetes Deployment:
- [ ] Minikube/Kubernetes cluster running
- [ ] Images available in cluster: `docker images | grep todo`
- [ ] Secrets created: `kubectl get secrets`
- [ ] Helm chart installed: `helm list`
- [ ] All pods running: `kubectl get pods`
- [ ] Services created: `kubectl get svc`
- [ ] Port-forward works
- [ ] Frontend accessible via port-forward
- [ ] Backend API accessible via port-forward
- [ ] Chat feature works in Kubernetes
- [ ] Data persists after pod restart

---

## 🎯 Quick Commands Reference

### Docker Commands:
```bash
# Build images
docker build -f Dockerfile.backend -t todo-backend:latest .
docker build -f Dockerfile.frontend -t todo-frontend:latest .

# Run with Docker Compose
docker-compose up -d
docker-compose logs -f
docker-compose down

# Clean up
docker-compose down -v
docker system prune -a
```

### Kubernetes Commands:
```bash
# Minikube
minikube start --driver=docker
minikube status
minikube stop
minikube delete
eval $(minikube docker-env)

# Kubectl
kubectl get pods
kubectl get svc
kubectl get secrets
kubectl logs <pod-name>
kubectl describe pod <pod-name>
kubectl delete pod <pod-name>

# Helm
helm install todo-app ./helm-chart
helm list
helm upgrade todo-app ./helm-chart
helm uninstall todo-app

# Port Forwarding
kubectl port-forward svc/todo-app-frontend-service 3000:3000
kubectl port-forward svc/todo-app-backend-service 8000:8000
```

---

## 🚀 Next Steps

1. **Scale the Application:**
   ```bash
   kubectl scale deployment todo-app-backend --replicas=3
   kubectl scale deployment todo-app-frontend --replicas=3
   ```

2. **Enable Autoscaling:**
   ```bash
   helm upgrade todo-app ./helm-chart --set autoscaling.enabled=true
   ```

3. **Add Ingress:**
   ```bash
   helm upgrade todo-app ./helm-chart --set ingress.enabled=true
   ```

4. **Monitor with Kubernetes Dashboard:**
   ```bash
   minikube dashboard
   ```

5. **Deploy to Cloud:**
   - AWS EKS
   - Google GKE
   - Azure AKS

---

## 📚 Additional Resources

- **Docker Documentation**: https://docs.docker.com/
- **Kubernetes Documentation**: https://kubernetes.io/docs/
- **Helm Documentation**: https://helm.sh/docs/
- **Minikube Documentation**: https://minikube.sigs.k8s.io/docs/

---

**Ready to deploy?** Start with Docker Compose for quick testing, then move to Kubernetes for production-ready deployment! 🎉

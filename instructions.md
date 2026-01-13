# 🛠️ Kubernetes & Docker Deployment Instructions

This guide provides step-by-step instructions for containerizing and deploying "The Evolution of Todo" application using Docker and Kubernetes.

---

## 🪟 For Windows Users (PowerShell)

**Your current location in PowerShell:**
```
PS \\wsl.localhost\Ubuntu\home\shafqatsarwar\Projects\2nd_hackathon-phase1-4>
```

### Quick Start - Docker Deployment

**Run these commands in PowerShell (in order):**

#### 1. Build Images (5-8 minutes total)
```powershell
# Build Backend (2-3 min)
docker build -f Dockerfile.backend -t todo-backend:latest .

# Build Frontend (3-5 min)
docker build -f Dockerfile.frontend -t todo-frontend:latest .

# Verify images
docker images
```

#### 2. Configure Environment
```powershell
# Create .env file if it doesn't exist
@"
DATABASE_URL=postgresql://postgres:postgres@db:5432/todo_db
BETTER_AUTH_SECRET=change-this-secret-in-production
OPENAI_API_KEY=your-openai-api-key-here
GITHUB_TOKEN=optional
"@ | Out-File -FilePath .env -Encoding utf8

# Edit with your actual OPENAI_API_KEY
notepad .env
```

#### 3. Start Services
```powershell
# Start all containers
docker-compose up -d

# Check status
docker-compose ps

# Test backend
curl http://localhost:8000/health

# Open application
start http://localhost:3000
```

**Access:**
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/docs

**Useful Commands:**
```powershell
docker-compose logs -f        # View logs
docker-compose down           # Stop services
docker-compose restart        # Restart services
```

---

## 🐧 For Linux/WSL Users (Bash)

### Docker Deployment

```bash
# Navigate to project
cd ~/Projects/2nd_hackathon-phase1-4

# Build images
docker build -f Dockerfile.backend -t todo-backend:latest .
docker build -f Dockerfile.frontend -t todo-frontend:latest .

# Create .env file
cat > .env << 'EOF'
DATABASE_URL=postgresql://postgres:postgres@db:5432/todo_db
BETTER_AUTH_SECRET=change-this-secret-in-production
OPENAI_API_KEY=your-openai-api-key-here
EOF

# Edit .env with your API key
nano .env

# Start services
docker-compose up -d

# Check status
docker-compose ps
curl http://localhost:8000/health
```

**Access:**
- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000


---

## ☸️ Kubernetes Deployment

### Prerequisites
- Docker Desktop with Kubernetes enabled OR Minikube
- Helm 3.x
- kubectl

### For Windows (PowerShell) or Linux/WSL (Bash)

#### Step 1: Start Minikube
```bash
# Run in WSL/Bash terminal
minikube start --driver=docker

# Configure to use Minikube's Docker
eval $(minikube docker-env)
```

#### Step 2: Build Images in Minikube
```bash
# Run in WSL/Bash terminal (after eval command above)
docker build -f Dockerfile.backend -t todo-backend:latest .
docker build -f Dockerfile.frontend -t todo-frontend:latest .
```

#### Step 3: Create Secrets
```bash
# Run in WSL/Bash or PowerShell
kubectl create secret generic todo-app-secrets \
  --from-literal=DATABASE_URL="postgresql://postgres:postgres@postgres-service:5432/todo_db" \
  --from-literal=BETTER_AUTH_SECRET="your_auth_secret" \
  --from-literal=OPENAI_API_KEY="your_openai_key" \
  --from-literal=GITHUB_TOKEN="your_github_token"
```

#### Step 4: Deploy with Helm
```bash
# Run in WSL/Bash or PowerShell
helm install todo-app ./helm-chart

# Verify deployment
kubectl get pods
kubectl get svc
```

#### Step 5: Access Application

**Option A: Port Forwarding (Recommended)**
```bash
# Terminal 1 - Frontend
kubectl port-forward svc/todo-app-frontend-service 3000:3000

# Terminal 2 - Backend
kubectl port-forward svc/todo-app-backend-service 8000:8000
```

**Option B: Management Script**
```bash
# Run in WSL/Bash
uv run python manage_phase_4.py tunnel
```

**Access:**
- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000/docs

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
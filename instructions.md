# 🛠️ Kubernetes & Docker Deployment Instructions

## 📦 Docker Deployment (Local Containerization)

### 1. Build Docker Images
Ensure you are in the project root.

```bash
# Backend
docker build -f Dockerfile.backend -t todo-backend:latest .

# Frontend
docker build -f Dockerfile.frontend -t todo-frontend:latest .
```

### 2. Run with Docker Compose
Use `docker-compose` for a quick local test of the containerized stack.

```bash
docker-compose up -d
```
*Access frontend at http://localhost:3000*

---

## ☸️ Kubernetes Deployment (Phase IV Core)

### 1. Setup Minikube (If not using Docker Desktop K8s)
```bash
minikube start --driver=docker
eval $(minikube docker-env) # Use Docker daemon inside Minikube
```

### 2. Secrets Management
Create a secret for sensitive environment variables.
*Replace values with your actual credentials.*

```bash
kubectl create secret generic todo-secrets \
  --from-literal=DATABASE_URL="postgresql://..." \
  --from-literal=BETTER_AUTH_SECRET="your_secret" \
  --from-literal=OPENAI_API_KEY="sk-..." \
  --from-literal=NEXT_PUBLIC_BACKEND_URL="http://todo-backend:8000" \
  --from-literal=NEXT_PUBLIC_BETTER_AUTH_URL="http://todo-frontend:3000"
```

### 3. Deploy via Helm
```bash
cd helm-chart
# Install
helm install phase4-todo .

# Upgrade (after changes)
helm upgrade phase4-todo .

# Uninstall
helm uninstall phase4-todo
```

### 4. Tunneling / Port Forwarding (Accessing the App)

**Option A: Recommended (Management Script)**
The easiest way to expose both services is using our management script:
```bash
uv run python manage_phase_4.py tunnel
```
*   Keeps both frontend (3000) and backend (8000) open.
*   Access app at: http://localhost:3000

**Option B: Manual Port Forwarding**
If you prefer manual control:
```bash
# Terminal 1 (Frontend)
kubectl port-forward svc/todo-app-frontend-service 3000:3000

# Terminal 2 (Backend)
kubectl port-forward svc/todo-app-backend-service 8000:8000
```

**Option C: Minikube Tunnel (Advanced)**
For LoadBalancer services (requires root/sudo):
```bash
sudo minikube tunnel
```

---

## 🤖 AI Operations (`kubectl-ai` & `kagent`)

### Using `kubectl-ai`
Generate and apply manifests or perform actions using natural language.

```bash
# Example: Create a new deployment
kubectl-ai "create a nginx deployment with 2 replicas"

# Example: Scale our app
kubectl-ai "scale deployment todo-backend to 5 replicas"
```

### Using `kagent`
Analyze and optimize the cluster.

```bash
# Diagnose issues
kagent "why is the frontend pod crashing?"

# Optimize
kagent "analyze resources and suggest limits"
```

## 🧪 Verification & Testing
1. **Persistence Test**: Delete a backend pod (`kubectl delete pod <backend-pod>`). It should recreate. Check if data persists in the app.
2. **Connectivity**: Ensure frontend can talk to backend via the K8s service DNS.
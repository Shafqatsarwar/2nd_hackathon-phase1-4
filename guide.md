# ☸️ Phase IV: Local Kubernetes Deployment

## 🎯 Objective
Prove the system is **cloud-native** by deploying the AI-powered Todo application to a local Kubernetes cluster (Minikube). The system must be resilient, scalable, and managed via declarative infrastructure (Helm Charts).

## 📜 Constitutional Requirements
- **Immutable Containers**: Docker images must be read-only at runtime.
- **Configuration**: All config via Environment Variables (no hardcoding).
- **Declarative Infrastructure**: Use Helm Charts for all resources.
- **Zero Data Loss**: System must survive pod restarts without losing data.
- **AI Operations**: Use `kubectl-ai` and `kagent` for cluster management.

## 🏗️ Architecture
- **Frontend**: Next.js (Dockerized)
- **Backend**: FastAPI (Dockerized)
- **Database**: External (Neon) or In-cluster (StatefulSet - *if strictly local, but we use Neon for continuity*)
- ** Orchestration**: Kubernetes (Minikube)
- **Packaging**: Helm 3
- **AI Ops**: kubectl-ai, kagent

## 🛠️ Prerequisites
1.  **Docker Desktop** (with Kubernetes enabled) OR **Minikube**
2.  **Helm 3.x**
3.  **kubectl**
4.  **kubectl-ai** (plugin)
5.  **kagent** (tool)
6.  Python 3.12+ & Node.js 18+

## 🚀 Quick Start
### 1. Build Containers
```bash
docker build -f Dockerfile.backend -t todo-backend:latest .
docker build -f Dockerfile.frontend -t todo-frontend:latest .
```

### 2. Deploy to Kubernetes
```bash
cd helm-chart
helm install todo-app . --values values.yaml
```

### 3. Verify Deployment
```bash
kubectl get pods
# Wait for Running status
```

### 4. AI-Assisted Management
```bash
kubectl-ai "scale the frontend to 3 replicas"
kagent "check cluster health and suggest optimizations"
```

## 📂 Project Structure for Phase IV
- `Dockerfile.backend`: Backend container spec
- `Dockerfile.frontend`: Frontend container spec
- `helm-chart/`: Helm chart definitions
- `scripts/`: Utility scripts for deployment
- `.claude/skills/`: AI agent skills for K8s management

## 📝 Success Criteria Checklist
- [ ] Application runs on Minikube/K8s
- [ ] No hardcoded URLs in code
- [ ] Env vars inject configuration
- [ ] Pods restart with data persistence
- [ ] `kubectl-ai` works for commands

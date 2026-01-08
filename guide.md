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
- **MCP**: GitHub integration for issue management.

## 🛠️ Prerequisites
1.  **Docker Desktop** (with Kubernetes enabled) OR **Minikube**
2.  **Helm 3.x**
3.  **kubectl**
4.  **kubectl-ai** (plugin)
5.  **kagent** (tool)
6.  Python 3.12+ & Node.js 18+

## 🚀 Quick Start (Local Development)

### 1. Run Locally (No Docker)
To test the application logic before containerization:

**Backend:**
```bash
uv run uvicorn src.backend.main:app --host 0.0.0.0 --port 8000 --reload --env-file .env
```
*Health Check: http://localhost:8000/health*

**Frontend:**
```bash
cd src/frontend
npm run dev
```
*Access App: http://localhost:3000*

### 2. Run with Docker Compose
```bash
docker-compose up -d
```

### 3. Deploy to Kubernetes
```bash
cd helm-chart
helm install todo-app . --values values.yaml
```

## 🛠️ Phase IV Management Script
We have provided a unified Python script to manage the entire deployment lifecycle.

**1. Check Status**
Verify your system has all required tools (Docker, Minikube, Helm, Kubectl).
```bash
uv run python manage_phase_4.py status
```

**2. One-Click Deployment**
Builds images, configures secrets from `.env`, and deploys via Helm.
```bash
uv run python manage_phase_4.py deploy
```

**3. Tunneling (Port Forwarding)**
Expose the Kubernetes services to `localhost:3000` and `localhost:8000`.
```bash
uv run python manage_phase_4.py tunnel
```

## 🛠️ Testing GitHub MCP Tool
The GitHub MCP Tool allows the AI agent to interact with your repository (create issues, list PRs, etc.).

**Prerequisites:**
- `GITHUB_TOKEN`, `GITHUB_OWNER`, `GITHUB_REPO` must be set in `.env`.

**Run Verification Script:**
We have provided a script to verify the GitHub connection:
```bash
uv run python test_github_mcp.py
```

**What it tests:**
1.  Connection to GitHub API.
2.  Fetching repository metadata.
3.  Listing open issues.

## 📂 Project Structure for Phase IV
- `Dockerfile.backend`: Backend container spec
- `Dockerfile.frontend`: Frontend container spec
- `helm-chart/`: Helm chart definitions
- `scripts/`: Utility scripts for deployment
- `.claude/skills/`: AI agent skills for K8s management
- `src/backend/mcp_server/`: MCP Tool implementations

## 📝 Success Criteria Checklist
- [ ] Application runs on Minikube/K8s
- [ ] No hardcoded URLs in code
- [ ] Env vars inject configuration
- [ ] Pods restart with data persistence
- [ ] `kubectl-ai` works for commands
- [ ] GitHub MCP tool verifies successfully

## 📚 submission_guide.md
See the newly created [submission_guide.md](./submission_guide.md) for advanced instructions on:
- Adding Helm Dependencies (Redis, etc.)
- Docker Debugging
- Creating your Demo Video for Judges

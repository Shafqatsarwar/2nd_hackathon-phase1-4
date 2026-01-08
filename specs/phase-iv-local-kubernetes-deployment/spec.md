# Specification: Phase IV - Local Kubernetes Deployment

## 1. Objective
Prove that the "Evolution of Todo" application is **cloud-native** by deploying it to a local Kubernetes cluster (Minikube). Moving beyond simple local processes, the system will leverage container orchestration to demonstrate resilience, scalability, and declarative infrastructure management.

## 2. Constitutional Requirements (Compliance)
This specification adheres strictly to the `Hackathon II - Phase IV` constitution:
*   **Immutable Containers**: Application artifacts are packaged as read-only Docker images (`todo-frontend:latest`, `todo-backend:latest`).
*   **Environment-Based Config**: All dynamic values (Database URL, API Keys, Secrets) are injected via Kubernetes Secrets and ConfigMaps, not hardcoded.
*   **Declarative Infrastructure**: All resources (Deployments, Services, Secrets) are defined in Helm Charts.
*   **Zero Data Loss**: The system uses persistent storage mechanics (External Neon DB) to ensure data survives pod restarts.
*   **AI Operations**: The deployment leverages `kubectl-ai` for ad-hoc management and `kagent` for optimization.

## 3. Scope
### Included Features
1.  **Frontend Containerization**: Next.js App Router application packaged in Docker.
2.  **Backend Containerization**: FastAPI application packaged in Docker.
3.  **Helm Chart**: A unified chart `todo-app` managing both tiers.
4.  **Local Cluster**: Deployment to Minikube with Docker driver.
5.  **GitHub MCP Integration**: Verification that the AI Agent can interact with GitHub for issue tracking.
6.  **Tunneling**: Automated script to expose cluster services to `localhost`.

### Excluded
*   **Cloud Hosting**: This phase is strictly *Local* Kubernetes (Minikube).
*   **Complex Ingress**: We are using Port-Forwarding/Tunneling for simplicity in the local environment, avoiding complex Ingress Controller setup unless necessary.

## 4. Architecture
*   **Container Runtime**: Docker
*   **Orchestrator**: Kubernetes (Minikube)
*   **Database**: Neon (SaaS Postgres) - *Chosen for continuity from Phase II/III*.
*   **Communication**: 
    *   Host -> Frontend (via Port Forward 3000)
    *   Frontend Pod -> Backend Service (ClusterDNS `todo-app-backend-service:8000`)
    *   Backend Pod -> Database (External SSL connection)

## 5. Success Criteria
1.  **Deployment**: `uv run python manage_phase_4.py deploy` completes with "Deployment Complete!".
2.  **Connectivity**: `localhost:3000` loads the Todo UI.
3.  **Functionality**: Creating a task persists it to the Neon DB.
4.  **Resilience**: Deleting a backend pod results in automatic recreation (Self-healing).
5.  **Clean Code**: Repository contains `Dockerfile`s, `helm-chart/`, and automation scripts.

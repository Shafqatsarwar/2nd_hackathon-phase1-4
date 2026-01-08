# Implementation Plan: Phase IV - Local Kubernetes Deployment

## 1. Technical Strategy
We will transition from a "Process-based" architecture (running `npm start` / `uvicorn` manually) to a "Container-based" architecture. This involves three distinct layers of work:

1.  **Container Layer**: Defining the "Recipe" for our applications (Dockerfiles).
2.  **Orchestration Layer**: Defining how these containers run, talk, and scale (Helm).
3.  **Automation Layer**: Scripting the glue code to make it easy for developers (Python Management Script).

## 2. Component Design

### A. Docker Containers
*   **Backend (`Dockerfile.backend`)**:
    *   Base: `python:3.12-slim`
    *   Optimization: Multi-stage build not strictly necessary for Python but recommended for size.
    *   Expose: 8000
    *   Command: `uvicorn`
*   **Frontend (`Dockerfile.frontend`)**:
    *   Base: `node:18-alpine`
    *   Optimization: Multi-stage build (Builder -> Runner) to keep image small.
    *   Expose: 3000
    *   Command: `npm start`

### B. Helm Chart Structure
*   `Chart.yaml`: Metadata.
*   `values.yaml`: Default configuration (image tags, replicas).
*   `templates/backend-deployment.yaml`: Defines the FastAPI pods.
*   `templates/frontend-deployment.yaml`: Defines the Next.js pods.
*   `templates/*-service.yaml`: Internal ClusterIP services for networking.
*   `templates/secrets.yaml`: (Managed via script injection for security).

### C. Management Automation
*   **Script**: `manage_phase_4.py`
*   **Responsibility**:
    1.  Check Minikube status.
    2.  Build both Docker images.
    3.  Load images into Minikube cache (critical step often missed).
    4.  Create K8s Secrets from local `.env`.
    5.  Run `helm install`/`upgrade`.
    6.  Run `kubectl port-forward` for access.

## 3. Operational Steps (Execution Order)

### Step 1: Containerization
*   Draft `Dockerfile.backend` and `Dockerfile.frontend`.
*   Verify local build (`docker build ...`).
*   Verify local run (`docker run ...`).

### Step 2: Infrastructure Definition (Helm)
*   Initialize helm chart.
*   Draft Deployment and Service manifests.
*   Ensure environment variables map correctly to Secret keys.

### Step 3: Deployment Pipeline
*   Implement `manage_phase_4.py`.
*   Test deployment against Minikube.
*   Debug networking (Frontend talking to Backend URL).

### Step 4: Verification & MCP
*   Test GitHub MCP tool integration.
*   Record demo video.

## 4. Risks & Mitigations
*   **Risk**: Frontend can't reach Backend.
    *   *Mitigation*: Use K8s Service DNS (`http://todo-app-backend-service:8000`) instead of localhost.
*   **Risk**: Database connection fails from within Cluster.
    *   *Mitigation*: Ensure Neon DB supports SSL and the connection string is passed correctly via Secrets.
*   **Risk**: "ImagePullBackOff" errors.
    *   *Mitigation*: Ensure `imagePullPolicy: IfNotPresent` and images are built inside Minikube's Docker daemon.

# Tasks: Phase IV - Local Kubernetes Deployment

## Task 1: Containerization ✅
**Description**: Create optimized Dockerfiles for both services.
**Files**: `Dockerfile.backend`, `Dockerfile.frontend`, `.dockerignore`
**Criteria**:
*   [x] `docker build` succeeds for both.
*   [x] Images are under 500MB (Frontend) / 300MB (Backend optimized/slim).
*   [x] No secrets are baked into the image.

## Task 2: Helm Chart Development ✅
**Description**: Create a unified Helm chart for the application stack.
**Files**: `helm-chart/Chart.yaml`, `values.yaml`, `templates/*.yaml`
**Criteria**:
*   [x] `helm lint` passes without errors.
*   [x] Backend Deployment includes Liveness/Readiness probes.
*   [x] Frontend Deployment includes env var for Backend URL.
*   [x] Services expose ports 3000 and 8000.

## Task 3: Automation Scripting ✅
**Description**: Create a Python script to manage the complex deployment life-cycle locally.
**Files**: `manage_phase_4.py`, `scripts/deploy_to_k8s.py`
**Criteria**:
*   [x] Script verifies tool installation (Minikube, etc.).
*   [x] Script injects `.env` variables into K8s Secrets securely.
*   [x] Script handles "Update" vs "Install" logic gracefully.

## Task 4: GitHub MCP Integration ✅
**Description**: Verify the AI Agent's ability to use GitHub tools.
**Files**: `src/backend/mcp_server/github_tools.py`, `test_github_mcp.py`
**Criteria**:
*   [x] Agent can authenticating using `GITHUB_TOKEN`.
*   [x] Agent can list issues from the repo.
*   [x] `test_github_mcp.py` returns success.

## Task 5: Final Verification & Documentation 🔄
**Description**: Test the end-to-end flow and document for judges.
**Files**: `guide.md`, `submission_guide.md`, `specs/*.md`
**Criteria**:
*   [x] Full deployment works on a fresh Minikube start.
*   [x] Application is accessible via `localhost`.
*   [x] Documentation explains exactly how to run it.
*   [ ] Demo Video recorded.

## Task 6: Submission Packaging ⏳
**Description**: Prepare the repository for final submission.
**Steps**:
1.  Run `pip freeze > requirements.txt`.
2.  Clean up any `tmp` files or logs.
3.  Commit all changes to Git.
4.  Push to remote repository.
5.  Submit URL and Video link.

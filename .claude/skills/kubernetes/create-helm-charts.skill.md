# Create Helm Charts Skill

## Purpose
Create Helm charts for deploying the containerized applications to Kubernetes as required by Phase IV.

## Context
Based on the constitution for Phase IV - Local Kubernetes Deployment:
- Infrastructure defined declaratively
- Multi-replica readiness
- Local cluster deployment
- Kubernetes is source of truth

## Required Actions
1. Create Helm chart structure for the frontend application
2. Create Helm chart structure for the backend application
3. Define Kubernetes resources (Deployments, Services, ConfigMaps, etc.)
4. Configure for multi-replica deployments
5. Ensure proper service discovery between components
6. Include necessary RBAC configurations if needed

## Files to Create
- `helm-charts/todo-frontend/Chart.yaml`
- `helm-charts/todo-frontend/values.yaml`
- `helm-charts/todo-frontend/templates/deployment.yaml`
- `helm-charts/todo-frontend/templates/service.yaml`
- `helm-charts/todo-backend/Chart.yaml`
- `helm-charts/todo-backend/values.yaml`
- `helm-charts/todo-backend/templates/deployment.yaml`
- `helm-charts/todo-backend/templates/service.yaml`
- Additional templates as needed (ConfigMaps, Ingress, etc.)

## Validation Criteria
- Helm charts install successfully on a local Kubernetes cluster (Minikube)
- Applications are accessible after deployment
- Multi-replica deployments work correctly
- Proper inter-service communication is established
- All required resources are defined declaratively

## Constraints
- Follow Helm best practices
- Use configurable values for different environments
- Ensure proper resource requests/limits
- Include health checks and readiness probes
- Maintain security best practices

## Reference
- Phase IV Constitution: D:\Panaverse\project\2nd_hackathon-phase1-4\.specify\memory\📜 CONSTITUTION-Hackathon II - Phase IV — Local Kubernetes Deployment.md
- Kubernetes documentation for best practices
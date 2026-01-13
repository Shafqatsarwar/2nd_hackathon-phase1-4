# Deploy to Kubernetes (Phase IV) Skill

## Description
This skill automates the deployment of the Todo Evolution application to a local Kubernetes cluster using Minikube. It handles containerization, Helm chart creation, and deployment orchestration.

## Parameters
- `environment`: Target environment (local/minikube/dev/prod) [default: local]
- `namespace`: Kubernetes namespace for deployment [default: todo-app]
- `image_tag`: Docker image tag to deploy [default: latest]
- `dry_run`: Whether to perform a dry run without actual deployment [default: false]

## Functions

### 1. setup_minikube_cluster
Sets up a local Minikube cluster with required resources and configurations.

### 2. build_docker_images
Builds Docker images for both frontend and backend services.

### 3. create_helm_charts
Generates Helm charts for the Todo Evolution application with configurable parameters.

### 4. deploy_to_k8s
Deploys the application to the Kubernetes cluster using Helm charts.

### 5. verify_deployment
Checks the status of deployed services and verifies they are running correctly.

### 6. update_deployment
Updates an existing deployment with new image versions or configuration changes.

### 7. rollback_deployment
Rolls back to a previous stable deployment version.

### 8. scale_services
Scales frontend and backend services based on demand.

## Execution Flow
1. Validate prerequisites (Docker, kubectl, minikube, helm)
2. Build Docker images for frontend and backend
3. Generate Helm charts with environment-specific configurations
4. Deploy to Kubernetes cluster
5. Verify deployment status
6. Perform health checks on deployed services

## Requirements
- Docker daemon running
- kubectl configured
- Minikube cluster running
- Helm installed
- Internet connectivity for pulling base images

## Examples
```
deploy-to-k8s --environment=minikube --namespace=todo-app
deploy-to-k8s --environment=dev --image_tag=v1.2.3 --dry_run=true
deploy-to-k8s --namespace=staging --scale_backend=3 --scale_frontend=2
```

## Output
- Deployment status and service endpoints
- Pod status and resource utilization
- Configuration files used for deployment
- Rollback procedures if deployment fails
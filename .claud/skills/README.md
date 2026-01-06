# Phase IV Kubernetes Deployment Skills

This directory contains the skills needed to complete Phase IV of the "Evolution of Todo" project: Local Kubernetes Deployment.

## Skills Overview

### 1. Dockerize Applications (`dockerize-applications.skill.md`)
Dockerizes the frontend and backend applications following immutability principles and environment-based configuration.

### 2. Create Helm Charts (`create-helm-charts.skill.md`)
Creates declarative Kubernetes deployment manifests using Helm charts for consistent, repeatable deployments.

### 3. Setup Minikube (`setup-minikube.skill.md`)
Sets up a local Kubernetes cluster for development and testing of the deployment.

### 4. Use kubectl-ai and kagent (`use-kubectl-ai-kagent.skill.md`)
Leverages AI-assisted Kubernetes operations for intelligent cluster management and optimization.

### 5. Use Docker AI Agent (Gordon) (`use-docker-ai-gordon.skill.md`)
Utilizes AI-assisted Docker operations for optimized container creation and management.

### 6. Deploy to Kubernetes (`deploy-to-kubernetes.skill.md`)
Executes the complete deployment process and validates the cloud-native application.

## Execution Order

To complete Phase IV, execute the skills in this sequence:

1. `dockerize-applications.skill.md` - Containerize the applications
2. `use-docker-ai-gordon.skill.md` - Optimize Docker operations with AI
3. `create-helm-charts.skill.md` - Prepare declarative deployment manifests
4. `setup-minikube.skill.md` - Establish local Kubernetes environment
5. `use-kubectl-ai-kagent.skill.md` - Configure AI-assisted Kubernetes operations
6. `deploy-to-kubernetes.skill.md` - Execute and validate the deployment

## Success Criteria

Following these skills will satisfy the Phase IV requirements:
- ✅ Prove the system is cloud-native, not cloud-hosted
- ✅ Containers are immutable
- ✅ Config via environment variables
- ✅ Infrastructure defined declaratively
- ✅ Dockerized frontend & backend
- ✅ Helm charts for deployment
- ✅ Multi-replica readiness
- ✅ Local cluster deployment
- ✅ No hardcoded service URLs
- ✅ No local filesystem dependencies
- ✅ Kubernetes is source of truth
- ✅ System survives pod restarts with zero data loss

## Reference Documents

- [Phase IV Constitution](../../.specify/memory/📜 CONSTITUTION-Hackathon II - Phase IV — Local Kubernetes Deployment.md)
- [Main Project Spec](../../.specify/memory/Hackathon II - Todo Spec-Driven Development.md)
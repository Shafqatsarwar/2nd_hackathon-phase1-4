# Deploy to Kubernetes Skill

## Purpose
Deploy the complete application to the local Kubernetes cluster using Helm charts and verify the deployment as required by Phase IV.

## Context
Based on the constitution for Phase IV - Local Kubernetes Deployment:
- Prove the system is cloud-native, not cloud-hosted
- Multi-replica readiness
- Local cluster deployment
- System survives pod restarts with zero data loss
- Kubernetes is source of truth

## Required Actions
1. Package the Docker images for deployment
2. Install the Helm charts to the Minikube cluster
3. Configure the database connection for Kubernetes
4. Set up proper service discovery between frontend and backend
5. Verify application functionality after deployment
6. Test pod restart resilience
7. Validate data persistence

## Tasks
1. Build and push Docker images (or use local images for Minikube)
2. Install Helm charts with appropriate configurations
3. Configure database connectivity (Neon DB or local Postgres in K8s)
4. Set up environment variables and secrets
5. Verify application functionality through UI and API
6. Test scaling of deployments
7. Test pod restart scenarios to ensure data persistence
8. Document the deployment process and troubleshooting steps

## Validation Criteria
- Application deploys successfully to Kubernetes
- Frontend and backend communicate properly
- Database connectivity works in the cluster
- Multi-replica deployments function correctly
- Pod restarts don't cause data loss
- Applications remain accessible after restarts
- Health checks pass consistently

## Constraints
- Maintain data integrity during deployments
- Ensure zero-downtime deployment where possible
- Follow security best practices for secrets management
- Use proper resource requests and limits
- Implement appropriate health checks

## Files to Create/Modify
- `scripts/deploy-to-k8s.sh` (deployment automation script)
- `k8s/secrets.yaml` (if needed for secrets management)
- `k8s/ingress.yaml` (for external access)
- `docs/deployment-guide.md` (comprehensive deployment documentation)

## Testing Requirements
- Verify all 5 Basic Level features work after deployment
- Test multi-user functionality if applicable
- Validate authentication works in the Kubernetes environment
- Confirm data persistence across pod restarts

## Reference
- Phase IV Constitution: D:\Panaverse\project\2nd_hackathon-phase1-4\.specify\memory\📜 CONSTITUTION-Hackathon II - Phase IV — Local Kubernetes Deployment.md
- Existing application functionality from previous phases
- Helm chart configurations created in previous steps
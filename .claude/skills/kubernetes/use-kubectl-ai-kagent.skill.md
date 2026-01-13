# Use kubectl-ai and kagent Skill

## Purpose
Use kubectl-ai and kagent for AI-assisted Kubernetes operations as required by Phase IV.

## Context
Based on the constitution and requirements for Phase IV - Local Kubernetes Deployment:
- Use kubectl-ai and kagent for AI-assisted Kubernetes operations
- Deploy on Minikube locally
- Multi-replica readiness
- System survives pod restarts with zero data loss

## Required Actions
1. Install and configure kubectl-ai
2. Install and configure kagent
3. Use kubectl-ai for intelligent Kubernetes operations
4. Use kagent for cluster analysis and optimization
5. Document common kubectl-ai and kagent commands for the project

## Tasks
1. Install kubectl-ai plugin
2. Install kagent
3. Use kubectl-ai for common operations:
   - Deploy applications with appropriate replica counts
   - Scale applications based on load requirements
   - Troubleshoot failing pods and deployments
   - Check cluster health and resource utilization
4. Use kagent for:
   - Cluster health analysis
   - Resource allocation optimization
   - Performance monitoring
5. Create documentation for team members on using these tools

## Examples of kubectl-ai Commands
- `kubectl-ai "deploy the todo frontend with 2 replicas"`
- `kubectl-ai "scale the backend to handle more load"`
- `kubectl-ai "check why the pods are failing"`
- `kubectl-ai "show me the resource usage of my deployments"`

## Examples of kagent Commands
- `kagent "analyze the cluster health"`
- `kagent "optimize resource allocation"`
- `kagent "show me potential security issues"`

## Files to Create/Modify
- `docs/kubectl-ai-usage.md` (Documentation on using kubectl-ai)
- `docs/kagent-usage.md` (Documentation on using kagent)
- `scripts/ai-k8s-operations.sh` (optional automation script)

## Validation Criteria
- Both kubectl-ai and kagent are successfully installed
- Basic operations work correctly with the Minikube cluster
- AI-assisted commands produce expected results
- Documentation is clear and comprehensive

## Constraints
- Follow best practices for AI-assisted operations
- Ensure security and privacy compliance
- Document limitations and appropriate use cases
- Maintain human oversight for critical operations

## Reference
- Phase IV Constitution: D:\Panaverse\project\2nd_hackathon-phase1-4\.specify\memory\📜 CONSTITUTION-Hackathon II - Phase IV — Local Kubernetes Deployment.md
- kubectl-ai documentation
- kagent documentation
# Kubernetes Configuration (Phase IV) Skill

## Description
This skill generates Kubernetes manifests and Helm charts for the Todo Evolution application. It handles service configuration, ingress setup, persistent storage, and environment-specific deployments.

## Parameters
- `environment`: Target environment (dev/staging/prod/minikube) [default: dev]
- `namespace`: Kubernetes namespace for resources [default: todo-app]
- `replica_count`: Number of replicas for each service [default: 1]
- `resources`: Resource limits and requests (cpu/memory) [default: auto]
- `ingress_enabled`: Whether to create ingress resources [default: true]
- `database_type`: Database type (postgres/sqlite) [default: postgres]
- `enable_monitoring`: Whether to enable monitoring resources [default: false]

## Functions

### 1. generate_deployment_manifests
Creates Kubernetes Deployment manifests for frontend and backend services.

### 2. generate_service_manifests
Creates Kubernetes Service manifests for internal service communication.

### 3. generate_ingress_config
Creates Ingress resources for external access to the application.

### 4. generate_configmaps_secrets
Generates ConfigMaps and Secrets for application configuration.

### 5. generate_persistent_storage
Creates PersistentVolume and PersistentVolumeClaim for data storage.

### 6. generate_helm_charts
Packages all manifests into Helm charts with configurable parameters.

### 7. generate_network_policies
Creates NetworkPolicy resources for service isolation.

### 8. generate_resource_quotas
Creates ResourceQuota and LimitRange for namespace resource management.

## Execution Flow
1. Analyze application architecture and dependencies
2. Generate base Kubernetes manifests
3. Configure environment-specific parameters
4. Create Helm chart structure with values files
5. Validate generated manifests for correctness
6. Package everything into deployable Helm charts

## Requirements
- Application source code available
- Environment-specific configuration values
- Understanding of application dependencies
- Kubernetes best practices knowledge

## Examples
```
k8s-configuration --environment=prod --replica_count=3 --enable_monitoring=true
k8s-configuration --namespace=todo-production --database_type=postgres
k8s-configuration --ingress_enabled=false --resources="cpu:500m,memory:1Gi"
```

## Output
- Kubernetes manifest files
- Helm chart directory structure
- Environment-specific values files
- Deployment validation reports
- Resource utilization estimates
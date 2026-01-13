# Dockerize Application (Phase IV) Skill

## Description
This skill creates Docker images for the Todo Evolution application's frontend and backend services. It handles multi-stage builds, image optimization, and container configuration for Kubernetes deployment.

## Parameters
- `service`: Specific service to dockerize (frontend/backend/both) [default: both]
- `build_context`: Path to the build context [default: .]
- `dockerfile_path`: Path to custom Dockerfile [default: auto-detect]
- `image_prefix`: Prefix for Docker image names [default: todo-evolution]
- `target_platform`: Target platform for the image [default: linux/amd64]
- `push_registry`: Whether to push images to registry [default: false]

## Functions

### 1. create_dockerfiles
Generates optimized Dockerfiles for both frontend and backend services using multi-stage builds.

### 2. build_frontend_image
Builds the Docker image for the Next.js frontend application.

### 3. build_backend_image
Builds the Docker image for the FastAPI backend service.

### 4. scan_image_security
Performs security scanning on built images to identify vulnerabilities.

### 5. optimize_image_size
Applies various optimization techniques to reduce image size.

### 6. push_to_registry
Pushes built images to specified container registry.

### 7. generate_multiarch_manifest
Creates multi-architecture image manifests for different platforms.

### 8. validate_image
Validates the built image for proper functionality and security.

## Execution Flow
1. Analyze project structure and identify service boundaries
2. Generate optimized Dockerfiles for each service
3. Build Docker images with appropriate caching strategies
4. Perform security scanning and optimization
5. Optionally push images to registry
6. Generate deployment manifests for Kubernetes

## Requirements
- Docker daemon running
- Dockerfile templates (if custom)
- Access to base images (Node.js, Python)
- Internet connectivity for pulling base images

## Examples
```
dockerize-application --service=frontend --image_prefix=todo-fe
dockerize-application --target_platform=linux/arm64 --push_registry=true
dockerize-application --service=backend --build_context=./src/backend
```

## Output
- Built Docker images with tags
- Security scan reports
- Image size optimization reports
- Docker Compose files for local testing
- Kubernetes deployment manifests
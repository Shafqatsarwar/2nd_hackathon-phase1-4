# Dockerize Applications Skill

## Purpose
Dockerize the frontend and backend applications for Kubernetes deployment as required by Phase IV.

## Context
Based on the constitution for Phase IV - Local Kubernetes Deployment:
- Containers are immutable
- Config via environment variables
- No hardcoded service URLs
- No local filesystem dependencies

## Required Actions
1. Create Dockerfile for the frontend application
2. Create Dockerfile for the backend application
3. Ensure applications are configured via environment variables
4. Remove any hardcoded service URLs
5. Ensure no local filesystem dependencies

## Files to Create/Modify
- `Dockerfile.frontend` or `frontend/Dockerfile`
- `Dockerfile.backend` or `backend/Dockerfile`
- Update environment configuration files if needed

## Validation Criteria
- Both applications build successfully in Docker containers
- Applications can be configured via environment variables
- No hardcoded URLs in the containerized applications
- Applications can run without local filesystem dependencies

## Constraints
- Follow Docker best practices (multi-stage builds, minimal base images)
- Ensure containers are immutable (no runtime modifications)
- Use environment variables for all configuration
- Maintain the existing application functionality

## Reference
- Phase IV Constitution: D:\Panaverse\project\2nd_hackathon-phase1-4\.specify\memory\📜 CONSTITUTION-Hackathon II - Phase IV — Local Kubernetes Deployment.md
- Existing application structure in src/, api/, and frontend/ directories
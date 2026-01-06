# Use Docker AI Agent (Gordon) Skill

## Purpose
Use Docker AI Agent (Gordon) for AI-assisted Docker operations as required by Phase IV.

## Context
Based on the constitution and requirements for Phase IV - Local Kubernetes Deployment:
- Containerize frontend and backend applications (Use Gordon)
- Use Docker AI Agent (Gordon) for AI-assisted Docker operations
- If Docker AI is unavailable, use standard Docker CLI commands

## Required Actions
1. Verify Docker AI Agent (Gordon) availability and setup
2. Use Gordon for intelligent Docker operations
3. Create Dockerfiles with AI assistance if needed
4. Build and optimize Docker images with AI assistance
5. Document Gordon capabilities and usage patterns

## Tasks
1. Check Docker Desktop version and enable Gordon (Beta features)
2. Test Gordon capabilities with: `docker ai "What can you do?"`
3. Use Gordon for Docker operations:
   - Create optimized Dockerfiles for frontend and backend
   - Build efficient multi-stage Docker images
   - Optimize image sizes and security
   - Troubleshoot Docker build issues
4. Document Gordon commands and best practices
5. Create fallback procedures if Gordon is unavailable

## Examples of Gordon Commands
- `docker ai "Create a Dockerfile for a Next.js application"`
- `docker ai "Optimize this Dockerfile for smaller size"`
- `docker ai "Fix this Docker build error"`
- `docker ai "Create a multi-stage build for a Python FastAPI app"`

## Files to Create/Modify
- `docs/docker-ai-gordon-usage.md` (Documentation on using Gordon)
- Update existing Dockerfiles if needed based on Gordon's suggestions
- `scripts/docker-ai-operations.sh` (optional automation script)

## Validation Criteria
- Gordon is properly configured and accessible
- AI-assisted Docker operations work correctly
- Docker images are optimized and functional
- Documentation is clear and comprehensive
- Fallback procedures are documented and tested

## Constraints
- Ensure compatibility with existing application structure
- Follow Docker security best practices
- Maintain image efficiency and security
- Document limitations of AI-assisted Docker operations
- Have manual alternatives ready if Gordon is unavailable

## Reference
- Phase IV Constitution: D:\Panaverse\project\2nd_hackathon-phase1-4\.specify\memory\📜 CONSTITUTION-Hackathon II - Phase IV — Local Kubernetes Deployment.md
- Docker AI Agent (Gordon) documentation
- Existing application structure from previous phases
# Phase IV: Docker, Kubernetes, and GitHub MCP Setup Instructions

This document provides comprehensive instructions for setting up Docker, Kubernetes, and GitHub MCP integration for the Phase IV deployment of the "Evolution of Todo" project.

## Section 1: Docker and Kubernetes Setup

### Prerequisites

- Docker Desktop or Docker Engine installed
- Minikube installed
- kubectl installed
- Helm installed
- Node.js 18+ installed
- Python 3.12+ installed

### Docker Setup

#### 1. Build Docker Images

First, build the Docker images for both frontend and backend:

```bash
# Build backend image
docker build -f Dockerfile.backend -t todo-backend:latest .

# Build frontend image
docker build -f Dockerfile.frontend -t todo-frontend:latest .
```

#### 2. Test Docker Images Locally

You can test the Docker images using docker-compose:

```bash
# Start the full application stack
docker-compose up --build

# Access the application:
# - Frontend: http://localhost:3000
# - Backend: http://localhost:8000
# - Backend API docs: http://localhost:8000/docs
```

### Kubernetes Setup

#### 1. Start Minikube

```bash
# Start Minikube cluster
minikube start

# Verify cluster is running
kubectl cluster-info
```

#### 2. Install Helm Chart

```bash
# Navigate to the helm chart directory
cd helm-chart

# Install the Helm chart
helm install todo-app . --set backend.image.tag=latest --set frontend.image.tag=latest

# Verify installation
kubectl get pods
kubectl get services
```

#### 3. Access the Application

```bash
# Port forward the frontend service
kubectl port-forward service/todo-frontend-service 3000:3000

# Or use Minikube tunnel for external access
minikube tunnel
```

### Configuration

#### Environment Variables

The application is configured via environment variables in the Helm chart values:

- `NEXT_PUBLIC_BACKEND_URL`: URL for the backend API
- `NEXT_PUBLIC_BETTER_AUTH_URL`: URL for Better Auth
- `DATABASE_URL`: PostgreSQL connection string
- `BETTER_AUTH_SECRET`: Secret key for authentication
- `OPENAI_API_KEY`: OpenAI API key for AI features

These are configured in `helm-chart/values.yaml`.

### Troubleshooting

#### Common Issues

1. **ImagePullBackOff**: Make sure Docker images are built locally before deploying to Kubernetes
2. **Service unavailable**: Check that all pods are running with `kubectl get pods`
3. **Database connection errors**: Verify PostgreSQL is running and accessible

#### Useful Commands

```bash
# Check pod status
kubectl get pods

# View pod logs
kubectl logs -l app=todo-backend
kubectl logs -l app=todo-frontend

# Check service endpoints
kubectl get services

# Scale deployments
kubectl scale deployment todo-backend --replicas=3
kubectl scale deployment todo-frontend --replicas=2

# Update Helm deployment
helm upgrade todo-app .

# Uninstall Helm release
helm uninstall todo-app
```

### Deployment Notes

- The application is designed to be cloud-native with immutable containers
- All configuration is done via environment variables (no hardcoded values)
- The system supports multi-replica deployments for scalability
- Kubernetes is the source of truth for infrastructure
- The application survives pod restarts with zero data loss

## Section 2: GitHub MCP Integration

### Getting GitHub Personal Access Token

#### Step 1: Open GitHub in Your Browser
- Open your web browser and go to [https://github.com](https://github.com)
- Sign in to your GitHub account

#### Step 2: Access Your Profile Settings
1. Look for your profile picture in the **top-right corner** of the page
2. Click on the profile picture to open the dropdown menu
3. From the dropdown menu, click on **"Settings"**

#### Step 3: Navigate to Developer Settings
1. On the Settings page, look at the **left sidebar**
2. Scroll down until you see **"Developer settings"** at the bottom of the sidebar
3. Click on **"Developer settings"**

#### Step 4: Access Personal Access Tokens
1. Under Developer settings, you'll see several options
2. Click on **"Personal access tokens"**
3. Then click on **"Tokens (classic)"**

#### Step 5: Generate New Token
1. Click the **"Generate new token"** button
2. Select **"Generate new token (classic)"** from the submenu

#### Step 6: Fill in Token Details
1. In the **"Note"** field, type a name for your token (e.g., "Todo App Token")
2. Select an expiration date from the dropdown (e.g., "30 days", "90 days", or "No expiration")
3. In the **"Select scopes"** section, check these boxes:
   - ✅ **repo** (Full control of private repositories)
   - ✅ **gist** (Create gists)
   - ✅ **read:org** (Read org and team membership)

#### Step 7: Generate the Token
1. Scroll down to the bottom of the page
2. Click the **"Generate token"** button (green button)

#### Step 8: Copy Your Token
1. **Important**: You'll see your new token displayed on the screen
2. **Immediately copy the token** - you won't be able to see it again!
3. The token will look like a long string starting with `ghp_` followed by random characters

#### Step 9: Configure Your Application
1. Open your project's `.env` file in the `src/backend/` directory
2. Add this line to the file:
   ```
   GITHUB_TOKEN=your_copied_token_here
   ```
3. Also add:
   ```
   GITHUB_OWNER=your_github_username
   GITHUB_REPO=your_repository_name
   ```

#### Step 10: Save and Secure
1. Save the `.env` file
2. Make sure your `.gitignore` file prevents the `.env` file from being committed to Git

**⚠️ Warning**: Never share this token publicly or commit it to a repository. Keep it secure!

### GitHub MCP Integration Features

The project now includes GitHub integration through Model Context Protocol (MCP) tools. This allows the AI assistant to interact with GitHub repositories directly.

#### Available GitHub Tools:
- Create GitHub issues
- List GitHub issues
- Create GitHub pull requests
- Get repository information
- List repository contents
- Create GitHub gists

The AI assistant can now handle requests like:
- "Create a GitHub issue about the login bug"
- "List all open issues in the repository"
- "Create a pull request for the new feature"
- "Show me the contents of the src directory"
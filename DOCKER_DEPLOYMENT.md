# 🐳 Docker Deployment Guide - Phase 1-4

## 🎯 Quick Start (Automated)

### Option 1: One-Command Deployment

```bash
cd ~/Projects/2nd_hackathon-phase1-4
chmod +x deploy-docker.sh
./deploy-docker.sh
```

This script will:
1. ✅ Create .env file with your API keys
2. ✅ Stop any existing containers
3. ✅ Build backend and frontend images
4. ✅ Start all services with docker-compose
5. ✅ Run health checks
6. ✅ Show you the URLs to access

---

## 📋 Manual Deployment (Step-by-Step)

### Step 1: Create .env File

```bash
cd ~/Projects/2nd_hackathon-phase1-4

# Create .env file for docker-compose
cat > .env <<'EOF'
DATABASE_URL=postgresql://neondb_owner:npg_zhJvIP74aTle@ep-long-waterfall-abcwopjg-pooler.eu-west-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require
BETTER_AUTH_SECRET=my_super_secure_hackathon_secret_key_2025
OPENAI_API_KEY=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
GITHUB_TOKEN=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
GITHUB_OWNER=Shafqatsarwar
GITHUB_REPO=2nd_hackathon-phase1-4
EOF
```

### Step 2: Build Docker Images

```bash
# Build backend image (takes 2-3 minutes)
docker build -f Dockerfile.backend -t todo-backend:latest .

# Build frontend image (takes 5-7 minutes)
docker build -f Dockerfile.frontend -t todo-frontend:latest .
```

### Step 3: Start Services

```bash
# Start all services in detached mode
docker-compose up -d

# Or start with logs visible
docker-compose up
```

### Step 4: Verify Deployment

```bash
# Check container status
docker-compose ps

# View logs
docker-compose logs -f

# Test backend health
curl http://localhost:8000/health

# Test frontend
curl http://localhost:3000
```

---

## 🌐 Access Your Application

Once deployed, access:

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:3000 | Main application UI |
| **Backend API** | http://localhost:8000 | REST API |
| **API Docs** | http://localhost:8000/docs | Interactive API documentation |
| **Database** | localhost:5432 | PostgreSQL (using Neon cloud) |

---

## 🔧 Docker Commands Reference

### Container Management

```bash
# Start containers
docker-compose up -d

# Stop containers
docker-compose down

# Restart containers
docker-compose restart

# View running containers
docker-compose ps

# View logs (all services)
docker-compose logs -f

# View logs (specific service)
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Rebuild & Update

```bash
# Rebuild and restart (after code changes)
docker-compose up -d --build

# Rebuild specific service
docker-compose up -d --build backend

# Remove all containers and volumes
docker-compose down -v
```

### Debugging

```bash
# Execute command in running container
docker-compose exec backend bash
docker-compose exec frontend sh

# View container resource usage
docker stats

# Inspect container
docker inspect <container_name>
```

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────┐
│           Docker Compose Network            │
│                                             │
│  ┌──────────────┐      ┌──────────────┐   │
│  │   Frontend   │      │   Backend    │   │
│  │  (Next.js)   │─────▶│  (FastAPI)   │   │
│  │  Port: 3000  │      │  Port: 8000  │   │
│  └──────────────┘      └──────────────┘   │
│         │                      │           │
│         │                      ▼           │
│         │              ┌──────────────┐   │
│         │              │  PostgreSQL  │   │
│         │              │  Port: 5432  │   │
│         │              └──────────────┘   │
│         │                                  │
│         ▼                                  │
│  External: Neon PostgreSQL (Cloud)        │
└─────────────────────────────────────────────┘
```

---

## 📦 What's Inside Each Container

### Backend Container
- **Base**: Python 3.12-slim
- **Framework**: FastAPI + Uvicorn
- **Features**:
  - Task CRUD API
  - AI Chatbot with OpenAI
  - Better Auth integration
  - MCP tools (GitHub, Web Search)
  - AI Skills (sentiment analysis, tag suggestions)

### Frontend Container
- **Base**: Node 20-alpine
- **Framework**: Next.js 15
- **Features**:
  - Modern React UI
  - AI Chat with voice (STT/TTS)
  - Better Auth integration
  - Tailwind CSS styling
  - Bilingual support (English/Urdu)

### Database Container
- **Image**: PostgreSQL 15
- **Purpose**: Local development database
- **Note**: Production uses Neon PostgreSQL (cloud)

---

## 🔍 Troubleshooting

### Issue: Port Already in Use

```bash
# Find process using port
lsof -i :3000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or stop local dev servers
pkill -f uvicorn
pkill -f next
```

### Issue: Build Fails

```bash
# Clear Docker cache and rebuild
docker system prune -a
docker-compose build --no-cache
```

### Issue: Frontend Can't Connect to Backend

```bash
# Check if backend is running
docker-compose logs backend

# Verify network
docker network ls
docker network inspect 2nd_hackathon-phase1-4_app-network
```

### Issue: Database Connection Error

```bash
# Check DATABASE_URL in .env
cat .env

# Verify Neon PostgreSQL is accessible
curl -I https://ep-long-waterfall-abcwopjg-pooler.eu-west-2.aws.neon.tech
```

---

## 🚀 Production Deployment

### Using Docker Hub

```bash
# Tag images
docker tag todo-backend:latest shafqatsarwar/todo-backend:latest
docker tag todo-frontend:latest shafqatsarwar/todo-frontend:latest

# Push to Docker Hub
docker push shafqatsarwar/todo-backend:latest
docker push shafqatsarwar/todo-frontend:latest
```

### Using Kubernetes (Helm)

```bash
# Install with Helm
cd helm-chart
helm install todo-app .

# Check deployment
kubectl get pods
kubectl get services

# Port forward
kubectl port-forward svc/todo-app-frontend-service 3000:3000
kubectl port-forward svc/todo-app-backend-service 8000:8000
```

---

## 📊 Health Checks

### Backend Health

```bash
# Basic health
curl http://localhost:8000/health

# OpenAI health
curl http://localhost:8000/health/openai

# API root
curl http://localhost:8000/
```

### Frontend Health

```bash
# Check if frontend is responding
curl -I http://localhost:3000

# Check build info
curl http://localhost:3000/_next/static/
```

---

## 🎯 Next Steps After Deployment

1. **Test the Application**
   - Visit http://localhost:3000
   - Create a task
   - Test AI chatbot
   - Try voice features

2. **Monitor Logs**
   ```bash
   docker-compose logs -f
   ```

3. **Test API Endpoints**
   - Visit http://localhost:8000/docs
   - Try the interactive API

4. **Deploy to Cloud** (Optional)
   - Push to Docker Hub
   - Deploy to Kubernetes
   - Or use Vercel for frontend

---

## 📝 Environment Variables Reference

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | ✅ Yes |
| `BETTER_AUTH_SECRET` | Auth secret (must match frontend/backend) | ✅ Yes |
| `OPENAI_API_KEY` | OpenAI API key for chatbot | ✅ Yes |
| `GITHUB_TOKEN` | GitHub personal access token | ⚠️ Optional |
| `GITHUB_OWNER` | GitHub username | ⚠️ Optional |
| `GITHUB_REPO` | Repository name | ⚠️ Optional |

---

## 🎉 Success Criteria

Your Docker deployment is successful when:

- ✅ `docker-compose ps` shows all containers as "Up"
- ✅ http://localhost:3000 loads the frontend
- ✅ http://localhost:8000/health returns `{"status": "healthy"}`
- ✅ http://localhost:8000/docs shows API documentation
- ✅ You can create and manage tasks
- ✅ AI chatbot responds to queries
- ✅ Voice features work (in browser)

---

**🎊 Congratulations! Your Phase 1-4 application is now running in Docker!**

For more details, see:
- `docker-compose.yml` - Service configuration
- `Dockerfile.backend` - Backend container spec
- `Dockerfile.frontend` - Frontend container spec
- `guide.md` - Development guide

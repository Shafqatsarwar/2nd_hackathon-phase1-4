# The Evolution of Todo - Phase IV: Cloud-Native Kubernetes Deployment

This repository contains the "The Evolution of Todo" project, showcasing the complete evolution from a simple CLI tool to a cloud-native, full-stack web system with AI capabilities. This project follows the Agentic Dev Stack workflow: Write spec → Generate plan → Break into tasks → Implement via Claude Code.

## 🚀 Project Overview

The project evolves through multiple phases:

- **Phase I**: In-Memory Python Console App
- **Phase II**: Full-Stack Web Application (Next.js + FastAPI)
- **Phase III**: AI-Powered Todo Chatbot
- **Phase IV**: Local Kubernetes Deployment (Current Focus)
- **Phase V**: Advanced Cloud Deployment

## 🌟 Features

### Core Todo Functionality
- Add, View, Update, Delete tasks
- Mark tasks as complete/incomplete
- User authentication and authorization

### Advanced Features
- Priority management
- Recurring tasks
- AI-powered analysis and sentiment detection
- Real-time web search capabilities for current information (weather, news, market rates, etc.)
- Chat history functionality
- MCP (Model Context Protocol) server integration

### Cloud-Native Features (Phase IV)
- Dockerized frontend and backend applications
- Helm charts for Kubernetes deployment
- Multi-replica readiness
- Local cluster deployment with Minikube
- AI-assisted operations with kubectl-ai and kagent
- Docker AI Agent (Gordon) integration

## 🛠 Tech Stack

- **Frontend**: Next.js 16+ (App Router)
- **Backend**: Python FastAPI
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth (JWT-based)
- **AI Integration**: OpenAI Agents SDK, MCP Server
- **Containerization**: Docker
- **Orchestration**: Kubernetes (Minikube)
- **Package Management**: uv

## 📁 Repository Structure

```
.
├── api/                    # Vercel serverless entry point
├── .claude/               # Claude Code MCP configuration
├── .specify/              # Claude Code memory and history
├── specs/                 # SDD Specifications
├── src/
│   ├── cli/               # Phase I: CLI App
│   ├── backend/           # Phase II+: Python FastAPI service
│   └── frontend/          # Phase II+: Next.js application
├── helm-chart/            # Phase IV: Kubernetes Helm charts
├── Dockerfile.backend     # Phase IV: Backend container
├── Dockerfile.frontend    # Phase IV: Frontend container
├── docker-compose.yml     # Phase IV: Local orchestration
├── vercel.json            # Vercel routing configuration
├── constitution.md        # Governing Rules
├── CLAUDE.md              # Claude Code instructions
├── guide.md               # Developer guide (with Phase IV)
└── pyproject.toml         # Project Workspace
```

## 🚀 Phase IV: Kubernetes Deployment

This project is now fully prepared for cloud-native deployment with the following features:

### Dockerization
- Both frontend and backend are containerized
- Optimized Dockerfiles for production
- Multi-stage builds for smaller images

### Helm Charts
- Complete Kubernetes deployment manifests
- Parameterizable configurations
- Service networking setup
- Resource management

### Local Kubernetes Setup
- Works with Minikube or Docker Desktop Kubernetes
- Multi-replica deployment ready
- Service discovery and load balancing

### AI-Assisted Operations
- kubectl-ai for intelligent Kubernetes operations
- kagent for cluster analysis
- Docker AI Agent (Gordon) for container operations

## 🚀 Quick Start

### Local Development
1. Clone the repository
2. Install dependencies:
   ```bash
   cd src/backend
   uv sync
   cd ../frontend
   npm install
   ```
3. Start backend: `uv run uvicorn main:app --reload --port 8000`
4. Start frontend: `npm run dev`

### Docker Deployment
1. Build Docker images:
   ```bash
   docker build -f Dockerfile.backend -t todo-backend:latest .
   docker build -f Dockerfile.frontend -t todo-frontend:latest .
   ```
2. Run with Docker Compose:
   ```bash
   docker-compose up -d
   ```

### Kubernetes Deployment
1. Install prerequisites: Docker, kubectl, Helm
2. Start Minikube: `minikube start`
3. Deploy with Helm:
   ```bash
   cd helm-chart
   helm install todo-release .
   ```

## 🌐 Live Deployment

The application can be deployed to:
- Vercel (for web deployment)
- Kubernetes cluster (for cloud-native deployment)
- Local Minikube (for development)

## 🤝 Contributing

This project follows a strict Spec-Driven Development (SDD) approach. All contributions should:
1. Follow the SDD workflow: Spec → Plan → Tasks → Implementation
2. Maintain the existing architecture and patterns
3. Preserve all existing functionality while adding new features
4. Update specifications when adding new features

## 📄 License

This project is part of the Panaversity Hackathon curriculum.
# 📖 Developer Guide: The Evolution of Todo

Welcome to the internal developer guide for Phase IV. This project implements a cloud-native, AI-powered Todo system using Spec-Driven Development (SDD).

## 🏗️ System Architecture

The application is split into three main tiers:

1.  **Frontend (Next.js 16)**: A modern React application using the App Router, Tailwind CSS, and Vercel AI SDK. It handles UI, voice interaction, and client-side auth.
2.  **Backend (FastAPI)**: A high-performance Python service that manages tasks, integrates with MCP (Model Context Protocol), and orchestrates AI agents.
3.  **Database (PostgreSQL)**: Hosted on Neon Serverless, managed via SQLModel (ORM).

## 📂 Project Structure

```text
.
├── src/
│   ├── frontend/          # Next.js Application
│   │   ├── app/           # Routes and API Handlers
│   │   ├── components/    # Reusable UI Components
│   │   └── .env.local     # Local Environment Variables
│   └── backend/           # FastAPI Application
│       ├── agents/        # OpenAI Orchestrator
│       ├── mcp_server/    # MCP Tools (GitHub, Web Search, Weather)
│       ├── models.py      # SQLModel Schemas
│       └── .env.backend   # Backend Environment Variables
├── helm-chart/            # Kubernetes Manifests
├── Dockerfile.backend     # Backend Container Spec
└── Dockerfile.frontend    # Frontend Container Spec
```

## 🎙️ AI Chat & Voice Features

We use the **Vercel AI SDK** combined with **Web Speech API** for a seamless interactive experience.

### Key Components:
- **STT (Speech-to-Text)**: Native browser `SpeechRecognition`.
- **TTS (Text-to-Speech)**: Native browser `speechSynthesis`.
- **Language Support**: Default is English (`en-US`), with support for Urdu (`ur-PK`).

### How to test:
1. Start the dev servers.
2. Visit `/chat`.
3. Click the 🎙️ icon to speak. The AI will respond and optionally read the message aloud via the 🔊 icon.

## 🛠️ MCP (Model Context Protocol) Tools

The backend exposes several tools to the AI Agent:
- **Task Tools**: CRUD operations on todos.
- **GitHub Tools**: Create issues, PRs, and list repos.
- **Web Search**: Real-time information fetching via Google/DuckDuckGo.
- **Weather**: Current weather and forecasts.

## 🤖 AI Agent Skills

The AI agents in this project are equipped with specialized skills to manage the deployment lifecycle:

- **Dockerization Skill**: Automatically generates and optimizes Dockerfiles for any service.
- **Helm Chart Skill**: Creates declarative Kubernetes manifests and manages value overrides.
- **Minikube Setup Skill**: Configures local Kubernetes environments and integrates with Docker.
- **K8s Deployment Skill**: Validates multi-replica readiness and zero-data-loss persistence.
- **Gordon (Docker AI)**: Special agent for container runtime optimization.
- **kubectl-ai & kagent**: Natural language orchestration and cluster diagnostics.

## 🚀 Development Workflow

1.  **Sync Dependencies**:
    ```bash
    # Frontend
    cd src/frontend && npm install
    # Backend
    uv sync
    ```
2.  **Set Environment Variables**:
    Ensure `.env.local` and `.env.backend` are populated with the keys provided in the setup instructions.
3.  **Run Development Servers**:
    ```bash
    # Backend
    uv run uvicorn src.backend.main:app --reload --port 8000
    # Frontend
    npm run dev --workspace=src/frontend
    ```

## 🔒 Security & Auth

- **Better Auth**: Handles user sessions and JWT generation.
- **JWT Middleware**: FastAPI `verify_jwt` dependency ensures that users can only access their own tasks.
- **Isolation**: Every database query is scoped by `user_id`.

## 📜 Constitutional Alignment

This project strictly follows the **Constitution**.
- **Golden Rule**: No manual code writing. All logic is derived from specs.
- **Statelessness**: Services are designed to be horizontally scalable.
- **Cloud-Ready**: Everything is containerized and ready for Kubernetes.

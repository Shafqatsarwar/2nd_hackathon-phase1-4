# 🚀 The Evolution of Todo: Phase IV
### Cloud-Native, AI-Powered Task Management System

[![Next.js](https://img.shields.io/badge/Frontend-Next.js%2016-black?logo=next.js)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Kubernetes](https://img.shields.io/badge/Orchestration-Kubernetes-326ce5?logo=kubernetes)](https://kubernetes.io/)
[![PostgreSQL](https://img.shields.io/badge/Database-Neon%20PostgreSQL-336791?logo=postgresql)](https://neon.tech/)

## 🌟 Overview

**The Evolution of Todo** is a showcase of modern software engineering, evolving from a simple CLI tool into a sophisticated, cloud-native enterprise platform. Phase IV focuses on **Local Kubernetes Deployment**, ensuring the system is resilient, scalable, and management-automated through AI.

## ✨ Key Features

-   **🤖 AI Conversational UI**: Manage your tasks through natural language with our built-in chatbot.
-   **🎙️ Voice-To-Action**: Fully integrated voice commands (STT) and voice feedback (TTS) with Urdu support.
-   **🔌 MCP Integration**: AI agents empowered with tools to interact with GitHub, perform web searches, and check weather.
-   **☸️ Cloud-Native Deployment**: Fully containerized with Docker and orchestrated via Kubernetes (Helm).
-   **🔐 Secure Multi-Tenancy**: Robust authentication powered by Better Auth with strict user data isolation.
-   **📈 Spec-Driven Development**: Entirely built using SDD principles where the specification is the absolute source of truth.

## 🛠 Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Frontend** | Next.js 15+ (App Router), Tailwind CSS, Framer Motion |
| **Backend** | Python FastAPI, SQLModel, Uvicorn |
| **AI** | OpenAI GPT-4o, Vercel AI SDK, MCP Server |
| **Auth** | Better Auth (JWT) |
| **Database** | Neon Serverless PostgreSQL |
| **DevOps** | Docker, Kubernetes, Helm, Minikube |
| **Tools** | uv, npm, kubectl-ai, kagent |

## 🚀 Quick Start

### 1. Prerequisites
Ensure you have `uv`, `node.js`, and `docker` installed.

### 2. Setup
```bash
# Clone the repository
git clone https://github.com/Shafqatsarwar/2nd_hackathon-phase1-4.git
cd 2nd_hackathon-phase1-4

# Install dependencies (WSL/Linux/macOS)
npm install
uv sync
```

### 3. Run Locally
```bash
# Start Backend
uv run uvicorn src.backend.main:app --reload --port 8000

# Start Frontend
npm run dev
```

## ☸️ Production-Ready Deployment

For instructions on how to deploy this system to a **Kubernetes** cluster, please refer to:
👉 **[Deployment Instructions](./instructions.md)**

## 🧪 Developer Resources

-   **[Developer Guide](./guide.md)**: Deep dive into architecture and features.
-   **[Project Constitution](./.specify/memory/📜%20CONSTITUTION-Hackathon%20II%20-%20Full%20Todo%20Spec-Driven%20Development.md)**: The governing rules of this project.

## 🤝 Acknowledgments

Built for the **Panaversity Hackathon II** — pushing the boundaries of AI-native software development.
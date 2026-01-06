# 2nd_hackathon-phase1-4

## The Evolution of Todo - From CLI to Full-Stack Cloud-Native AI System

This repository contains the "The Evolution of Todo" project, implementing a todo application that evolves from a simple CLI tool to a full-stack web application with AI capabilities. This project follows the Agentic Dev Stack workflow: Write spec → Generate plan → Break into tasks → Implement via Claude Code.

## Project Overview

The project evolves through multiple phases:

- **Phase I**: In-Memory Python Console App
- **Phase II**: Full-Stack Web Application (Next.js + FastAPI)
- **Phase III**: AI-Powered Todo Chatbot
- **Phase IV**: Local Kubernetes Deployment (Current Focus)
- **Phase V**: Advanced Cloud Deployment

## Features

### Core Todo Functionality
- Add, View, Update, Delete tasks
- Mark tasks as complete/incomplete
- User authentication and authorization

### Advanced Features
- Priority management
- Recurring tasks
- AI-powered analysis and sentiment detection
- Web search capabilities
- Chat history functionality
- MCP (Model Context Protocol) server integration

### Cloud-Native Features (Phase IV)
- Dockerized frontend and backend applications
- Helm charts for Kubernetes deployment
- Multi-replica readiness
- Local cluster deployment with Minikube
- AI-assisted operations with kubectl-ai and kagent
- Docker AI Agent (Gordon) integration

## Tech Stack

- **Frontend**: Next.js 16+ (App Router)
- **Backend**: Python FastAPI
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth (JWT-based)
- **AI Integration**: OpenAI Agents SDK, MCP Server
- **Containerization**: Docker
- **Orchestration**: Kubernetes (Minikube)
- **Package Management**: uv

## API Endpoints (Phase II+)

- `GET /api/{user_id}/tasks` - List all tasks
- `POST /api/{user_id}/tasks` - Create a new task
- `GET /api/{user_id}/tasks/{id}` - Get task details
- `PUT /api/{user_id}/tasks/{id}` - Update a task
- `DELETE /api/{user_id}/tasks/{id}` - Delete a task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle completion
- `POST /api/{user_id}/chat` - AI chatbot endpoint
- `GET /api/{user_id}/chat/history` - Chat history

## Development Workflow

1. Create specification in `/specs/`
2. Generate plan based on specification
3. Break plan into tasks
4. Implement via Claude Code
5. No manual editing of generated source code in `src/`

## Environment Configuration

- Database configuration via `DATABASE_URL`
- Authentication via `BETTER_AUTH_SECRET`
- Backend URL via `NEXT_PUBLIC_BACKEND_URL`
- Auth URL via `NEXT_PUBLIC_BETTER_AUTH_URL`
- OpenAI API key via `OPENAI_API_KEY`

## Deployment

The application is designed for deployment to Vercel with the backend API running on FastAPI.

## Compliance with Constitution

- All development starts with specification
- No manual code editing in `src/` directory
- Uses Claude Code and Spec-Kit Plus as primary tools
- Follows the Agentic Dev Stack workflow

## Repository Structure

- `/specs` - Feature specifications and architectural plans
- `/src` - Verified source code
- `/src/cli` - Phase I: In-Memory Python CLI App
- `/src/backend` - Phase II+: Python FastAPI service
- `/src/frontend` - Phase II+: Next.js application
- `/api/index.py` - Vercel serverless entry point
- `/history` - Prompt History Records (PHR) and ADRs
- `.claud/skills` - Skills for Phase IV (Kubernetes deployment)

## License

This project is part of the Panaversity Hackathon curriculum.

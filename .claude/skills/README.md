# Hackathon II Todo Evolution Skill

This skill implements the "The Evolution of Todo" hackathon requirements, supporting the progression from CLI app to cloud-native AI system.

## Overview

The skill supports the following phases of the hackathon:

- **Phase I**: In-Memory Python Console App
- **Phase II**: Full-Stack Web Application
- **Phase III**: AI-Powered Todo Chatbot
- **Phase IV**: Local Kubernetes Deployment
- **Phase V**: Advanced Cloud Deployment

## Constitution Compliance

This skill enforces the Spec-Driven Development (SDD) workflow:
- **Specify** → **Plan** → **Tasks** → **Implement**
- All code must be generated via Claude Code from validated specs
- No manual code editing allowed in `src/` directory

## Commands

### `create-project-structure`
Creates the required project structure for the hackathon.

### `create-specification`
Creates a specification file following SDD principles.
- `feature_name`: Name of the feature to specify
- `content`: Content of the specification

### `create-plan`
Creates an implementation plan.
- `feature_name`: Name of the feature to plan
- `plan_content`: Content of the implementation plan

### `create-tasks`
Creates a task breakdown for implementation.
- `feature_name`: Name of the feature to break into tasks
- `tasks`: List of tasks to create

### `execute-phase`
Executes a specific phase following SDD workflow.
- `phase`: Name of the phase to execute (Phase I, Phase II, etc.)

### `validate-spec-compliance`
Validates that the project follows SDD constitution.

### `get-phase-requirements`
Gets requirements for a specific phase.
- `phase`: Name of the phase to get requirements for

## Usage Example

```python
from skills.hackathon_todo_skill import HackathonTodoSkill

skill = HackathonTodoSkill()
skill.create_project_structure()
skill.execute_phase("Phase I")
```

## Technology Stack

- Python 3.13+
- Claude Code
- Spec-Kit Plus
- Next.js 16+ (from Phase II)
- FastAPI (from Phase II)
- SQLModel (from Phase II)
- Neon Serverless PostgreSQL (from Phase II)
- Better Auth (from Phase II)
- OpenAI Agents SDK (from Phase III)
- Official MCP SDK (from Phase III)
- Docker, Kubernetes, Helm (from Phase IV)
- Kafka, Dapr (from Phase V)
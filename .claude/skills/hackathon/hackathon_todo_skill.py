"""
Hackathon II Todo Skill - Spec-Driven Development for Todo Evolution

This skill implements the "The Evolution of Todo" hackathon requirements,
supporting the progression from CLI app to cloud-native AI system.

Phases:
- Phase I: In-Memory Python Console App
- Phase II: Full-Stack Web Application
- Phase III: AI-Powered Todo Chatbot
- Phase IV: Local Kubernetes Deployment
- Phase V: Advanced Cloud Deployment

Constitution: All development must follow SDD (Specify → Plan → Tasks → Implement)
No manual code editing allowed in src/ directory.
"""
import os
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass


@dataclass
class PhaseConfig:
    """Configuration for each hackathon phase"""
    phase: str
    description: str
    tech_stack: List[str]
    required_features: List[str]
    deliverables: List[str]

    def get_deployment_script(self):
        """Return the path to the deployment script for this phase if applicable"""
        if self.phase == "Phase IV":
             return "scripts/deploy_to_k8s.py"
        return None


class HackathonTodoSkill:
    """
    Skill for implementing the Hackathon II Todo Evolution project
    following Spec-Driven Development principles
    """

    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.specs_dir = self.project_root / "specs"
        self.src_dir = self.project_root / "src"
        self.history_dir = self.project_root / "history"

        # Define phase configurations
        self.phases = {
            "phase_i": PhaseConfig(
                phase="Phase I",
                description="Todo In-Memory Python Console App",
                tech_stack=["Python 3.13+", "UV", "Claude Code", "Spec-Kit Plus"],
                required_features=[
                    "Add Task (Title & Description)",
                    "View Task List (with Status indicators)",
                    "Update Task Details",
                    "Delete Task by ID",
                    "Mark Task as Complete/Incomplete"
                ],
                deliverables=[
                    "Python CLI application",
                    "In-memory storage",
                    "Console interface"
                ]
            ),
            "phase_ii": PhaseConfig(
                phase="Phase II",
                description="Todo Full-Stack Web Application",
                tech_stack=[
                    "Next.js 16+ (App Router)", "Python FastAPI",
                    "SQLModel", "Neon Serverless PostgreSQL",
                    "Better Auth", "Claude Code + Spec-Kit Plus"
                ],
                required_features=[
                    "All 5 Basic Level features as web app",
                    "RESTful API endpoints",
                    "Responsive frontend interface",
                    "Neon Serverless PostgreSQL storage",
                    "User authentication (Better Auth)"
                ],
                deliverables=[
                    "Frontend Next.js app",
                    "Backend FastAPI service",
                    "REST API with JWT auth",
                    "Database schema"
                ]
            ),
            "phase_iii": PhaseConfig(
                phase="Phase III",
                description="Todo AI Chatbot",
                tech_stack=[
                    "OpenAI ChatKit", "OpenAI Agents SDK",
                    "Official MCP SDK", "Python FastAPI",
                    "SQLModel", "Neon Serverless PostgreSQL",
                    "Better Auth", "Claude Code + Spec-Kit Plus"
                ],
                required_features=[
                    "Conversational interface for all Basic Level features",
                    "MCP server with task operation tools",
                    "Stateless chat endpoint",
                    "AI agents using MCP tools",
                    "Natural language processing"
                ],
                deliverables=[
                    "MCP server with tools",
                    "AI chatbot interface",
                    "Conversation state management",
                    "MCP tools for task operations"
                ]
            ),
            "phase_iv": PhaseConfig(
                phase="Phase IV",
                description="Local Kubernetes Deployment",
                tech_stack=[
                    "Docker", "Minikube", "Helm Charts",
                    "kubectl-ai", "kagent", "Phase III Todo Chatbot",
                    "GitHub MCP Tool"
                ],
                required_features=[
                    "Containerized frontend & backend",
                    "Helm charts for deployment",
                    "Minikube local cluster deployment",
                    "Multi-replica readiness",
                    "GitHub MCP Integration"
                ],
                deliverables=[
                    "Docker images",
                    "Helm charts",
                    "Kubernetes manifests",
                    "Minikube deployment",
                    "Verified GitHub Tools"
                ]
            ),
            "phase_v": PhaseConfig(
                phase="Phase V",
                description="Advanced Cloud Deployment",
                tech_stack=[
                    "Kafka (Redpanda/Strimzi/Managed)",
                    "Dapr (Pub/Sub, State, Jobs, Secrets)",
                    "Managed Kubernetes (AKS/GKE/OKE)",
                    "Phase IV deployment"
                ],
                required_features=[
                    "Recurring tasks",
                    "Due dates & reminders",
                    "Event-driven processing",
                    "Distributed services"
                ],
                deliverables=[
                    "Kafka event streams",
                    "Dapr integration",
                    "Cloud Kubernetes deployment",
                    "Advanced features"
                ]
            )
        }

    def create_project_structure(self):
        """Create the required project structure"""
        dirs_to_create = [
            self.specs_dir,
            self.src_dir,
            self.history_dir,
            self.specs_dir / "features",
            self.specs_dir / "api",
            self.specs_dir / "database",
            self.specs_dir / "ui",
            self.src_dir / "cli",  # Phase I
            self.src_dir / "backend",  # Phase II+
            self.src_dir / "frontend",  # Phase II+
        ]

        for directory in dirs_to_create:
            directory.mkdir(parents=True, exist_ok=True)

        print(f"Created project structure in {self.project_root}")

    def create_specification(self, feature_name: str, content: str) -> Path:
        """Create a specification file following SDD principles"""
        spec_file = self.specs_dir / f"{feature_name}.md"

        with open(spec_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"Created specification: {spec_file}")
        return spec_file

    def create_plan(self, feature_name: str, plan_content: str) -> Path:
        """Create an implementation plan"""
        plan_file = self.specs_dir / f"{feature_name}_plan.md"

        with open(plan_file, 'w', encoding='utf-8') as f:
            f.write(plan_content)

        print(f"Created plan: {plan_file}")
        return plan_file

    def create_tasks(self, feature_name: str, tasks: List[Dict]) -> Path:
        """Create a task breakdown for implementation"""
        tasks_file = self.specs_dir / f"{feature_name}_tasks.md"

        content = f"# Tasks for {feature_name}\n\n"
        for i, task in enumerate(tasks, 1):
            content += f"## Task {i}: {task.get('title', 'Untitled Task')}\n\n"
            content += f"**Description:** {task.get('description', '')}\n\n"
            content += f"**Files to modify:** {', '.join(task.get('files', []))}\n\n"
            content += f"**Acceptance criteria:** {task.get('acceptance_criteria', '')}\n\n"

        with open(tasks_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"Created tasks: {tasks_file}")
        return tasks_file

    def run_claude_code_implementation(self, task_file: str):
        """Simulate running Claude Code implementation based on tasks"""
        print(f"Running Claude Code implementation based on: {task_file}")
        print("Implementation would be generated via Claude Code based on the task specification.")
        print("Per constitution: All code must be generated via Claude Code from validated specs.")

    def validate_spec_compliance(self) -> bool:
        """Validate that the project follows SDD constitution"""
        required_files = [
            self.project_root / "constitution.md",
            self.project_root / "CLAUDE.md",
            self.project_root / "specs",
            self.project_root / "src"
        ]

        all_present = True
        for file_path in required_files:
            if not file_path.exists():
                print(f"Missing required file/directory: {file_path}")
                all_present = False

        if all_present:
            print("✓ Project structure complies with SDD constitution")
            return True
        else:
            print("✗ Project structure does not comply with SDD constitution")
            return False

    def get_phase_requirements(self, phase: str) -> Optional[PhaseConfig]:
        """Get requirements for a specific phase"""
        return self.phases.get(phase.lower().replace(" ", "_"))

    def list_all_phases(self) -> List[str]:
        """List all available phases"""
        return list(self.phases.keys())

    def generate_phase_summary(self) -> Dict[str, Any]:
        """Generate a summary of all phases"""
        summary = {}
        for phase_key, config in self.phases.items():
            summary[phase_key] = {
                "phase": config.phase,
                "description": config.description,
                "tech_stack": config.tech_stack,
                "required_features": config.required_features,
                "deliverables": config.deliverables
            }
        return summary

    def execute_phase(self, phase: str) -> bool:
        """Execute a specific phase following SDD workflow"""
        phase_config = self.get_phase_requirements(phase)
        if not phase_config:
            print(f"Unknown phase: {phase}")
            return False

        print(f"\n--- Executing {phase_config.phase} ---")
        print(f"Description: {phase_config.description}")
        print(f"Tech Stack: {', '.join(phase_config.tech_stack)}")
        print(f"Required Features: {', '.join(phase_config.required_features)}")
        print(f"Deliverables: {', '.join(phase_config.deliverables)}")

        # Following SDD workflow: Specify → Plan → Tasks → Implement
        print(f"\n1. Creating specifications for {phase_config.phase}...")
        spec_content = f"# Specification for {phase_config.phase}\n\n## Objective\n{phase_config.description}\n\n## Features\n"
        for feature in phase_config.required_features:
            spec_content += f"- {feature}\n"

        spec_file = self.create_specification(f"{phase.lower().replace(' ', '_')}_spec", spec_content)

        print(f"\n2. Creating implementation plan for {phase_config.phase}...")
        plan_content = f"# Implementation Plan for {phase_config.phase}\n\n## Architecture\nPlan for implementing {phase_config.description}\n\n## Steps\n"
        for i, feature in enumerate(phase_config.required_features, 1):
            plan_content += f"{i}. {feature}\n"

        plan_file = self.create_plan(f"{phase.lower().replace(' ', '_')}_implementation", plan_content)

        print(f"\n3. Breaking down tasks for {phase_config.phase}...")
        tasks = []
        for i, feature in enumerate(phase_config.required_features):
            tasks.append({
                "title": f"Implement {feature}",
                "description": f"Implementation of {feature} feature",
                "files": [f"src/{'cli' if 'phase_i' in phase else 'backend'}/feature_{i}.py"],
                "acceptance_criteria": f"{feature} works as specified in the requirements"
            })

        tasks_file = self.create_tasks(f"{phase.lower().replace(' ', '_')}_implementation", tasks)

        print(f"\n4. Running Claude Code implementation for {phase_config.phase}...")
        self.run_claude_code_implementation(str(tasks_file))

        print(f"\n✓ Completed {phase_config.phase} execution following SDD workflow")
        return True


# Example usage function
def create_hackathon_todo_skill():
    """Factory function to create the hackathon todo skill"""
    return HackathonTodoSkill()


# Example of how to use the skill
if __name__ == "__main__":
    skill = HackathonTodoSkill()

    # Validate project compliance
    skill.validate_spec_compliance()

    # Create basic project structure
    skill.create_project_structure()

    # List all phases
    print("\nAvailable phases:")
    for phase in skill.list_all_phases():
        print(f"- {phase}")

    # Generate phase summary
    summary = skill.generate_phase_summary()
    print(f"\nTotal phases: {len(summary)}")

    # Example: Execute Phase I
    # skill.execute_phase("Phase I")
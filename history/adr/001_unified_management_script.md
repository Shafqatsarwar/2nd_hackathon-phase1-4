# ADR 001: Unified Management Script for Phase IV

## Date
2026-01-08

## Context
Phase IV requires managing a complex stack involving Docker, Minikube, Helm, and Kubectl.
Users (engineers) are operating in a hybrid Windows/WSL environment, which often leads to pathing issues and command syntax errors when alternating between PowerShell and Bash.
The previous approach of disparate shell scripts (`.sh`) created friction for Windows users and didn't provide a unified status view.

## Decision
We have decided to implement a **Unified Management Script** using Python (`manage_phase_4.py`) to encapsulate all Phase IV operations.

The script provides:
1.  **Status Check (`status`)**: Validates the presence of required tools (Docker, Minikube, Helm, Kubectl).
2.  **Deployment (`deploy`)**: wraps the `scripts/deploy_to_k8s.py` logic to build images, configure secrets, and install Helm charts.
3.  **Tunneling (`tunnel`)**: Automates `kubectl port-forward` for both services simultaneously, handling keep-alive logic.

## Consequences

### Positive
-   **Cross-Platform**: Python runs consistently in both WSL and Windows (provided tools are in PATH).
-   **Simplified UX**: User only needs to remember `uv run python manage_phase_4.py <action>`.
-   **Reduced Error Surface**: Encapsulates complex flags and environment variable injection (Secrets) within the script.
-   **Agent Integration**: The script imports and leverages the existing `HackathonTodoSkill` class, ensuring the code remains source-of-truth.

### Negative
-   **Dependency**: Requires Python environment (handled by `uv`).
-   **Maintenance**: Logic is now in Python rather than standard K8s makefiles/shell scripts, which might be less familiar to pure DevOps engineers.

## Status
Accepted and Implemented.

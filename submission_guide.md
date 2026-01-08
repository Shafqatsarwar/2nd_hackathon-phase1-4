
## 📦 Advanced: Adding Dependencies & Finalizing
To expand your project (e.g., waiting for Redis or other services) and prepare for submission:

### 1. Adding Dependencies (Helm)
To add standard packages (like Redis) to your cluster:
1.  **Edit `helm-chart/Chart.yaml`**:
    ```yaml
    dependencies:
      - name: redis
        version: 17.3.14
        repository: https://charts.bitnami.com/bitnami
    ```
2.  **Update Dependencies**:
    ```bash
    helm dependency update ./helm-chart
    ```
3.  **Deploy**:
    ```bash
    uv run python manage_phase_4.py deploy
    ```

### 2. Docker Debugging
If a container fails to start, inspect it directly:
```bash
# List running containers
docker ps

# See logs of a specific container
docker logs <container-id>

# Enter the container shell
docker exec -it <container-id> /bin/sh
```

### 3. 🏆 Finalizing & Submitting
Since this is a "Local Deployment" phase, your submission proof consists of:

**A. The Code Repository**
Ensure your `helm-chart/` and `Dockerfile`s are committed.

**B. The Demo Video (Proof of Work)**
Record a screen capture showing:
1.  **Deployment**: Run `uv run python manage_phase_4.py deploy` and show it succeeding.
2.  **Status**: Run `kubectl get all` to show running pods.
3.  **Usage**: Open `localhost:3000` and create a task.
4.  **AI Ops**: Run a simple command like `kubectl-ai "show me all pods"` to demonstrate the AI integration.

**C. Submission Instructions**
Include this command in your submission `README.md` so judges can run it easily:
> "To run this project locally, ensure you have Minikube and Python installed, then run: `uv run python manage_phase_4.py deploy`"


import subprocess
import sys
import time
import os
from pathlib import Path

def run_command(command, cwd=None, shell=True):
    """Run a shell command and print output"""
    print(f"🚀 Running: {command}")
    try:
        result = subprocess.run(
            command, 
            cwd=cwd, 
            shell=shell, 
            check=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True
        )
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error executing command: {command}")
        print(e.stderr)
        return False

def check_requirements():
    """Check if required tools are installed"""
    tools = ["docker", "minikube", "helm", "kubectl"]
    missing = []
    for tool in tools:
        if subprocess.call(f"which {tool}", shell=True, stdout=subprocess.DEVNULL) != 0:
            missing.append(tool)
    
    if missing:
        print(f"❌ Missing requirements: {', '.join(missing)}")
        return False
    return True

def deploy():
    root_dir = Path(__file__).parent.parent
    helm_dir = root_dir / "helm-chart"

    print("\n📦 --- PHASE IV: KUBERNETES DEPLOYMENT --- 📦\n")

    if not check_requirements():
        return

    # 1. Build Docker Images
    print("\n🏗️  Step 1: Building Docker Images (Minikube Context)...")
    # We use 'minikube image build' or eval docker-env. 
    # For robustness in scripts, let's try assuming the user has done `eval $(minikube docker-env)`
    # OR explicitly load them. specific to Minikube:
    
    run_command("docker build -f Dockerfile.backend -t todo-backend:latest .", cwd=root_dir)
    run_command("docker build -f Dockerfile.frontend -t todo-frontend:latest .", cwd=root_dir)

    # If using Minikube, we might need to load them if not using docker-env
    # run_command("minikube image load todo-backend:latest") 
    # run_command("minikube image load todo-frontend:latest")

    # 2. Update Helm Dependencies (if any)
    # print("\n⎈ Step 2: Preparing Helm Charts...")
    # run_command("helm dependency update", cwd=helm_dir)

    # 3. Create Secrets
    print("\n🔐 Step 3: Configuring Secrets...")
    # This is a simplified secret creation. In production, use external-secrets or sealed-secrets.
    # We'll use the existing .env file if possible, or just skip if exists to avoid error
    secret_cmd = """kubectl create secret generic todo-secrets \
    --from-literal=DATABASE_URL="${DATABASE_URL}" \
    --from-literal=BETTER_AUTH_SECRET="${BETTER_AUTH_SECRET}" \
    --from-literal=OPENAI_API_KEY="${OPENAI_API_KEY}" \
    --dry-run=client -o yaml | kubectl apply -f -"""
    # Note: Environment variables must be set in the shell running this script for this to work perfectly.
    
    # 4. Helm Install
    print("\n🚀 Step 4: Deploying with Helm...")
    run_command("helm upgrade --install todo-app . --values values.yaml", cwd=helm_dir)

    # 5. Wait for Rollout
    print("\n⏳ Step 5: Waiting for Rollout...")
    run_command("kubectl rollout status deployment/todo-backend")
    run_command("kubectl rollout status deployment/todo-frontend")

    print("\n✅ Deployment Complete!")
    print("\nUse 'kubectl port-forward svc/todo-frontend 3000:3000' to access the app.")

if __name__ == "__main__":
    deploy()

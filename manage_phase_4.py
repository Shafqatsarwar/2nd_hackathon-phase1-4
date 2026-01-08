#!/usr/bin/env python3
"""
Phase IV Management Script
Interacts with the Hackathon Agent Skills to manage the Kubernetes deployment.
"""
import sys
import argparse
import time
from pathlib import Path

# Add .claude/skills to path to import the skill module
sys.path.append(str(Path(__file__).parent / ".claude" / "skills"))
try:
    from hackathon_todo_skill import HackathonTodoSkill
    from scripts.deploy_to_k8s import deploy, check_requirements
except ImportError as e:
    print(f"Error importing skills: {e}")
    sys.exit(1)

def status():
    print("📊 Phase IV Status Check")
    skill = HackathonTodoSkill()
    phase_config = skill.get_phase_requirements("Phase IV")
    
    print(f"\nPhase: {phase_config.phase}")
    print(f"Description: {phase_config.description}")
    
    print("\n✅ Requirements Check:")
    if check_requirements():
        print("  - All system tools (docker, minikube, helm, kubectl) found.")
    else:
        print("  - ❌ Missing system tools.")

def run_tunnel():
    """
    Establish port forwarding for Frontend (3000) and Backend (8000).
    """
    print("� Establishing Tunnels (Port Forwarding)...")
    print("   - Frontend: http://localhost:3000")
    print("   - Backend:  http://localhost:8000")
    print("\nPress Ctrl+C to stop tunnels.")

    import subprocess
    
    # We use Popen to run both concurrently
    try:
        p1 = subprocess.Popen(
            ["kubectl", "port-forward", "svc/todo-app-frontend-service", "3000:3000"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        p2 = subprocess.Popen(
            ["kubectl", "port-forward", "svc/todo-app-backend-service", "8000:8000"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Keep alive
        while True:
            time.sleep(1)
            if p1.poll() is not None:
                print(f"❌ Frontend Tunnel died: {p1.stderr.read()}")
                break
            if p2.poll() is not None:
                print(f"❌ Backend Tunnel died: {p2.stderr.read()}")
                break

    except KeyboardInterrupt:
        print("\nStopping tunnels...")
        p1.terminate()
        p2.terminate()

def main():
    parser = argparse.ArgumentParser(description="Manage Phase IV: Local Kubernetes Deployment")
    parser.add_argument("action", choices=["status", "deploy", "tunnel"], help="Action to perform")
    
    args = parser.parse_args()
    
    if args.action == "status":
        status()
    elif args.action == "deploy":
        run_deployment()
    elif args.action == "tunnel":
        run_tunnel()

if __name__ == "__main__":
    main()

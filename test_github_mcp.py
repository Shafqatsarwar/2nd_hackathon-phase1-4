
import os
import sys
from dotenv import load_dotenv

# Add project root to sys.path
sys.path.append(os.getcwd())

from src.backend.mcp_server.github_tools import GitHubMCPTools

# Load environment variables
load_dotenv()

def test_github_tools():
    print("Testing GitHub MCP Tools...")
    
    # Initialize tools
    github_tools = GitHubMCPTools()
    
    if not github_tools.github_token:
        print("❌ GITHUB_TOKEN not set!")
        return

    # Test 1: Get Repo Info
    print("\n1. Testing get_repo_info()...")
    repo_info = github_tools.get_repo_info()
    if "error" in repo_info:
        print(f"❌ Error: {repo_info['error']}")
    else:
        print(f"✅ Success! Repo: {repo_info.get('full_name')}")

    # Test 2: List Issues
    print("\n2. Testing list_issues()...")
    issues = github_tools.list_issues(state="open")
    if isinstance(issues, dict) and "error" in issues:
         print(f"❌ Error: {issues['error']}")
    else:
        print(f"✅ Success! Found {len(issues)} open issues.")
        if len(issues) > 0:
            print(f"   Sample issue: {issues[0].get('title')}")

if __name__ == "__main__":
    test_github_tools()

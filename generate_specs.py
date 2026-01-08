
import sys
import os
from pathlib import Path

# Add .claude/skills to python path
sys.path.append(str(Path.cwd() / ".claude" / "skills"))

try:
    from hackathon_todo_skill import HackathonTodoSkill
    
    print("🚀 Generating Specs for Phase IV...")
    skill = HackathonTodoSkill(project_root=".")
    
    # This will generate the spec, plan, and tasks files
    skill.execute_phase("Phase IV")
    
    print("\n✅ Phase IV Specs Generated Successfully!")
    
except ImportError as e:
    print(f"❌ Error importing skill: {e}")
except Exception as e:
    print(f"❌ An error occurred: {e}")

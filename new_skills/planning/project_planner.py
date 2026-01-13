"""
Project Planner Skill
Automatically creates comprehensive project plans with timelines, resource allocation, and risk assessments.
"""
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Set
from enum import Enum
import random

class TaskStatus(Enum):
    NOT_STARTED = "Not Started"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    BLOCKED = "Blocked"
    ON_HOLD = "On Hold"

class Priority(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

class ResourceType(Enum):
    HUMAN = "Human"
    EQUIPMENT = "Equipment"
    SOFTWARE = "Software"
    BUDGET = "Budget"

@dataclass
class TeamMember:
    id: str
    name: str
    role: str
    skills: List[str]
    availability_percentage: float  # 0-100
    current_workload: int  # Number of active tasks

@dataclass
class Resource:
    id: str
    name: str
    type: ResourceType
    quantity: int
    availability_start: datetime
    availability_end: datetime

@dataclass
class TaskDependency:
    predecessor_id: str
    successor_id: str
    dependency_type: str  # FS (Finish-Start), SS (Start-Start), FF (Finish-Finish), SF (Start-Finish)

@dataclass
class Risk:
    id: str
    description: str
    probability: float  # 0-1
    impact: float  # 0-1
    category: str
    mitigation_strategy: str

@dataclass
class ProjectTask:
    id: str
    name: str
    description: str
    duration_days: int
    assignee: Optional[TeamMember]
    priority: Priority
    status: TaskStatus
    dependencies: List[TaskDependency]
    resources_needed: List[Resource]
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    estimated_effort_hours: int = 0

@dataclass
class ProjectPlan:
    name: str
    description: str
    start_date: datetime
    end_date: datetime
    tasks: List[ProjectTask]
    team_members: List[TeamMember]
    resources: List[Resource]
    risks: List[Risk]
    milestones: List[Dict[str, any]]

class ProjectPlanner:
    """
    Skill to automatically create comprehensive project plans.
    """

    def __init__(self):
        self.risk_categories = [
            "Technical", "Schedule", "Resource", "Budget", "External", "Scope"
        ]

        self.mitigation_strategies = {
            "Technical": [
                "Conduct thorough testing", "Implement code reviews",
                "Use proven technologies", "Create technical prototypes"
            ],
            "Schedule": [
                "Add buffer time", "Parallelize tasks", "Fast-track critical path",
                "Adjust scope if needed"
            ],
            "Resource": [
                "Cross-train team members", "Hire additional staff",
                "Contract external help", "Reschedule tasks"
            ],
            "Budget": [
                "Identify cost-saving opportunities", "Negotiate better rates",
                "Optimize resource allocation", "Reduce scope"
            ],
            "External": [
                "Monitor external dependencies", "Have backup suppliers",
                "Maintain good stakeholder relationships", "Stay informed on regulations"
            ],
            "Scope": [
                "Define clear requirements", "Implement change control",
                "Regular stakeholder reviews", "Focus on MVP"
            ]
        }

    def estimate_task_duration(self, task_name: str, complexity: str = "medium") -> int:
        """
        Estimate task duration based on name and complexity.
        """
        base_duration = {
            "low": random.randint(1, 3),
            "medium": random.randint(3, 7),
            "high": random.randint(7, 14)
        }[complexity.lower()]

        # Adjust based on task name keywords
        if any(keyword in task_name.lower() for keyword in ["research", "design", "analysis"]):
            base_duration = int(base_duration * 1.5)
        elif any(keyword in task_name.lower() for keyword in ["bug", "fix", "patch"]):
            base_duration = max(1, int(base_duration * 0.7))
        elif any(keyword in task_name.lower() for keyword in ["review", "test", "qa"]):
            base_duration = int(base_duration * 1.2)

        return base_duration

    def identify_dependencies(self, tasks: List[ProjectTask]) -> List[TaskDependency]:
        """
        Identify task dependencies based on task names and logical relationships.
        """
        dependencies = []
        task_names = [task.name.lower() for task in tasks]

        for i, task in enumerate(tasks):
            for j, other_task in enumerate(tasks):
                if i == j:
                    continue

                # Identify common dependency patterns
                if ("design" in task.name.lower() and
                    "implement" in other_task.name.lower()) or \
                   ("specification" in task.name.lower() and
                    "develop" in other_task.name.lower()) or \
                   ("setup" in task.name.lower() and
                    ("develop" in other_task.name.lower() or
                     "test" in other_task.name.lower())):

                    # Task should finish before other_task starts
                    dependency = TaskDependency(
                        predecessor_id=task.id,
                        successor_id=other_task.id,
                        dependency_type="FS"
                    )
                    dependencies.append(dependency)

        return dependencies

    def allocate_resources(self, tasks: List[ProjectTask], team_members: List[TeamMember],
                          resources: List[Resource]) -> List[ProjectTask]:
        """
        Allocate team members and resources to tasks based on skills and availability.
        """
        # Sort tasks by priority (critical first)
        sorted_tasks = sorted(tasks, key=lambda t: t.priority.value, reverse=True)

        allocated_tasks = []
        member_workload = {member.id: member.current_workload for member in team_members}

        for task in sorted_tasks:
            # Try to assign a team member with relevant skills
            assigned_member = None
            for member in team_members:
                # Check if member has relevant skills
                relevant_skills = [skill for skill in member.skills
                                 if skill.lower() in task.name.lower() or
                                    skill.lower() in task.description.lower()]

                # Check availability
                if (member.availability_percentage > 0 and
                    member_workload[member.id] < (member.availability_percentage / 100) * 10):
                    assigned_member = member
                    member_workload[member.id] += 1
                    break

            # Assign the member to the task
            task.assignee = assigned_member
            allocated_tasks.append(task)

        return allocated_tasks

    def calculate_project_timeline(self, tasks: List[ProjectTask], dependencies: List[TaskDependency],
                                  start_date: datetime) -> List[ProjectTask]:
        """
        Calculate task start and end dates considering dependencies.
        """
        # Create a dependency graph
        dependency_map = {}
        for dep in dependencies:
            if dep.successor_id not in dependency_map:
                dependency_map[dep.successor_id] = []
            dependency_map[dep.successor_id].append(dep.predecessor_id)

        # Initialize all tasks with start date
        for task in tasks:
            task.start_date = start_date

        # Process tasks in dependency order
        processed_tasks = set()
        changed = True

        while changed:
            changed = False
            for task in tasks:
                if task.id in processed_tasks:
                    continue

                # Check if all dependencies are processed
                dependencies_met = True
                max_dependency_end = start_date

                if task.id in dependency_map:
                    for dep_id in dependency_map[task.id]:
                        dep_task = next((t for t in tasks if t.id == dep_id), None)
                        if dep_task and dep_task.id not in processed_tasks:
                            dependencies_met = False
                            break
                        elif dep_task:
                            # Calculate earliest possible start based on dependency
                            dep_end = dep_task.start_date + timedelta(days=dep_task.duration_days)
                            max_dependency_end = max(max_dependency_end, dep_end)

                if dependencies_met:
                    # Set start date to max dependency end date
                    task.start_date = max_dependency_end
                    task.end_date = task.start_date + timedelta(days=task.duration_days)
                    processed_tasks.add(task.id)
                    changed = True

        # If some tasks weren't processed (possible circular dependency), assign them a default date
        for task in tasks:
            if task.id not in processed_tasks:
                task.start_date = start_date
                task.end_date = task.start_date + timedelta(days=task.duration_days)

        return tasks

    def identify_risks(self, tasks: List[ProjectTask], team_members: List[TeamMember],
                      resources: List[Resource]) -> List[Risk]:
        """
        Identify potential project risks based on project characteristics.
        """
        risks = []

        # Technical risks
        if any("prototype" in task.name.lower() for task in tasks):
            risks.append(Risk(
                id=f"TECH_{len(risks)+1}",
                description="Prototype development may reveal technical challenges",
                probability=0.6,
                impact=0.7,
                category="Technical",
                mitigation_strategy=random.choice(self.mitigation_strategies["Technical"])
            ))

        # Resource risks
        overloaded_members = [m for m in team_members if m.current_workload > 8]
        if overloaded_members:
            risks.append(Risk(
                id=f"RES_{len(risks)+1}",
                description=f"{len(overloaded_members)} team members have high workload",
                probability=0.8,
                impact=0.5,
                category="Resource",
                mitigation_strategy=random.choice(self.mitigation_strategies["Resource"])
            ))

        # Schedule risks
        long_tasks = [task for task in tasks if task.duration_days > 10]
        if long_tasks:
            risks.append(Risk(
                id=f"SCHED_{len(risks)+1}",
                description=f"{len(long_tasks)} tasks have long duration (>10 days)",
                probability=0.4,
                impact=0.6,
                category="Schedule",
                mitigation_strategy=random.choice(self.mitigation_strategies["Schedule"])
            ))

        # Budget risks
        high_effort_tasks = [task for task in tasks if task.estimated_effort_hours > 40]
        if high_effort_tasks:
            risks.append(Risk(
                id=f"BUDG_{len(risks)+1}",
                description=f"{len(high_effort_tasks)} tasks have high effort estimate",
                probability=0.5,
                impact=0.4,
                category="Budget",
                mitigation_strategy=random.choice(self.mitigation_strategies["Budget"])
            ))

        # External risks
        if any("integration" in task.name.lower() for task in tasks):
            risks.append(Risk(
                id=f"EXT_{len(risks)+1}",
                description="Integration tasks may depend on external systems",
                probability=0.3,
                impact=0.8,
                category="External",
                mitigation_strategy=random.choice(self.mitigation_strategies["External"])
            ))

        # Generate additional risks based on team composition
        if len(team_members) < 3:
            risks.append(Risk(
                id=f"RES_{len(risks)+1}",
                description="Small team size may limit flexibility",
                probability=0.4,
                impact=0.5,
                category="Resource",
                mitigation_strategy=random.choice(self.mitigation_strategies["Resource"])
            ))

        return risks

    def create_milestones(self, tasks: List[ProjectTask], project_duration: int) -> List[Dict[str, any]]:
        """
        Create project milestones based on task completion.
        """
        milestones = []

        # Add initial milestone
        milestones.append({
            "name": "Project Kickoff",
            "date": tasks[0].start_date if tasks else datetime.now(),
            "description": "Project officially begins"
        })

        # Add intermediate milestones based on task completion percentages
        if project_duration > 7:  # Only add intermediate milestones for longer projects
            quarter_point = project_duration // 4
            half_point = project_duration // 2
            three_quarters = (project_duration * 3) // 4

            milestones.append({
                "name": "Quarter Point Review",
                "date": tasks[0].start_date + timedelta(days=quarter_point) if tasks else datetime.now(),
                "description": "Review progress at 25% completion"
            })

            milestones.append({
                "name": "Mid-Project Review",
                "date": tasks[0].start_date + timedelta(days=half_point) if tasks else datetime.now(),
                "description": "Review progress at 50% completion"
            })

            milestones.append({
                "name": "Three-Quarters Review",
                "date": tasks[0].start_date + timedelta(days=three_quarters) if tasks else datetime.now(),
                "description": "Review progress at 75% completion"
            })

        # Add final milestone
        end_date = max([task.end_date for task in tasks if task.end_date] or [datetime.now()])
        milestones.append({
            "name": "Project Completion",
            "date": end_date,
            "description": "Project deliverables completed and delivered"
        })

        return milestones

    def calculate_risk_score(self, risks: List[Risk]) -> float:
        """
        Calculate overall project risk score based on individual risks.
        """
        if not risks:
            return 0.0

        total_risk = sum(risk.probability * risk.impact for risk in risks)
        return min(total_risk / len(risks), 1.0)  # Normalize to 0-1 scale

    def generate_project_plan(self, project_name: str, project_description: str,
                           tasks_data: List[Dict], team_members: List[TeamMember],
                           resources: List[Resource], start_date: datetime) -> ProjectPlan:
        """
        Generate a comprehensive project plan.
        """
        # Create ProjectTask objects from input data
        tasks = []
        for i, task_data in enumerate(tasks_data):
            task = ProjectTask(
                id=f"T{i+1:03d}",
                name=task_data.get("name", f"Task {i+1}"),
                description=task_data.get("description", ""),
                duration_days=task_data.get("duration_days",
                                          self.estimate_task_duration(task_data.get("name", ""),
                                                                    task_data.get("complexity", "medium"))),
                assignee=None,  # Will be assigned later
                priority=Priority[task_data.get("priority", "MEDIUM").upper()],
                status=TaskStatus.NOT_STARTED,
                dependencies=[],
                resources_needed=[],
                estimated_effort_hours=task_data.get("estimated_effort_hours", 0)
            )
            tasks.append(task)

        # Identify dependencies
        dependencies = self.identify_dependencies(tasks)

        # Allocate resources
        tasks = self.allocate_resources(tasks, team_members, resources)

        # Calculate timeline
        tasks = self.calculate_project_timeline(tasks, dependencies, start_date)

        # Identify risks
        risks = self.identify_risks(tasks, team_members, resources)

        # Calculate project duration
        project_end_date = start_date
        if tasks:
            project_end_date = max(task.end_date for task in tasks if task.end_date)

        # Create milestones
        project_duration = (project_end_date - start_date).days
        milestones = self.create_milestones(tasks, project_duration)

        return ProjectPlan(
            name=project_name,
            description=project_description,
            start_date=start_date,
            end_date=project_end_date,
            tasks=tasks,
            team_members=team_members,
            resources=resources,
            risks=risks,
            milestones=milestones
        )

    def generate_plan_report(self, project_plan: ProjectPlan) -> str:
        """
        Generate a comprehensive project plan report.
        """
        report = f"# Project Plan: {project_plan.name}\n\n"
        report += f"**Description**: {project_plan.description}\n"
        report += f"**Duration**: {(project_plan.end_date - project_plan.start_date).days} days\n"
        report += f"**Start Date**: {project_plan.start_date.strftime('%Y-%m-%d')}\n"
        report += f"**End Date**: {project_plan.end_date.strftime('%Y-%m-%d')}\n\n"

        # Team overview
        report += f"## Team Members\n"
        for member in project_plan.team_members:
            report += f"- **{member.name}** ({member.role}): {member.availability_percentage}% availability, {member.current_workload} active tasks\n"
        report += "\n"

        # Task summary
        report += f"## Task Summary\n"
        for task in project_plan.tasks:
            assignee_name = task.assignee.name if task.assignee else "Unassigned"
            report += f"- **{task.name}** ({task.duration_days} days) - Assigned to: {assignee_name} - Priority: {task.priority.value}\n"
        report += "\n"

        # Critical path (simplified)
        critical_tasks = [task for task in project_plan.tasks if task.duration_days > 7]
        if critical_tasks:
            report += f"## Critical Tasks (>7 days)\n"
            for task in critical_tasks:
                assignee_name = task.assignee.name if task.assignee else "Unassigned"
                report += f"- **{task.name}** ({task.duration_days} days) - Assigned to: {assignee_name}\n"
            report += "\n"

        # Risks
        report += f"## Risk Assessment\n"
        risk_score = self.calculate_risk_score(project_plan.risks)
        report += f"**Overall Risk Score**: {risk_score:.2f}/1.0 ({'High' if risk_score > 0.6 else 'Medium' if risk_score > 0.3 else 'Low'})\n\n"

        if project_plan.risks:
            report += f"**Identified Risks**:\n"
            for risk in project_plan.risks:
                report += f"- **{risk.category}**: {risk.description} (Prob: {risk.probability:.1f}, Impact: {risk.impact:.1f})\n"
            report += "\n"
        else:
            report += f"**No major risks identified**\n\n"

        # Milestones
        report += f"## Key Milestones\n"
        for milestone in project_plan.milestones:
            report += f"- **{milestone['name']}** on {milestone['date'].strftime('%Y-%m-%d')}: {milestone['description']}\n"
        report += "\n"

        # Recommendations
        report += f"## Recommendations\n"
        if risk_score > 0.6:
            report += f"- High risk detected. Consider adding buffer time to critical tasks.\n"
        if len(critical_tasks) > 3:
            report += f"- Multiple long-duration tasks identified. Consider breaking down large tasks.\n"
        if len(project_plan.team_members) < 3:
            report += f"- Small team size identified. Consider cross-training or temporary help.\n"
        if not project_plan.risks:
            report += f"- Consider conducting a more thorough risk analysis.\n"

        report += f"\n*Report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"

        return report

def create_project_planner_skill():
    """Factory function to create the project planner skill."""
    return ProjectPlanner()

# Example usage
if __name__ == "__main__":
    # Example usage
    planner = create_project_planner_skill()

    # Define team members
    team = [
        TeamMember(id="TM001", name="Alice Johnson", role="Developer",
                  skills=["Python", "JavaScript", "API Development"],
                  availability_percentage=80, current_workload=2),
        TeamMember(id="TM002", name="Bob Smith", role="Designer",
                  skills=["UI/UX", "Figma", "Prototyping"],
                  availability_percentage=90, current_workload=1),
        TeamMember(id="TM003", name="Carol Davis", role="QA Engineer",
                  skills=["Testing", "Automation", "Manual Testing"],
                  availability_percentage=70, current_workload=0)
    ]

    # Define resources
    resources = [
        Resource(id="R001", name="Development Servers", type=ResourceType.EQUIPMENT,
                quantity=5, availability_start=datetime.now(),
                availability_end=datetime.now() + timedelta(days=60)),
        Resource(id="R002", name="Design Software License", type=ResourceType.SOFTWARE,
                quantity=3, availability_start=datetime.now(),
                availability_end=datetime.now() + timedelta(days=365))
    ]

    # Define tasks
    tasks_data = [
        {"name": "Requirements Gathering", "description": "Collect and analyze requirements",
         "complexity": "medium", "priority": "HIGH", "estimated_effort_hours": 16},
        {"name": "System Design", "description": "Create system architecture",
         "complexity": "high", "priority": "HIGH", "estimated_effort_hours": 24},
        {"name": "Frontend Development", "description": "Develop user interface",
         "complexity": "medium", "priority": "MEDIUM", "estimated_effort_hours": 40},
        {"name": "Backend Development", "description": "Develop server-side logic",
         "complexity": "high", "priority": "HIGH", "estimated_effort_hours": 60},
        {"name": "Testing", "description": "Test system functionality",
         "complexity": "medium", "priority": "MEDIUM", "estimated_effort_hours": 32},
        {"name": "Deployment", "description": "Deploy to production",
         "complexity": "low", "priority": "LOW", "estimated_effort_hours": 8}
    ]

    # Generate project plan
    plan = planner.generate_project_plan(
        project_name="New Web Application",
        project_description="Development of a new customer portal application",
        tasks_data=tasks_data,
        team_members=team,
        resources=resources,
        start_date=datetime.now()
    )

    # Generate report
    report = planner.generate_plan_report(plan)
    print(report)
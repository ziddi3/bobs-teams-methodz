"""
Bob's Teams Methodz - Workforce Engine
Main execution engine that coordinates all agents and manages task execution
"""

import os
import sys
import json
import time
from typing import Dict, Any, List, Optional

from . import config as _config
from .task_manager import TaskManager, TaskStatus
from .agents import (
    ResearcherAgent,
    DeveloperAgent,
    WriterAgent,
    DesignerAgent,
    AnalystAgent,
    ProjectManagerAgent
)


class WorkforceEngine:
    """Main engine for Bob's Teams Methodz coordination"""
    
    BRAND = _config.BRAND
    TAGLINE = _config.TAGLINE
    PACKAGE_DIR = _config.PACKAGE_DIR
    
    def __init__(self, keep_in_loop: bool = True):
        self.task_manager = TaskManager()
        self.keep_in_loop = keep_in_loop
        self.workforce_id = self._generate_workforce_id()
        self.workspace = _config.get_workspace()
        
        # Register all agents
        self.register_agents()
        
        print(f"\n{'='*60}")
        print(f"🎯 {self.BRAND} - {self.TAGLINE}")
        print(f"{'='*60}\n")
        self.print_team_status()
    
    def _generate_workforce_id(self) -> str:
        """Generate unique workforce ID"""
        import datetime
        return f"WF-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}"
    
    def _pkg_path(self, *parts) -> str:
        """Build a path inside the bobs_teams_methodz package directory"""
        return os.path.join(self.workspace, self.PACKAGE_DIR, *parts)
    
    def register_agents(self):
        """Register all available agents"""
        agents = [
            ResearcherAgent(),
            DeveloperAgent(),
            WriterAgent(),
            DesignerAgent(),
            AnalystAgent(),
            ProjectManagerAgent()
        ]
        
        for agent in agents:
            self.task_manager.register_agent(agent)
    
    def print_team_status(self):
        """Print current team status"""
        print(f"👥 Bob's Team:")
        print(f"{'─'*60}")
        
        for agent_name, agent in self.task_manager.agents.items():
            capabilities = ", ".join(agent.capabilities[:3])
            if len(agent.capabilities) > 3:
                capabilities += "..."
            
            print(f"  • {agent.name:20} {agent.role:30}")
            print(f"    Skills: {capabilities}")
        
        print(f"\n🎯 Team ID: {self.workforce_id}")
        print(f"{'='*60}\n")
    
    def submit_task(self, description: str, task_type: str = "general",
                    requirements: Dict[str, Any] = None) -> str:
        """Submit a new task to the workforce"""

        task_id = f"task-{len(self.task_manager.tasks) + 1}"

        print(f"\n📝 New Task Received")
        print(f"{'─'*60}")
        print(f"Task ID: {task_id}")
        print(f"Description: {description}")
        print(f"Type: {task_type}")

        # Create task in task manager
        self.task_manager.create_task(
            task_id=task_id,
            description=description,
            task_type=task_type,
            requirements=requirements or {}
        )

        print(f"📌 Task created successfully")

        return task_id
    
    def execute_autonomous(self, task_id: str = None):
        """Execute tasks autonomously"""
        
        print(f"\n{'='*60}")
        print(f"🔄 Autonomous Execution Mode")
        print(f"{'='*60}\n")
        
        # If no task_id provided, use the most recent task
        if task_id is None:
            if self.task_manager.tasks:
                task_id = list(self.task_manager.tasks.keys())[-1]
            else:
                print("❌ No task to execute. Submit a task first.")
                return None
        
        # Step 1: Plan the project
        print(f"Step 1/4: Planning Project")
        print(f"{'─'*60}")
        project_plan = self.plan_project(task_id)
        
        if not project_plan:
            print("❌ Project planning failed. Aborting execution.")
            return None
        
        # Step 2: Decompose tasks
        print(f"\nStep 2/4: Decomposing Tasks")
        print(f"{'─'*60}")
        tasks = self.decompose_tasks(project_plan)
        
        if not tasks:
            print("⚠️ No tasks decomposed. Delivering plan as-is.")
            return self.assemble_deliverable({}, project_plan)
        
        # Step 3: Execute tasks
        print(f"\nStep 3/4: Executing Tasks")
        print(f"{'─'*60}")
        results = self.execute_tasks(tasks)
        
        # Step 4: Assemble deliverables
        print(f"\nStep 4/4: Assembling Deliverables")
        print(f"{'─'*60}")
        deliverable = self.assemble_deliverable(results, project_plan)
        
        print(f"\n{'='*60}")
        print(f"✅ Execution Complete!")
        print(f"{'='*60}")
        print(f"📦 Deliverable: {deliverable}")
        
        return deliverable
    
    def plan_project(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Plan the project using Project Manager"""
        
        task = self.task_manager.get_task(task_id)
        if not task:
            print(f"❌ Task {task_id} not found")
            return None
        
        # Update task status
        self.task_manager.update_task_status(task_id, TaskStatus.IN_PROGRESS)
        
        # Get Project Manager agent
        pm_agent = self.task_manager.agents.get("ProjectManager")
        
        if not pm_agent:
            print("❌ Project Manager agent not found")
            return None
        
        # Create planning task
        planning_task = {
            "task_id": f"{task_id}_plan",
            "type": "project_plan",
            "description": task.description,
            "requirements": task.requirements or {}
        }
        
        # Execute planning
        print(f"  📋 Project Manager: Creating project plan...")
        result = pm_agent.process_task(planning_task)
        
        if result.get("success"):
            print(f"  ✅ Project plan created")
            project_plan = result.get("project_plan", {})
            
            # Save plan to context
            self.task_manager.update_context("current_project_plan", project_plan)
            
            return project_plan
        else:
            print(f"  ❌ Failed to create project plan: {result.get('error', 'Unknown error')}")
            return None
    
    def decompose_tasks(self, project_plan: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Decompose project plan into executable tasks"""
        
        if not project_plan:
            return []
        
        tasks = []
        phases = project_plan.get("phases", [])
        
        for phase in phases:
            phase_num = phase.get("phase", 0)
            phase_name = phase.get("name", "Unnamed Phase")
            phase_tasks = phase.get("tasks", [])
            task_count = 0
            
            for task_def in phase_tasks:
                task_key = task_def.get("task_id", f"task_{task_count}")
                
                # Create task in task manager
                task_id = f"{self.workforce_id}_phase{phase_num}_{task_key}"
                
                self.task_manager.create_task(
                    task_id=task_id,
                    description=task_def.get("description", ""),
                    task_type="general",
                    requirements={"agent": task_def.get("agent", "Developer")}
                )
                
                tasks.append({
                    "task_id": task_id,
                    "description": task_def.get("description", ""),
                    "agent": task_def.get("agent", "Developer"),
                    "phase": phase_num,
                    "phase_name": phase_name
                })
                
                task_count += 1
            
            print(f"  📦 Phase {phase_num} ({phase_name}): {task_count} tasks")
        
        print(f"  ✅ Total tasks decomposed: {len(tasks)}")
        return tasks
    
    def execute_tasks(self, tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Execute all tasks with appropriate agents"""
        
        results = {}
        
        for i, task_def in enumerate(tasks, 1):
            print(f"\n  [{i}/{len(tasks)}] Executing: {task_def['description']}")
            print(f"  Agent: {task_def['agent']}")
            
            # Get agent
            agent = self.task_manager.agents.get(task_def["agent"])
            if not agent:
                print(f"  ❌ Agent not found: {task_def['agent']}")
                results[task_def["task_id"]] = {
                    "success": False,
                    "error": f"Agent {task_def['agent']} not found"
                }
                continue
            
            # Update task status
            task_id = task_def["task_id"]
            self.task_manager.update_task_status(task_id, TaskStatus.IN_PROGRESS)
            
            # Execute task
            task_data = {
                "task_id": task_id,
                "description": task_def["description"],
                "type": "general",
                "requirements": {}
            }
            
            try:
                result = agent.process_task(task_data)
                
                # Save result
                if result.get("success"):
                    print(f"  ✅ Task completed")
                    self.task_manager.update_task_status(task_id, TaskStatus.COMPLETED, result)
                    
                    # Report progress
                    progress = self.task_manager.get_progress_summary()
                    print(f"  📊 Progress: {progress['progress_percentage']:.1f}% ({progress['completed']}/{progress['total_tasks']})")
                    
                    results[task_id] = result
                else:
                    error_msg = result.get("error", "Unknown error")
                    print(f"  ❌ Task failed: {error_msg}")
                    self.task_manager.update_task_status(task_id, TaskStatus.FAILED, error=error_msg)
                    results[task_id] = result
            except Exception as e:
                print(f"  ❌ Task exception: {str(e)}")
                self.task_manager.update_task_status(task_id, TaskStatus.FAILED, error=str(e))
                results[task_id] = {"success": False, "error": str(e)}
            
            # Check if user wants to be notified
            if self.keep_in_loop and (i % 3 == 0 or i == len(tasks)):
                self.show_summary(results)
        
        return results
    
    def assemble_deliverable(self, results: Dict[str, Any], project_plan: Dict[str, Any]) -> str:
        """Assemble final deliverable from all results"""
        
        # Create deliverable directory
        deliverable_dir = self._pkg_path("deliverables", self.workforce_id)
        os.makedirs(deliverable_dir, exist_ok=True)
        
        # Create summary report
        total_results = len(results)
        completed_count = sum(1 for r in results.values() if r.get("success"))
        failed_count = sum(1 for r in results.values() if not r.get("success"))
        
        report = {
            "workforce_id": self.workforce_id,
            "project_goal": project_plan.get("project_goal", "") if project_plan else "",
            "execution_summary": {
                "total_tasks": total_results,
                "completed": completed_count,
                "failed": failed_count
            },
            "results_by_phase": {},
            "deliverables": []
        }
        
        # Group results by phase
        for task_id, result in results.items():
            parts = task_id.split("_")
            if len(parts) >= 3:
                phase = parts[2]
                if phase not in report["results_by_phase"]:
                    report["results_by_phase"][phase] = []
                report["results_by_phase"][phase].append(result)
        
        # Save report
        report_file = os.path.join(deliverable_dir, "execution_report.json")
        try:
            with open(report_file, "w") as f:
                json.dump(report, f, indent=2)
            print(f"  📄 Execution report saved: {report_file}")
        except (OSError, IOError) as e:
            print(f"  ⚠️ Could not save report: {e}")
        
        # Create human-readable report
        human_report = self._generate_human_report(report)
        human_report_file = os.path.join(deliverable_dir, "report.md")
        try:
            with open(human_report_file, "w") as f:
                f.write(human_report)
            print(f"  📄 Human-readable report: {human_report_file}")
        except (OSError, IOError) as e:
            print(f"  ⚠️ Could not save report: {e}")
        
        return deliverable_dir
    
    def _generate_human_report(self, report: Dict[str, Any]) -> str:
        """Generate human-readable markdown report"""
        
        lines = []
        lines.append(f"# {self.BRAND} - Execution Report")
        lines.append(f"\n**Workforce ID:** {report['workforce_id']}")
        lines.append(f"**Project Goal:** {report['project_goal']}")
        lines.append(f"\n---\n")
        
        # Executive Summary
        lines.append(f"## Executive Summary")
        execution = report['execution_summary']
        lines.append(f"\n- **Total Tasks:** {execution['total_tasks']}")
        lines.append(f"- **Completed:** {execution['completed']}")
        lines.append(f"- **Failed:** {execution['failed']}")
        success_rate = (execution['completed']/execution['total_tasks']*100) if execution['total_tasks'] > 0 else 0
        lines.append(f"- **Success Rate:** {success_rate:.1f}%")
        
        # Phase Results
        if report.get('results_by_phase'):
            lines.append(f"\n## Results by Phase")
            for phase, results in report['results_by_phase'].items():
                lines.append(f"\n### {phase}")
                for result in results:
                    status = "✅" if result.get("success") else "❌"
                    lines.append(f"- {status} Task completed")
        
        # Deliverables
        if report.get('deliverables'):
            lines.append(f"\n## Deliverables")
            for deliverable in report['deliverables']:
                lines.append(f"- {deliverable}")
        
        lines.append(f"\n---\n")
        lines.append(f"*Generated by {self.BRAND} - {self.TAGLINE}*")
        
        return "\n".join(lines)
    
    def show_summary(self, results: Dict[str, Any] = None):
        """Show progress summary"""
        
        progress = self.task_manager.get_progress_summary()
        
        print(f"\n{'='*60}")
        print(f"📊 Progress Summary")
        print(f"{'='*60}")
        print(f"Total: {progress['total_tasks']} | "
              f"Completed: {progress['completed']} | "
              f"In Progress: {progress['in_progress']} | "
              f"Pending: {progress['pending']}")
        print(f"Progress: {progress['progress_percentage']:.1f}%")
        print(f"{'='*60}\n")
    
    def get_results(self) -> Dict[str, Any]:
        """Get all execution results"""
        return {
            "workforce_id": self.workforce_id,
            "progress": self.task_manager.get_progress_summary(),
            "tasks": {tid: t.to_dict() for tid, t in self.task_manager.tasks.items()},
            "context": self.task_manager.get_context()
        }

"""
Project Manager Agent
Coordinates all agents, plans projects, and manages workflow
"""

from typing import Dict, Any, List
import json
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ..agent_base import AgentBase


class ProjectManagerAgent(AgentBase):
    """Agent specialized in project management and coordination"""
    
    def __init__(self):
        capabilities = [
            "project_planning",
            "task_decomposition",
            "resource_allocation",
            "progress_tracking",
            "coordination",
            "quality_control"
        ]
        super().__init__("ProjectManager", "Project Management & Coordination", capabilities)
    
    def process_task(self, task: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process project management task"""
        self.update_status("working", task.get("task_id"))
        
        try:
            task_type = task.get("type", "management")
            
            if task_type == "project_plan":
                result = self.create_project_plan(task)
            elif task_type == "coordinate":
                result = self.coordinate_agents(task)
            elif task_type == "report_progress":
                result = self.report_progress(task)
            elif task_type == "quality_check":
                result = self.quality_check(task)
            else:
                result = self.management_assistance(task)
            
            self.update_status("idle")
            return result
            
        except Exception as e:
            self.log(f"Error processing task: {str(e)}", "error")
            self.update_status("idle")
            return {"error": str(e), "success": False}
    
    def create_project_plan(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Create comprehensive project plan"""
        project_goal = task.get("description", "")
        requirements = task.get("requirements", {})
        
        self.log(f"Creating project plan: {project_goal}")
        
        # Decompose project into phases and tasks
        project_plan = {
            "project_goal": project_goal,
            "phases": [],
            "required_agents": [],
            "timeline": {},
            "deliverables": []
        }
        
        # Determine approach based on project type
        project_type = self._determine_project_type(project_goal)
        
        # Create phases
        phases = self._create_phases(project_type)
        project_plan["phases"] = phases
        
        # Assign agents to tasks
        agent_assignments = self._assign_agents_to_tasks(phases)
        project_plan["required_agents"] = list(set([a["agent"] for a in agent_assignments]))
        
        # Estimate timeline
        timeline = self._estimate_timeline(phases)
        project_plan["timeline"] = timeline
        
        # Define deliverables
        deliverables = self._define_deliverables(project_type, phases)
        project_plan["deliverables"] = deliverables
        
        # Save project plan
        plan_file = os.path.join(self.workspace, "ai_workforce", "context", f"project_plan_{task.get('task_id')}.json")
        with open(plan_file, "w") as f:
            json.dump(project_plan, f, indent=2)
        
        return {
            "project_plan": project_plan,
            "agent_assignments": agent_assignments,
            "success": True
        }
    
    def coordinate_agents(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate agent work"""
        project_plan = task.get("project_plan", {})
        current_phase = task.get("current_phase", 1)
        
        self.log(f"Coordinating agents for phase {current_phase}")
        
        coordination_status = {
            "current_phase": current_phase,
            "active_agents": [],
            "completed_tasks": [],
            "pending_tasks": [],
            "next_actions": []
        }
        
        # Get tasks for current phase
        if current_phase <= len(project_plan.get("phases", [])):
            phase_tasks = project_plan["phases"][current_phase - 1].get("tasks", [])
            
            for task in phase_tasks:
                if task.get("status") == "completed":
                    coordination_status["completed_tasks"].append(task["task_id"])
                else:
                    coordination_status["pending_tasks"].append(task["task_id"])
                    coordination_status["active_agents"].append(task["assigned_agent"])
        
        return {
            "coordination_status": coordination_status,
            "success": True
        }
    
    def report_progress(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Report project progress"""
        self.log("Generating progress report")
        
        # Load project context if available
        context = task.get("context", {})
        
        progress_report = {
            "overall_progress": context.get("progress_percentage", 0),
            "completed_tasks": context.get("completed", 0),
            "total_tasks": context.get("total_tasks", 0),
            "active_agents": [],
            "tasks_in_progress": [],
            "blockers": [],
            "next_milestones": []
        }
        
        return {
            "progress_report": progress_report,
            "success": True
        }
    
    def quality_check(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Perform quality check on deliverables"""
        deliverables = task.get("deliverables", [])
        
        self.log(f"Performing quality check on {len(deliverables)} deliverables")
        
        quality_report = {
            "deliverables_checked": len(deliverables),
            "passed": 0,
            "failed": 0,
            "warnings": 0,
            "issues": [],
            "recommendations": []
        }
        
        for deliverable in deliverables:
            # Check if deliverable exists
            if deliverable.get("file_path"):
                if os.path.exists(os.path.join(self.workspace, deliverable["file_path"])):
                    quality_report["passed"] += 1
                else:
                    quality_report["failed"] += 1
                    quality_report["issues"].append({
                        "deliverable": deliverable["name"],
                        "issue": "File not found"
                    })
        
        return {
            "quality_report": quality_report,
            "success": True
        }
    
    def management_assistance(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """General management assistance"""
        description = task.get("description", "")
        
        self.log(f"Providing management assistance: {description}")
        
        assistance = {
            "recommendations": [],
            "best_practices": [],
            "next_steps": []
        }
        
        # Provide recommendations based on task
        if "workflow" in description.lower():
            assistance["recommendations"].extend([
                "Define clear project phases",
                "Assign appropriate agents to each task",
                "Set up regular checkpoints",
                "Maintain communication between agents"
            ])
            assistance["best_practices"].extend([
                "Start with research phase",
                "Iterate based on findings",
                "Document progress continuously",
                "Review deliverables before finalizing"
            ])
        
        return {
            "assistance": assistance,
            "success": True
        }
    
    def _determine_project_type(self, goal: str) -> str:
        """Determine project type from goal"""
        goal_lower = goal.lower()
        
        if any(keyword in goal_lower for keyword in ["website", "web app", "landing page", "ui"]):
            return "web_development"
        elif any(keyword in goal_lower for keyword in ["research", "study", "analysis", "report"]):
            return "research_project"
        elif any(keyword in goal_lower for keyword in ["content", "writing", "blog", "article"]):
            return "content_creation"
        elif any(keyword in goal_lower for keyword in ["data", "analytics", "analysis", "insights"]):
            return "data_analysis"
        elif any(keyword in goal_lower for keyword in ["design", "image", "visual", "graphic"]):
            return "design_project"
        else:
            return "general_project"
    
    def _create_phases(self, project_type: str) -> List[Dict[str, Any]]:
        """Create project phases based on type"""
        phase_templates = {
            "web_development": [
                {
                    "phase": 1,
                    "name": "Research & Planning",
                    "tasks": [
                        {"task_id": "research_requirements", "description": "Research requirements", "agent": "Researcher", "status": "pending"},
                        {"task_id": "plan_architecture", "description": "Plan architecture", "agent": "Developer", "status": "pending"}
                    ]
                },
                {
                    "phase": 2,
                    "name": "Design & Content",
                    "tasks": [
                        {"task_id": "design_ui", "description": "Design UI/UX", "agent": "Designer", "status": "pending"},
                        {"task_id": "create_content", "description": "Create content", "agent": "Writer", "status": "pending"}
                    ]
                },
                {
                    "phase": 3,
                    "name": "Development",
                    "tasks": [
                        {"task_id": "develop_frontend", "description": "Develop frontend", "agent": "Developer", "status": "pending"},
                        {"task_id": "test_functionality", "description": "Test functionality", "agent": "Developer", "status": "pending"}
                    ]
                },
                {
                    "phase": 4,
                    "name": "Deployment & Delivery",
                    "tasks": [
                        {"task_id": "deploy_site", "description": "Deploy site", "agent": "Developer", "status": "pending"},
                        {"task_id": "quality_check", "description": "Quality check", "agent": "ProjectManager", "status": "pending"}
                    ]
                }
            ],
            "research_project": [
                {
                    "phase": 1,
                    "name": "Topic Definition",
                    "tasks": [
                        {"task_id": "define_scope", "description": "Define research scope", "agent": "ProjectManager", "status": "pending"}
                    ]
                },
                {
                    "phase": 2,
                    "name": "Data Gathering",
                    "tasks": [
                        {"task_id": "conduct_research", "description": "Conduct research", "agent": "Researcher", "status": "pending"},
                        {"task_id": "extract_data", "description": "Extract data", "agent": "Researcher", "status": "pending"}
                    ]
                },
                {
                    "phase": 3,
                    "name": "Analysis & Reporting",
                    "tasks": [
                        {"task_id": "analyze_data", "description": "Analyze data", "agent": "Analyst", "status": "pending"},
                        {"task_id": "create_report", "description": "Create report", "agent": "Writer", "status": "pending"}
                    ]
                },
                {
                    "phase": 4,
                    "name": "Delivery",
                    "tasks": [
                        {"task_id": "format_deliverable", "description": "Format deliverable", "agent": "Writer", "status": "pending"},
                        {"task_id": "final_review", "description": "Final review", "agent": "ProjectManager", "status": "pending"}
                    ]
                }
            ],
            "general_project": [
                {
                    "phase": 1,
                    "name": "Planning",
                    "tasks": [
                        {"task_id": "plan_project", "description": "Plan project", "agent": "ProjectManager", "status": "pending"}
                    ]
                },
                {
                    "phase": 2,
                    "name": "Execution",
                    "tasks": [
                        {"task_id": "execute_tasks", "description": "Execute tasks", "agent": "Developer", "status": "pending"}
                    ]
                },
                {
                    "phase": 3,
                    "name": "Review",
                    "tasks": [
                        {"task_id": "review_work", "description": "Review work", "agent": "ProjectManager", "status": "pending"}
                    ]
                }
            ]
        }
        
        return phase_templates.get(project_type, phase_templates["general_project"])
    
    def _assign_agents_to_tasks(self, phases: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Assign agents to tasks"""
        assignments = []
        
        for phase in phases:
            for task in phase.get("tasks", []):
                assignments.append({
                    "task_id": task["task_id"],
                    "agent": task["agent"],
                    "phase": phase["phase"]
                })
        
        return assignments
    
    def _estimate_timeline(self, phases: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Estimate project timeline"""
        total_tasks = sum(len(phase.get("tasks", [])) for phase in phases)
        
        timeline = {
            "phases": len(phases),
            "total_tasks": total_tasks,
            "estimated_units": total_tasks * 10,  # Simplified estimation
            "milestones": [f"Phase {i}: {phase['name']}" for i, phase in enumerate(phases, 1)]
        }
        
        return timeline
    
    def _define_deliverables(self, project_type: str, phases: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Define project deliverables"""
        deliverables = []
        
        for i, phase in enumerate(phases, 1):
            if phase["name"] == "Execution" or phase["name"] == "Development" or phase["name"] == "Analysis & Reporting":
                deliverables.append({
                    "phase": i,
                    "name": f"{phase['name']} Output",
                    "type": "output"
                })
        
        # Final deliverable
        deliverables.append({
            "phase": len(phases),
            "name": "Final Deliverable",
            "type": "final"
        })
        
        return deliverables
"""
Task Manager for Bob's Teams Methodz
Manages task queue, distribution, and agent coordination
"""

import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum


class TaskStatus(Enum):
    """Task status enumeration"""
    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class Task:
    """Represents a single task"""
    
    def __init__(self, task_id: str, description: str, task_type: str, 
                 requirements: Dict[str, Any] = None, dependencies: List[str] = None):
        self.task_id = task_id
        self.description = description
        self.task_type = task_type
        self.requirements = requirements or {}
        self.dependencies = dependencies or []
        self.status = TaskStatus.PENDING
        self.assigned_agent = None
        self.created_at = datetime.now().isoformat()
        self.started_at = None
        self.completed_at = None
        self.result = None
        self.error = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary"""
        return {
            "task_id": self.task_id,
            "description": self.description,
            "type": self.task_type,
            "requirements": self.requirements,
            "dependencies": self.dependencies,
            "status": self.status.value,
            "assigned_agent": self.assigned_agent,
            "created_at": self.created_at,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "result": self.result,
            "error": self.error
        }


class TaskManager:
    """Manages tasks, agents, and coordination"""
    
    def __init__(self, workspace: str = "/workspace"):
        self.workspace = workspace
        self.tasks: Dict[str, Task] = {}
        self.agents = {}
        self.task_queue: List[str] = []
        self.completed_tasks: List[str] = []
        self.context = {}
        
        self.setup_directories()
    
    def setup_directories(self):
        """Create necessary directories"""
        dirs = [
            "bobs_teams_methodz/logs",
            "bobs_teams_methodz/results",
            "bobs_teams_methodz/context",
            "bobs_teams_methodz/tasks",
            "bobs_teams_methodz/deliverables"
        ]
        
        for dir_path in dirs:
            os.makedirs(os.path.join(self.workspace, dir_path), exist_ok=True)
    
    def register_agent(self, agent):
        """Register an agent with the task manager"""
        self.agents[agent.name] = agent
        print(f"✓ Agent registered: {agent.name} ({agent.role})")
    
    def create_task(self, task_id: str, description: str, task_type: str,
                    requirements: Dict[str, Any] = None, dependencies: List[str] = None) -> Task:
        """Create a new task"""
        task = Task(task_id, description, task_type, requirements, dependencies)
        self.tasks[task_id] = task
        self.task_queue.append(task_id)
        
        self.save_tasks()
        return task
    
    def assign_task(self, task_id: str, agent_name: str):
        """Assign a task to an agent"""
        if task_id not in self.tasks:
            raise ValueError(f"Task {task_id} not found")
        
        if agent_name not in self.agents:
            raise ValueError(f"Agent {agent_name} not found")
        
        task = self.tasks[task_id]
        task.status = TaskStatus.ASSIGNED
        task.assigned_agent = agent_name
        
        self.save_tasks()
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a task by ID"""
        return self.tasks.get(task_id)
    
    def update_task_status(self, task_id: str, status: TaskStatus, result: Any = None, error: str = None):
        """Update task status"""
        if task_id not in self.tasks:
            return
        
        task = self.tasks[task_id]
        task.status = status
        
        if status == TaskStatus.IN_PROGRESS and not task.started_at:
            task.started_at = datetime.now().isoformat()
        
        if status == TaskStatus.COMPLETED:
            task.completed_at = datetime.now().isoformat()
            task.result = result
            if task_id in self.task_queue:
                self.task_queue.remove(task_id)
            self.completed_tasks.append(task_id)
        
        if status == TaskStatus.FAILED:
            task.error = error
            if task_id in self.task_queue:
                self.task_queue.remove(task_id)
        
        self.save_tasks()
    
    def get_next_task(self, agent_name: str) -> Optional[Task]:
        """Get the next task for an agent"""
        # Check for tasks that can be started (dependencies met)
        available_tasks = []
        
        for task_id in self.task_queue:
            task = self.tasks[task_id]
            
            # Check if dependencies are completed
            dependencies_met = all(
                dep_id in self.completed_tasks 
                for dep_id in task.dependencies
            )
            
            if dependencies_met and task.status == TaskStatus.PENDING:
                available_tasks.append(task)
        
        if not available_tasks:
            return None
        
        # Select task based on agent capabilities (simple version - first available)
        # In a more sophisticated version, would match capabilities to task type
        task = available_tasks[0]
        self.assign_task(task.task_id, agent_name)
        
        return task
    
    def save_tasks(self):
        """Save tasks to file"""
        tasks_file = os.path.join(self.workspace, "ai_workforce", "tasks", "active_tasks.json")
        
        tasks_data = {
            "tasks": {task_id: task.to_dict() for task_id, task in self.tasks.items()},
            "queue": self.task_queue,
            "completed": self.completed_tasks
        }
        
        with open(tasks_file, "w") as f:
            json.dump(tasks_data, f, indent=2)
    
    def load_tasks(self):
        """Load tasks from file"""
        tasks_file = os.path.join(self.workspace, "ai_workforce", "tasks", "active_tasks.json")
        
        if not os.path.exists(tasks_file):
            return
        
        with open(tasks_file, "r") as f:
            tasks_data = json.load(f)
        
        self.tasks = {}
        for task_id, task_data in tasks_data["tasks"].items():
            task = Task(
                task_id,
                task_data["description"],
                task_data["type"],
                task_data["requirements"],
                task_data["dependencies"]
            )
            task.status = TaskStatus(task_data["status"])
            task.assigned_agent = task_data["assigned_agent"]
            task.created_at = task_data["created_at"]
            task.started_at = task_data["started_at"]
            task.completed_at = task_data["completed_at"]
            task.result = task_data["result"]
            task.error = task_data["error"]
            
            self.tasks[task_id] = task
        
        self.task_queue = tasks_data["queue"]
        self.completed_tasks = tasks_data["completed"]
    
    def update_context(self, key: str, value: Any):
        """Update global context"""
        self.context[key] = value
        
        context_file = os.path.join(self.workspace, "ai_workforce", "context", "global_context.json")
        with open(context_file, "w") as f:
            json.dump(self.context, f, indent=2)
    
    def get_context(self, key: str = None) -> Any:
        """Get context value or entire context"""
        if key:
            return self.context.get(key)
        return self.context
    
    def get_progress_summary(self) -> Dict[str, Any]:
        """Get summary of progress"""
        total_tasks = len(self.tasks)
        completed_tasks = len(self.completed_tasks)
        in_progress = sum(1 for t in self.tasks.values() if t.status == TaskStatus.IN_PROGRESS)
        pending_tasks = sum(1 for t in self.tasks.values() if t.status == TaskStatus.PENDING)
        failed_tasks = sum(1 for t in self.tasks.values() if t.status == TaskStatus.FAILED)
        
        return {
            "total_tasks": total_tasks,
            "completed": completed_tasks,
            "in_progress": in_progress,
            "pending": pending_tasks,
            "failed": failed_tasks,
            "progress_percentage": (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        }
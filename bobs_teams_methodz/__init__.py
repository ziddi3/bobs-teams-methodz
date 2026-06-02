"""
Bob's Teams Methodz
The Only Methodz - Autonomous AI Agent Collaboration System
"""

from .workforce_engine import WorkforceEngine as BobsTeams
from .task_manager import TaskManager, Task, TaskStatus

__version__ = "1.0.0"
__name__ = "Bob's Teams Methodz"
__tagline__ = "The Only Methodz"

__all__ = ["BobsTeams", "TaskManager", "Task", "TaskStatus"]
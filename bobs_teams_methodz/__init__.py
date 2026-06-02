"""
Bob's Teams Methodz
The Only Methodz - Autonomous AI Agent Collaboration System
"""

from .workforce_engine import WorkforceEngine as BobsTeams
from .task_manager import TaskManager, Task, TaskStatus
from . import config

__version__ = config.VERSION
__name__ = config.BRAND
__tagline__ = config.TAGLINE

__all__ = ["BobsTeams", "TaskManager", "Task", "TaskStatus", "config"]

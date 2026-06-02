"""
Base Agent Class for Bob's Teams Methodz
All Bob agents inherit from this base class
"""

import os
import json
import traceback
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from datetime import datetime
import time

from . import config as _config


class AgentBase(ABC):
    """Base class for all specialized AI agents"""
    
    BRAND = _config.BRAND
    PACKAGE_DIR = _config.PACKAGE_DIR
    
    def __init__(self, name: str, role: str, capabilities: List[str]):
        self.name = name
        self.role = role
        self.capabilities = capabilities
        self.status = "idle"
        self.current_task = None
        self.tasks_completed = []
        self.workspace = _config.get_workspace()
        self.brand = self.BRAND
        
    @abstractmethod
    def process_task(self, task: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process a task and return results"""
        pass
    
    def _pkg_path(self, *parts) -> str:
        """Build a path inside the bobs_teams_methodz package directory"""
        return os.path.join(self.workspace, self.PACKAGE_DIR, *parts)
    
    def log(self, message: str, level: str = "info"):
        """Log a message with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{self.name}] [{level.upper()}] {message}"
        
        log_file = self._pkg_path("logs", f"{self.name.lower()}.log")
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        with open(log_file, "a") as f:
            f.write(log_entry + "\n")
        
        print(log_entry)
        
    def update_status(self, status: str, task: Optional[str] = None):
        """Update agent status"""
        self.status = status
        self.current_task = task
        self.log(f"Status changed to: {status}" + (f" (task: {task})" if task else ""))
        
    def save_result(self, task_id: str, result: Dict[str, Any]):
        """Save task result to file"""
        results_dir = self._pkg_path("results")
        os.makedirs(results_dir, exist_ok=True)
        
        result_file = os.path.join(results_dir, f"{task_id}_{self.name.lower()}_result.json")
        
        result_data = {
            "task_id": task_id,
            "agent": self.name,
            "role": self.role,
            "timestamp": datetime.now().isoformat(),
            "result": result
        }
        
        with open(result_file, "w") as f:
            json.dump(result_data, f, indent=2)
        
        self.log(f"Result saved to {result_file}")
    
    def load_context(self, context_file: str) -> Dict[str, Any]:
        """Load context from file"""
        context_path = self._pkg_path("context", context_file)
        
        if os.path.exists(context_path):
            with open(context_path, "r") as f:
                return json.load(f)
        
        return {}
    
    def save_context(self, context_file: str, context: Dict[str, Any]):
        """Save context to file"""
        context_dir = self._pkg_path("context")
        os.makedirs(context_dir, exist_ok=True)
        
        context_path = os.path.join(context_dir, context_file)
        
        with open(context_path, "w") as f:
            json.dump(context, f, indent=2)
        
        self.log(f"Context saved to {context_file}")
    
    def execute_with_retry(self, func, max_retries: int = 3, retry_delay: int = 2):
        """Execute function with retry logic"""
        for attempt in range(max_retries):
            try:
                return func()
            except Exception as e:
                if attempt == max_retries - 1:
                    self.log(f"Failed after {max_retries} attempts: {str(e)}", "error")
                    raise
                
                self.log(f"Attempt {attempt + 1} failed: {str(e)}, retrying...", "warning")
                time.sleep(retry_delay)
        return None
    
    def get_file_content(self, file_path: str) -> str:
        """Read file content"""
        full_path = os.path.join(self.workspace, file_path)
        
        if os.path.exists(full_path):
            with open(full_path, "r") as f:
                return f.read()
        
        self.log(f"File not found: {file_path}", "warning")
        return ""
    
    def save_file_content(self, file_path: str, content: str):
        """Save content to file"""
        full_path = os.path.join(self.workspace, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        with open(full_path, "w") as f:
            f.write(content)
        
        self.log(f"File saved: {file_path}")

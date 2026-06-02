"""
Developer Agent for Bob's Teams Methodz
Specializes in code generation, testing, and deployment
"""

from typing import Dict, Any
import json
import os

from ..agent_base import AgentBase


class DeveloperAgent(AgentBase):
    """Agent specialized in development tasks"""
    
    def __init__(self):
        capabilities = [
            "code_generation",
            "code_review",
            "testing",
            "debugging",
            "deployment",
            "file_operations"
        ]
        super().__init__("Developer", "Development Specialist", capabilities)
    
    def process_task(self, task: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process development task"""
        self.update_status("working", task.get("task_id"))
        
        try:
            task_type = task.get("type", "development")
            
            if task_type == "code_generation":
                result = self.generate_code(task)
            elif task_type == "code_review":
                result = self.review_code(task)
            elif task_type == "testing":
                result = self.run_tests(task)
            elif task_type == "deployment":
                result = self.deploy(task)
            elif task_type == "file_create":
                result = self.create_file(task)
            else:
                result = self.development_assistance(task)
            
            self.update_status("idle")
            return result
            
        except Exception as e:
            self.log(f"Error processing task: {str(e)}", "error")
            self.update_status("idle")
            return {"error": str(e), "success": False}
    
    def generate_code(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Generate code based on requirements"""
        requirements = task.get("requirements", {})
        language = requirements.get("language", "python")
        description = task.get("description", "")
        
        self.log(f"Generating {language} code: {description}")
        
        code_spec = {
            "language": language,
            "description": description,
            "requirements": requirements,
            "code": "",
            "file_path": requirements.get("file_path", ""),
            "dependencies": [],
            "needs_generation": True,
            "task_id": task.get("task_id")
        }
        
        self.save_context(f"code_spec_{task.get('task_id')}.json", code_spec)
        
        return {
            "action_required": "generate_code",
            "spec": code_spec,
            "language": language,
            "success": True
        }
    
    def review_code(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Review code"""
        file_path = task.get("file_path", "")
        
        self.log(f"Reviewing code: {file_path}")
        
        code_content = self.get_file_content(file_path)
        
        if not code_content:
            return {
                "error": "File not found or empty",
                "success": False
            }
        
        review_result = {
            "file_path": file_path,
            "lines_of_code": len(code_content.split("\n")),
            "issues": [],
            "suggestions": [],
            "quality_score": 0
        }
        
        lines = code_content.split("\n")
        
        for i, line in enumerate(lines, 1):
            if "TODO" in line or "FIXME" in line:
                review_result["issues"].append({
                    "line": i,
                    "type": "comment",
                    "message": "Contains TODO/FIXME comment"
                })
            
            if len(line) > 120:
                review_result["issues"].append({
                    "line": i,
                    "type": "style",
                    "message": "Line exceeds 120 characters"
                })
        
        base_score = 100
        review_result["quality_score"] = max(0, base_score - len(review_result["issues"]) * 5)
        
        return {
            "review": review_result,
            "success": True
        }
    
    def run_tests(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Run tests"""
        test_type = task.get("test_type", "unit")
        test_files = task.get("test_files", [])
        
        self.log(f"Running {test_type} tests on {len(test_files)} files")
        
        test_params = {
            "action": "run_tests",
            "test_type": test_type,
            "files": test_files,
            "task_id": task.get("task_id")
        }
        
        self.save_context(f"test_{task.get('task_id')}.json", test_params)
        
        return {
            "action_required": "run_tests",
            "params": test_params,
            "test_type": test_type,
            "success": True
        }
    
    def deploy(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Deploy application"""
        deploy_type = task.get("deploy_type", "static")
        directory = task.get("directory", "")
        name = task.get("name", "")
        
        self.log(f"Deploying {deploy_type} from {directory} as {name}")
        
        deploy_params = {
            "action": "deploy",
            "type": deploy_type,
            "directory": directory,
            "name": name,
            "task_id": task.get("task_id")
        }
        
        return {
            "action_required": "deploy",
            "params": deploy_params,
            "success": True
        }
    
    def create_file(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Create a file with content"""
        file_path = task.get("file_path", "")
        content = task.get("content", "")
        
        self.log(f"Creating file: {file_path}")
        
        if content:
            self.save_file_content(file_path, content)
        
        return {
            "file_path": file_path,
            "file_size": len(content),
            "success": True
        }
    
    def development_assistance(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """General development assistance"""
        description = task.get("description", "")
        
        self.log(f"Providing development assistance: {description}")
        
        dev_plan = {
            "task": description,
            "steps": [
                "Analyze requirements",
                "Design solution architecture",
                "Implement code",
                "Test implementation",
                "Document code"
            ],
            "recommended_actions": []
        }
        
        if "web" in description.lower():
            dev_plan["recommended_actions"].append("Create HTML/CSS/JS files")
            dev_plan["recommended_actions"].append("Test browser compatibility")
        
        if "data" in description.lower():
            dev_plan["recommended_actions"].append("Process data with Python")
            dev_plan["recommended_actions"].append("Generate visualizations")
        
        return {
            "development_plan": dev_plan,
            "success": True
        }

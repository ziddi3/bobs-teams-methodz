"""
Writer Agent
Specializes in content creation, documentation, and writing
"""

from typing import Dict, Any
import json
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ..agent_base import AgentBase


class WriterAgent(AgentBase):
    """Agent specialized in writing tasks"""
    
    def __init__(self):
        capabilities = [
            "content_creation",
            "documentation",
            "copywriting",
            "editing",
            "summarization",
            "blog_writing"
        ]
        super().__init__("Writer", "Content Specialist", capabilities)
    
    def process_task(self, task: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process writing task"""
        self.update_status("working", task.get("task_id"))
        
        try:
            task_type = task.get("type", "writing")
            
            if task_type == "content_creation":
                result = self.create_content(task)
            elif task_type == "documentation":
                result = self.create_documentation(task)
            elif task_type == "summary":
                result = self.create_summary(task)
            elif task_type == "editing":
                result = self.edit_content(task)
            else:
                result = self.assistance(task)
            
            self.update_status("idle")
            return result
            
        except Exception as e:
            self.log(f"Error processing task: {str(e)}", "error")
            self.update_status("idle")
            return {"error": str(e), "success": False}
    
    def create_content(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Create content based on requirements"""
        requirements = task.get("requirements", {})
        content_type = requirements.get("content_type", "article")
        topic = task.get("description", "")
        tone = requirements.get("tone", "professional")
        target_audience = requirements.get("target_audience", "general")
        word_count = requirements.get("word_count", 1000)
        
        self.log(f"Creating {content_type}: {topic}")
        
        content_spec = {
            "content_type": content_type,
            "topic": topic,
            "tone": tone,
            "target_audience": target_audience,
            "word_count": word_count,
            "requirements": requirements,
            "content": "",
            "file_path": requirements.get("file_path", ""),
            "task_id": task.get("task_id")
        }
        
        # Mark that content creation is needed
        content_spec["needs_creation"] = True
        
        # Save spec for later use
        spec_file = os.path.join(self.workspace, "ai_workforce", "context", f"content_spec_{task.get('task_id')}.json")
        with open(spec_file, "w") as f:
            json.dump(content_spec, f, indent=2)
        
        return {
            "action_required": "create_content",
            "spec": content_spec,
            "content_type": content_type,
            "success": True
        }
    
    def create_documentation(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Create documentation"""
        doc_type = task.get("doc_type", "user_guide")
        subject = task.get("description", "")
        
        self.log(f"Creating {doc_type}: {subject}")
        
        doc_structure = self._get_documentation_structure(doc_type)
        
        doc_spec = {
            "doc_type": doc_type,
            "subject": subject,
            "structure": doc_structure,
            "content": {},
            "file_path": task.get("file_path", ""),
            "task_id": task.get("task_id")
        }
        
        doc_spec["needs_creation"] = True
        
        spec_file = os.path.join(self.workspace, "ai_workforce", "context", f"doc_spec_{task.get('task_id')}.json")
        with open(spec_file, "w") as f:
            json.dump(doc_spec, f, indent=2)
        
        return {
            "action_required": "create_documentation",
            "spec": doc_spec,
            "doc_type": doc_type,
            "success": True
        }
    
    def create_summary(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Create summary of content"""
        source_content = task.get("content", "")
        summary_type = task.get("summary_type", "executive")
        
        self.log(f"Creating {summary_type} summary")
        
        summary = self._generate_summary(source_content, summary_type)
        
        # Save summary to file if path specified
        file_path = task.get("file_path")
        if file_path:
            self.save_file_content(file_path, summary)
        
        return {
            "summary": summary,
            "summary_type": summary_type,
            "original_length": len(source_content),
            "summary_length": len(summary),
            "success": True
        }
    
    def edit_content(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Edit and improve content"""
        content = task.get("content", "")
        edit_type = task.get("edit_type", "proofread")
        
        self.log(f"Editing content: {edit_type}")
        
        edited_content = self._edit_content(content, edit_type)
        
        # Save edited content if path specified
        file_path = task.get("file_path")
        if file_path:
            self.save_file_content(file_path, edited_content)
        
        changes_made = {
            "grammar_fixes": self._count_grammar_fixes(content, edited_content),
            "style_improvements": self._count_style_improvements(content, edited_content),
            "clarity_enhancements": self._count_clarity_changes(content, edited_content)
        }
        
        return {
            "edited_content": edited_content,
            "edit_type": edit_type,
            "changes_made": changes_made,
            "success": True
        }
    
    def assistance(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """General writing assistance"""
        description = task.get("description", "")
        
        self.log(f"Providing writing assistance: {description}")
        
        writing_plan = {
            "task": description,
            "suggestions": [],
            "outline": []
        }
        
        # Analyze task and provide suggestions
        if "article" in description.lower():
            writing_plan["outline"] = [
                "Introduction",
                "Background",
                "Main Points (3-5 key sections)",
                "Analysis",
                "Conclusion"
            ]
            writing_plan["suggestions"].append("Use compelling headlines")
            writing_plan["suggestions"].append("Include relevant examples")
        
        elif "blog" in description.lower():
            writing_plan["outline"] = [
                "Hook/Opening",
                "Main content with subheadings",
                "Takeaway points",
                "Call to action"
            ]
            writing_plan["suggestions"].append("Use conversational tone")
            writing_plan["suggestions"].append("Optimize for SEO keywords")
        
        return {
            "writing_plan": writing_plan,
            "success": True
        }
    
    def _get_documentation_structure(self, doc_type: str) -> Dict[str, Any]:
        """Get structure for documentation type"""
        structures = {
            "user_guide": {
                "sections": [
                    "Introduction",
                    "Getting Started",
                    "Features",
                    "How-to Guides",
                    "FAQ",
                    "Troubleshooting",
                    "Support"
                ],
                "format": "markdown"
            },
            "technical_documentation": {
                "sections": [
                    "Overview",
                    "Architecture",
                    "API Reference",
                    "Configuration",
                    "Examples",
                    "Best Practices"
                ],
                "format": "markdown"
            },
            "readme": {
                "sections": [
                    "Title",
                    "Description",
                    "Installation",
                    "Usage",
                    "Features",
                    "Contributing",
                    "License"
                ],
                "format": "markdown"
            }
        }
        
        return structures.get(doc_type, structures["user_guide"])
    
    def _generate_summary(self, content: str, summary_type: str) -> str:
        """Generate summary based on type"""
        if not content:
            return ""
        
        if summary_type == "executive":
            # Executive summary: brief, high-level
            sentences = content.split(". ")
            key_sentences = sentences[:3]
            return ". ".join(key_sentences) + "."
        
        elif summary_type == "detailed":
            # Detailed summary: more comprehensive
            paragraphs = content.split("\n\n")
            if len(paragraphs) >= 2:
                return paragraphs[0] + "\n\n" + paragraphs[-1]
            return content[:500] + "..."
        
        else:
            # Standard summary
            return content[:300] + "..."
    
    def _edit_content(self, content: str, edit_type: str) -> str:
        """Edit content based on type"""
        if edit_type == "proofread":
            # Basic proofreading
            # Fix common issues (simplified)
            edited = content.replace("  ", " ")  # Double spaces
            edited = edited.replace("\n\n\n", "\n\n")  # Multiple blank lines
            return edited
        
        elif edit_type == "style":
            # Style improvements
            # Add transitional phrases where needed
            return content
        
        else:
            return content
    
    def _count_grammar_fixes(self, original: str, edited: str) -> int:
        """Count grammar fixes (simplified)"""
        return abs(len(original.split()) - len(edited.split()))
    
    def _count_style_improvements(self, original: str, edited: str) -> int:
        """Count style improvements"""
        return 0  # Placeholder
    
    def _count_clarity_changes(self, original: str, edited: str) -> int:
        """Count clarity enhancements"""
        return 0  # Placeholder
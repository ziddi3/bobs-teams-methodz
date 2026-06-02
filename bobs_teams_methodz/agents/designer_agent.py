"""
Designer Agent
Specializes in visual design, layouts, and creative work
"""

from typing import Dict, Any, List
import json
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ..agent_base import AgentBase


class DesignerAgent(AgentBase):
    """Agent specialized in design tasks"""
    
    def __init__(self):
        capabilities = [
            "image_generation",
            "graphic_design",
            "layout_design",
            "ui_design",
            "visual_consulting",
            "presentation_design"
        ]
        super().__init__("Designer", "Design Specialist", capabilities)
    
    def process_task(self, task: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process design task"""
        self.update_status("working", task.get("task_id"))
        
        try:
            task_type = task.get("type", "design")
            
            if task_type == "image_generation":
                result = self.generate_image(task)
            elif task_type == "layout_design":
                result = self.design_layout(task)
            elif task_type == "ui_design":
                result = self.design_ui(task)
            elif task_type == "presentation":
                result = self.design_presentation(task)
            else:
                result = self.design_assistance(task)
            
            self.update_status("idle")
            return result
            
        except Exception as e:
            self.log(f"Error processing task: {str(e)}", "error")
            self.update_status("idle")
            return {"error": str(e), "success": False}
    
    def generate_image(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Generate or edit images"""
        requirements = task.get("requirements", {})
        prompt = requirements.get("prompt", task.get("description", ""))
        image_type = requirements.get("image_type", "original")
        source_file = requirements.get("source_file", "")
        size = requirements.get("size", "1024x1024")
        
        self.log(f"Generating image: {prompt[:50]}...")
        
        image_spec = {
            "prompt": prompt,
            "image_type": image_type,
            "source_file": source_file,
            "size": size,
            "requirements": requirements,
            "task_id": task.get("task_id")
        }
        
        # Determine action needed
        if image_type == "edit" and source_file:
            image_spec["action"] = "edit_image"
        else:
            image_spec["action"] = "generate_image"
        
        # Save spec for later use
        spec_file = os.path.join(self.workspace, "ai_workforce", "context", f"image_spec_{task.get('task_id')}.json")
        with open(spec_file, "w") as f:
            json.dump(image_spec, f, indent=2)
        
        return {
            "action_required": image_spec["action"],
            "spec": image_spec,
            "prompt": prompt[:100],
            "success": True
        }
    
    def design_layout(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Design layout (HTML/CSS)"""
        requirements = task.get("requirements", {})
        layout_type = requirements.get("layout_type", "webpage")
        content = task.get("description", "")
        
        self.log(f"Designing {layout_type} layout")
        
        layout_spec = {
            "layout_type": layout_type,
            "content": content,
            "requirements": requirements,
            "structure": self._get_layout_structure(layout_type),
            "styles": self._get_style_guidelines(layout_type),
            "file_path": requirements.get("file_path", ""),
            "task_id": task.get("task_id")
        }
        
        layout_spec["needs_creation"] = True
        
        spec_file = os.path.join(self.workspace, "ai_workforce", "context", f"layout_spec_{task.get('task_id')}.json")
        with open(spec_file, "w") as f:
            json.dump(layout_spec, f, indent=2)
        
        return {
            "action_required": "create_layout",
            "spec": layout_spec,
            "layout_type": layout_type,
            "success": True
        }
    
    def design_ui(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Design user interface"""
        ui_type = task.get("ui_type", "web")
        description = task.get("description", "")
        
        self.log(f"Designing UI: {ui_type}")
        
        ui_spec = {
            "ui_type": ui_type,
            "description": description,
            "components": self._get_ui_components(ui_type),
            "principles": self._get_design_principles(),
            "task_id": task.get("task_id")
        }
        
        return {
            "ui_design_plan": ui_spec,
            "success": True
        }
    
    def design_presentation(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Design presentation"""
        topic = task.get("description", "")
        slides_count = task.get("slides_count", 5)
        
        self.log(f"Designing presentation: {topic}")
        
        presentation_spec = {
            "topic": topic,
            "slides_count": slides_count,
            "structure": self._get_presentation_structure(slides_count),
            "design_guidelines": self._get_presentation_guidelines(),
            "task_id": task.get("task_id")
        }
        
        spec_file = os.path.join(self.workspace, "ai_workforce", "context", f"presentation_spec_{task.get('task_id')}.json")
        with open(spec_file, "w") as f:
            json.dump(presentation_spec, f, indent=2)
        
        return {
            "action_required": "create_presentation",
            "spec": presentation_spec,
            "success": True
        }
    
    def design_assistance(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """General design assistance"""
        description = task.get("description", "")
        
        self.log(f"Providing design assistance: {description}")
        
        design_advice = {
            "task": description,
            "best_practices": [],
            "tools": [],
            "inspiration": []
        }
        
        # Provide design advice based on task
        if "web" in description.lower():
            design_advice["best_practices"].extend([
                "Use responsive design",
                "Ensure accessibility",
                "Optimize loading speed",
                "Maintain visual hierarchy"
            ])
            design_advice["tools"] = ["Figma", "Adobe XD", "Sketch"]
        
        if "image" in description.lower():
            design_advice["best_practices"].extend([
                "Use high-resolution images",
                "Maintain consistent style",
                "Optimize file sizes",
                "Consider color theory"
            ])
        
        return {
            "design_advice": design_advice,
            "success": True
        }
    
    def _get_layout_structure(self, layout_type: str) -> Dict[str, Any]:
        """Get structure for layout type"""
        structures = {
            "webpage": {
                "sections": ["header", "hero", "content", "footer"],
                "grid": True,
                "responsive": True
            },
            "dashboard": {
                "sections": ["sidebar", "topbar", "widgets", "content"],
                "grid": True,
                "responsive": True
            },
            "landing_page": {
                "sections": ["hero", "features", "testimonials", "cta", "footer"],
                "full_width": True,
                "scroll_styling": True
            }
        }
        
        return structures.get(layout_type, structures["webpage"])
    
    def _get_style_guidelines(self, layout_type: str) -> Dict[str, Any]:
        """Get style guidelines"""
        return {
            "color_scheme": "modern",
            "typography": "clean",
            "spacing": "consistent",
            "animations": "subtle"
        }
    
    def _get_ui_components(self, ui_type: str) -> List[str]:
        """Get UI components list"""
        components = {
            "web": ["navigation", "buttons", "forms", "modals", "cards"],
            "mobile": ["bottom_navigation", "tabs", "swipe_gestures", "touch_targets"],
            "desktop": ["menus", "toolbars", "panels", "notifications"]
        }
        
        return components.get(ui_type, components["web"])
    
    def _get_design_principles(self) -> List[str]:
        """Get design principles"""
        return [
            "Visual hierarchy",
            "Consistency",
            "Feedback",
            "Accessibility",
            "Efficiency"
        ]
    
    def _get_presentation_structure(self, slides_count: int) -> List[Dict[str, Any]]:
        """Get presentation structure"""
        structure = [
            {"slide": 1, "type": "title", "content": "Title and subtitle"},
            {"slide": 2, "type": "agenda", "content": "Table of contents"}
        ]
        
        # Add content slides
        for i in range(3, slides_count):
            structure.append({
                "slide": i,
                "type": "content",
                "content": f"Content slide {i-2}"
            })
        
        # Add closing slide
        structure.append({
            "slide": slides_count,
            "type": "closing",
            "content": "Thank you and Q&A"
        })
        
        return structure
    
    def _get_presentation_guidelines(self) -> Dict[str, Any]:
        """Get presentation design guidelines"""
        return {
            "slide_limit": "one_idea_per_slide",
            "text_ratio": "max_6_words_per_line",
            "visual_ratio": "balance_text_and_images",
            "color_scheme": "consistent_across_slides"
        }
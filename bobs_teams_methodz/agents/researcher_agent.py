"""
Researcher Agent
Specializes in web research, data gathering, information extraction
"""

from typing import Dict, Any
import json
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ..agent_base import AgentBase


class ResearcherAgent(AgentBase):
    """Agent specialized in research and information gathering"""
    
    def __init__(self):
        capabilities = [
            "web_search",
            "web_scraping",
            "data_extraction",
            "source_verification",
            "information_synthesis"
        ]
        super().__init__("Researcher", "Research Specialist", capabilities)
    
    def process_task(self, task: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process research task"""
        self.update_status("working", task.get("task_id"))
        
        try:
            task_type = task.get("type", "research")
            
            if task_type == "web_search":
                result = self.perform_web_search(task)
            elif task_type == "web_scrape":
                result = self.perform_web_scrape(task)
            elif task_type == "data_extraction":
                result = self.perform_data_extraction(task)
            else:
                result = self.perform_general_research(task)
            
            self.update_status("idle")
            return result
            
        except Exception as e:
            self.log(f"Error processing task: {str(e)}", "error")
            self.update_status("idle")
            return {"error": str(e), "success": False}
    
    def perform_web_search(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Perform web search"""
        query = task.get("query", "")
        num_results = task.get("num_results", 10)
        
        self.log(f"Performing web search for: {query}")
        
        # Trigger web search - this will be handled by the main system
        search_results = {
            "query": query,
            "results": [],
            "summary": "",
            "sources": []
        }
        
        # Save search parameters for the main system to execute
        search_params = {
            "action": "web_search",
            "query": query,
            "num_results": num_results,
            "task_id": task.get("task_id")
        }
        
        params_file = os.path.join(self.workspace, "ai_workforce", "context", f"search_{task.get('task_id')}.json")
        with open(params_file, "w") as f:
            json.dump(search_params, f, indent=2)
        
        self.log(f"Search parameters saved. Execute: web_search with query '{query}'")
        
        return {
            "action_required": "web_search",
            "params": search_params,
            "query": query,
            "success": True
        }
    
    def perform_web_scrape(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Perform web scraping"""
        urls = task.get("urls", [])
        
        self.log(f"Preparing to scrape {len(urls)} URLs")
        
        scrape_params = {
            "action": "web_scrape",
            "urls": urls,
            "task_id": task.get("task_id")
        }
        
        params_file = os.path.join(self.workspace, "ai_workforce", "context", f"scrape_{task.get('task_id')}.json")
        with open(params_file, "w") as f:
            json.dump(scrape_params, f, indent=2)
        
        return {
            "action_required": "web_scrape",
            "params": scrape_params,
            "urls": urls,
            "success": True
        }
    
    def perform_data_extraction(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Perform data extraction from content"""
        content = task.get("content", "")
        extraction_type = task.get("extraction_type", "summary")
        
        self.log(f"Extracting data: type={extraction_type}")
        
        result = {
            "extraction_type": extraction_type,
            "extracted_data": {},
            "content_length": len(content) if content else 0
        }
        
        if extraction_type == "summary":
            # Extract key points from content
            result["extracted_data"] = {
                "summary": self._generate_summary(content),
                "key_points": self._extract_key_points(content)
            }
        elif extraction_type == "entities":
            result["extracted_data"] = {
                "entities": self._extract_entities(content)
            }
        elif extraction_type == "facts":
            result["extracted_data"] = {
                "facts": self._extract_facts(content)
            }
        
        return result
    
    def perform_general_research(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Perform general research task"""
        topic = task.get("description", "")
        
        self.log(f"Conducting research on: {topic}")
        
        # Plan research approach
        research_plan = {
            "topic": topic,
            "approach": [
                "Initial web search for overview",
                "Identify key sources and references",
                "Extract relevant information",
                "Synthesize findings"
            ],
            "required_tasks": []
        }
        
        # Create sub-tasks for research
        research_plan["required_tasks"] = [
            {
                "task_id": f"{task.get('task_id')}_search_1",
                "type": "web_search",
                "query": topic,
                "description": f"Search information about: {topic}"
            }
        ]
        
        return {
            "research_plan": research_plan,
            "success": True
        }
    
    def _generate_summary(self, content: str) -> str:
        """Generate summary from content"""
        # Simple approach: first and last paragraphs
        if not content:
            return ""
        
        paragraphs = content.split("\n\n")
        if len(paragraphs) <= 2:
            return content[:500] + "..."
        
        return paragraphs[0][:300] + "...\n" + paragraphs[-1][:300]
    
    def _extract_key_points(self, content: str) -> list:
        """Extract key points from content"""
        # Look for bullet points or numbered lists
        key_points = []
        
        lines = content.split("\n")
        for line in lines:
            line = line.strip()
            if line.startswith(("-", "•", "*", "1.", "2.", "3.")):
                key_points.append(line)
            elif len(line) > 50 and len(line) < 200:
                # Potential key point sentences
                if any(marker in line for marker in (". ", "! ", "? ")):
                    key_points.append(line)
        
        return key_points[:10]
    
    def _extract_entities(self, content: str) -> list:
        """Extract entities from content"""
        # Simple entity extraction (would be better with NLP)
        entities = {
            "people": [],
            "organizations": [],
            "locations": [],
            "dates": []
        }
        
        # This is a placeholder - real implementation would use NLP
        return entities
    
    def _extract_facts(self, content: str) -> list:
        """Extract facts from content"""
        # Look for factual statements
        facts = []
        
        sentences = content.split(". ")
        for sentence in sentences:
            if any(word in sentence.lower() for word in ("is", "are", "was", "were", "has", "have")):
                if len(sentence) > 20 and len(sentence) < 150:
                    facts.append(sentence.strip() + ".")
        
        return facts[:15]
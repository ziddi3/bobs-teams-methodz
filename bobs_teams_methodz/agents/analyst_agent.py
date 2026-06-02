"""
Analyst Agent
Specializes in data analysis, insights, and reporting
"""

from typing import Dict, Any, List
import json
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ..agent_base import AgentBase


class AnalystAgent(AgentBase):
    """Agent specialized in analytical tasks"""
    
    def __init__(self):
        capabilities = [
            "data_analysis",
            "statistical_analysis",
            "trend_identification",
            "report_generation",
            "insight_extraction",
            "pattern_recognition"
        ]
        super().__init__("Analyst", "Analytics Specialist", capabilities)
    
    def process_task(self, task: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process analytical task"""
        self.update_status("working", task.get("task_id"))
        
        try:
            task_type = task.get("type", "analysis")
            
            if task_type == "data_analysis":
                result = self.analyze_data(task)
            elif task_type == "trend_analysis":
                result = self.analyze_trends(task)
            elif task_type == "report":
                result = self.generate_report(task)
            elif task_type == "insights":
                result = self.extract_insights(task)
            else:
                result = self.analysis_assistance(task)
            
            self.update_status("idle")
            return result
            
        except Exception as e:
            self.log(f"Error processing task: {str(e)}", "error")
            self.update_status("idle")
            return {"error": str(e), "success": False}
    
    def analyze_data(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze data"""
        data_source = task.get("data_source", "")
        analysis_type = task.get("analysis_type", "overview")
        
        self.log(f"Analyzing data from: {data_source}")
        
        analysis_spec = {
            "data_source": data_source,
            "analysis_type": analysis_type,
            "metrics": [],
            "findings": [],
            "visualizations": [],
            "task_id": task.get("task_id")
        }
        
        # If data is provided directly
        if task.get("data"):
            data = task.get("data")
            analysis_result = self._perform_analysis(data, analysis_type)
            analysis_spec.update(analysis_result)
        
        return {
            "analysis": analysis_spec,
            "success": True
        }
    
    def analyze_trends(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze trends in data"""
        data = task.get("data", [])
        time_period = task.get("time_period", "all")
        
        self.log(f"Analyzing trends over period: {time_period}")
        
        trend_analysis = {
            "period": time_period,
            "trends": [],
            "patterns": [],
            "anomalies": [],
            "predictions": []
        }
        
        if data:
            trend_analysis = self._analyze_trends(data, time_period)
        
        return {
            "trend_analysis": trend_analysis,
            "success": True
        }
    
    def generate_report(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Generate analytical report"""
        report_type = task.get("report_type", "summary")
        data = task.get("data", {})
        title = task.get("title", "Analytical Report")
        
        self.log(f"Generating {report_type} report: {title}")
        
        report_structure = {
            "title": title,
            "report_type": report_type,
            "sections": self._get_report_sections(report_type),
            "content": {},
            "summary": "",
            "recommendations": []
        }
        
        # Generate report content
        if data:
            report_content = self._generate_report_content(data, report_type)
            report_structure["content"] = report_content["content"]
            report_structure["summary"] = report_content["summary"]
            report_structure["recommendations"] = report_content["recommendations"]
        
        # Save report if path specified
        file_path = task.get("file_path")
        if file_path:
            report_text = self._format_report_as_text(report_structure)
            self.save_file_content(file_path, report_text)
        
        return {
            "report": report_structure,
            "file_path": file_path,
            "success": True
        }
    
    def extract_insights(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Extract insights from data"""
        data = task.get("data", {})
        focus_areas = task.get("focus_areas", [])
        
        self.log(f"Extracting insights from data")
        
        insights = {
            "key_insights": [],
            "patterns": [],
            "opportunities": [],
            "risks": [],
            "actionable_items": []
        }
        
        if data:
            insights = self._extract_insights_from_data(data, focus_areas)
        
        return {
            "insights": insights,
            "success": True
        }
    
    def analysis_assistance(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """General analysis assistance"""
        description = task.get("description", "")
        
        self.log(f"Providing analysis assistance: {description}")
        
        analysis_plan = {
            "task": description,
            "recommended_approach": [],
            "metrics_to_track": [],
            "tools_needed": []
        }
        
        # Provide recommendations based on task
        if "sales" in description.lower():
            analysis_plan["recommended_approach"].extend([
                "Analyze sales trends over time",
                "Identify top-performing products",
                "Segment customers by behavior",
                "Forecast future sales"
            ])
            analysis_plan["metrics_to_track"] = [
                "Revenue growth",
                "Conversion rate",
                "Average order value",
                "Customer lifetime value"
            ]
        
        elif "performance" in description.lower():
            analysis_plan["recommended_approach"].extend([
                "Measure key performance indicators",
                "Benchmark against targets",
                "Identify bottlenecks",
                "Recommend optimizations"
            ])
            analysis_plan["metrics_to_track"] = [
                "Efficiency",
                "Quality",
                "Speed",
                "Resource utilization"
            ]
        
        return {
            "analysis_plan": analysis_plan,
            "success": True
        }
    
    def _perform_analysis(self, data: Any, analysis_type: str) -> Dict[str, Any]:
        """Perform analysis on data"""
        result = {
            "metrics": [],
            "findings": [],
            "visualizations": []
        }
        
        if isinstance(data, list) and len(data) > 0:
            # Analyze list data
            result["metrics"].append({
                "name": "Count",
                "value": len(data)
            })
            
            if isinstance(data[0], (int, float)):
                result["metrics"].extend([
                    {"name": "Sum", "value": sum(data)},
                    {"name": "Average", "value": sum(data) / len(data)},
                    {"name": "Min", "value": min(data)},
                    {"name": "Max", "value": max(data)}
                ])
                
                result["findings"].append(
                    f"Data range: {min(data)} to {max(data)}"
                )
        
        return result
    
    def _analyze_trends(self, data: List[Any], time_period: str) -> Dict[str, Any]:
        """Analyze trends in data"""
        trend_analysis = {
            "period": time_period,
            "trends": [],
            "patterns": [],
            "anomalies": []
        }
        
        if len(data) >= 3:
            # Simple trend detection
            if isinstance(data[0], (int, float)):
                first_half = data[:len(data)//2]
                second_half = data[len(data)//2:]
                
                avg_first = sum(first_half) / len(first_half)
                avg_second = sum(second_half) / len(second_half)
                
                if avg_second > avg_first * 1.1:
                    trend_analysis["trends"].append("Upward trend detected")
                elif avg_second < avg_first * 0.9:
                    trend_analysis["trends"].append("Downward trend detected")
                else:
                    trend_analysis["trends"].append("Stable trend")
        
        return trend_analysis
    
    def _get_report_sections(self, report_type: str) -> List[str]:
        """Get sections for report type"""
        sections = {
            "summary": ["Executive Summary", "Key Findings", "Conclusions"],
            "detailed": ["Introduction", "Methodology", "Findings", "Analysis", "Conclusions", "Recommendations"],
            "dashboard": ["Overview", "Metrics", "Trends", "Insights", "Actions"]
        }
        
        return sections.get(report_type, sections["summary"])
    
    def _generate_report_content(self, data: Dict[str, Any], report_type: str) -> Dict[str, Any]:
        """Generate report content"""
        return {
            "content": {
                "introduction": "This report presents an analysis of the provided data.",
                "findings": f"Analysis completed on {len(data) if isinstance(data, (list, dict)) else 1} data points."
            },
            "summary": "Data analysis completed successfully.",
            "recommendations": ["Continue monitoring data trends", "Investigate anomalies", "Optimize based on findings"]
        }
    
    def _extract_insights_from_data(self, data: Dict[str, Any], focus_areas: List[str]) -> Dict[str, Any]:
        """Extract insights from data"""
        insights = {
            "key_insights": [],
            "patterns": [],
            "opportunities": [],
            "risks": [],
            "actionable_items": []
        }
        
        # Extract insights based on data structure
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, (int, float)):
                    insights["key_insights"].append(f"{key}: {value}")
        
        insights["actionable_items"].append("Review and act on identified insights")
        
        return insights
    
    def _format_report_as_text(self, report: Dict[str, Any]) -> str:
        """Format report as text"""
        lines = []
        lines.append(f"# {report['title']}")
        lines.append("")
        
        if report.get("summary"):
            lines.append("## Executive Summary")
            lines.append(report["summary"])
            lines.append("")
        
        if report.get("content"):
            lines.append("## Content")
            for section, content in report["content"].items():
                lines.append(f"### {section.capitalize()}")
                lines.append(str(content))
                lines.append("")
        
        if report.get("recommendations"):
            lines.append("## Recommendations")
            for i, rec in enumerate(report["recommendations"], 1):
                lines.append(f"{i}. {rec}")
        
        return "\n".join(lines)
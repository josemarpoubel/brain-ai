"""
Reviewer Agent

Responsible for validating generated code, suggesting improvements
in architecture and logic.
"""

from typing import Dict, Any, List
import logging

from .base_agent import BaseAgent

logger = logging.getLogger(__name__)


class ReviewerAgent(BaseAgent):
    """
    Reviewer Agent for code validation and review.
    
    Responsibilities:
    - Validate generated code
    - Suggest improvements in architecture and logic
    - Check for best practices and potential issues
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("reviewer", config)
        self.checks_enabled = config.get("checks", ["syntax", "style", "security"]) if config else []
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute code review for a given task.
        
        Args:
            task: Task dictionary containing code to review
            
        Returns:
            Dictionary containing review results and suggestions
        """
        logger.info(f"Reviewer executing task: {task.get('description', 'unknown')}")
        
        code = task.get("code", "")
        review_results = self._review_code(code)
        
        return {
            "success": True,
            "agent": self.name,
            "review": review_results,
            "approved": review_results["issues_count"] == 0,
            "suggestions": review_results["suggestions"],
            "metadata": {
                "checks_performed": self.checks_enabled,
                "task_id": task.get("id")
            }
        }
    
    def _review_code(self, code: str) -> Dict[str, Any]:
        """
        Perform comprehensive code review.
        
        Args:
            code: Code string to review
            
        Returns:
            Dictionary containing review results
        """
        issues = []
        suggestions = []
        
        # Syntax check
        if "syntax" in self.checks_enabled:
            syntax_valid = self._check_syntax(code)
            if not syntax_valid:
                issues.append({
                    "type": "syntax",
                    "severity": "critical",
                    "message": "Syntax errors detected"
                })
        
        # Style check
        if "style" in self.checks_enabled:
            style_issues = self._check_style(code)
            issues.extend(style_issues)
        
        # Security check
        if "security" in self.checks_enabled:
            security_issues = self._check_security(code)
            issues.extend(security_issues)
        
        # Generate suggestions
        suggestions = self._generate_suggestions(code, issues)
        
        return {
            "issues": issues,
            "issues_count": len(issues),
            "suggestions": suggestions,
            "quality_score": self._calculate_quality_score(code, issues)
        }
    
    def _check_syntax(self, code: str) -> bool:
        """Check code syntax."""
        try:
            compile(code, '<string>', 'exec')
            return True
        except SyntaxError:
            return False
    
    def _check_style(self, code: str) -> List[Dict[str, Any]]:
        """Check code style (placeholder)."""
        issues = []
        
        # Simple checks
        if len(code.split('\n')) > 100:
            issues.append({
                "type": "style",
                "severity": "low",
                "message": "File is longer than 100 lines, consider refactoring"
            })
        
        return issues
    
    def _check_security(self, code: str) -> List[Dict[str, Any]]:
        """Check for common security issues (placeholder)."""
        issues = []
        
        # Basic security checks
        if "eval(" in code:
            issues.append({
                "type": "security",
                "severity": "high",
                "message": "Use of eval() detected - potential security risk"
            })
        
        if "exec(" in code:
            issues.append({
                "type": "security",
                "severity": "high",
                "message": "Use of exec() detected - potential security risk"
            })
        
        return issues
    
    def _generate_suggestions(self, code: str, issues: List[Dict[str, Any]]) -> List[str]:
        """Generate improvement suggestions."""
        suggestions = []
        
        if not code.strip():
            suggestions.append("Code is empty - implement the required functionality")
        
        if "# TODO" in code:
            suggestions.append("Address TODO comments in the code")
        
        for issue in issues:
            if issue["severity"] == "critical":
                suggestions.append(f"Fix critical issue: {issue['message']}")
        
        return suggestions
    
    def _calculate_quality_score(self, code: str, issues: List[Dict[str, Any]]) -> float:
        """Calculate overall code quality score (0-100)."""
        base_score = 100.0
        
        severity_penalties = {
            "critical": 30,
            "high": 15,
            "medium": 5,
            "low": 2
        }
        
        for issue in issues:
            penalty = severity_penalties.get(issue["severity"], 0)
            base_score -= penalty
        
        return max(0.0, min(100.0, base_score))

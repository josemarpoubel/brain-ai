"""
Tester Agent

Responsible for generating and executing tests,
validating system correctness.
"""

from typing import Dict, Any, List
import logging

from .base_agent import BaseAgent

logger = logging.getLogger(__name__)


class TesterAgent(BaseAgent):
    """
    Tester Agent for test generation and execution.
    
    Responsibilities:
    - Generate and execute tests
    - Validate system correctness
    - Report test results and coverage
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("tester", config)
        self.test_framework = config.get("test_framework", "pytest") if config else "pytest"
        self.coverage_enabled = config.get("coverage_enabled", True) if config else True
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute testing for a given task.
        
        Args:
            task: Task dictionary containing code to test
            
        Returns:
            Dictionary containing test results
        """
        logger.info(f"Tester executing task: {task.get('description', 'unknown')}")
        
        code = task.get("code", "")
        test_type = task.get("test_type", "unit")
        
        # Generate tests
        tests = self._generate_tests(code, test_type)
        
        # Execute tests (placeholder)
        test_results = self._run_tests(tests)
        
        return {
            "success": True,
            "agent": self.name,
            "tests_generated": len(tests),
            "test_results": test_results,
            "passed": test_results["passed"],
            "failed": test_results["failed"],
            "metadata": {
                "test_framework": self.test_framework,
                "test_type": test_type,
                "task_id": task.get("id")
            }
        }
    
    def _generate_tests(self, code: str, test_type: str) -> List[Dict[str, Any]]:
        """
        Generate tests based on code analysis.
        
        Args:
            code: Code string to generate tests for
            test_type: Type of tests to generate (unit, integration, etc.)
            
        Returns:
            List of test case dictionaries
        """
        # Placeholder implementation
        # In production, this would use LLM for intelligent test generation
        tests = []
        
        # Basic function detection
        if "def " in code:
            functions = [line.split("def ")[1].split("(")[0] for line in code.split('\n') if "def " in line]
            
            for func in functions:
                tests.append({
                    "name": f"test_{func}",
                    "type": test_type,
                    "target_function": func,
                    "assertions": ["function exists", "returns expected type"],
                    "status": "generated"
                })
        
        if not tests:
            tests.append({
                "name": "test_placeholder",
                "type": test_type,
                "target_function": "main",
                "assertions": ["basic functionality"],
                "status": "generated"
            })
        
        return tests
    
    def _run_tests(self, tests: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Run generated tests.
        
        Args:
            tests: List of test case dictionaries
            
        Returns:
            Dictionary containing test execution results
        """
        # Placeholder implementation
        # In production, this would actually execute tests in a sandbox
        passed = 0
        failed = 0
        results = []
        
        for test in tests:
            # Simulate test execution
            test_result = {
                "name": test["name"],
                "passed": True,  # Placeholder - all tests pass
                "message": "Test executed successfully (placeholder)",
                "execution_time": 0.001
            }
            
            if test_result["passed"]:
                passed += 1
            else:
                failed += 1
            
            results.append(test_result)
        
        return {
            "total": len(tests),
            "passed": passed,
            "failed": failed,
            "results": results,
            "coverage": self._calculate_coverage() if self.coverage_enabled else None
        }
    
    def _calculate_coverage(self) -> Dict[str, Any]:
        """
        Calculate code coverage (placeholder).
        
        Returns:
            Dictionary containing coverage statistics
        """
        return {
            "statement_coverage": 85.0,
            "branch_coverage": 75.0,
            "function_coverage": 90.0,
            "message": "Coverage calculation is a placeholder"
        }
    
    def generate_test_report(self, test_results: Dict[str, Any]) -> str:
        """
        Generate a human-readable test report.
        
        Args:
            test_results: Test results dictionary
            
        Returns:
            Formatted test report string
        """
        report = []
        report.append("=" * 60)
        report.append("TEST EXECUTION REPORT")
        report.append("=" * 60)
        report.append(f"Total Tests: {test_results.get('total', 0)}")
        report.append(f"Passed: {test_results.get('passed', 0)}")
        report.append(f"Failed: {test_results.get('failed', 0)}")
        report.append("")
        
        for result in test_results.get("results", []):
            status = "✓ PASS" if result.get("passed") else "✗ FAIL"
            report.append(f"{status}: {result.get('name', 'unknown')}")
            if not result.get("passed"):
                report.append(f"       {result.get('message', 'No details')}")
        
        report.append("=" * 60)
        
        return "\n".join(report)

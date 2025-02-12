# core/code_quality.py
import os
import re
import ast
import time
import json
import tempfile
import subprocess
from pathlib import Path
from typing import Dict, List, Any
import bandit
# from git import Repo
from radon.complexity import cc_visit
from radon.metrics import mi_visit
from bandit.core import manager as bandit_manager
from jinja2 import Environment, FileSystemLoader
from core.base_agent import BaseAgent
from utils.logger import AgentLogger

class CodeHelper(BaseAgent):
    def __init__(self, quality_threshold=8.5, config_path=".cqarc", **kwargs):
        super().__init__(**kwargs)
        self.quality_threshold = quality_threshold
        self.config = self._load_config(config_path)
        self.logger = AgentLogger("CodeQuality", log_file="logs/code_quality.log")
        self.temp_dir = Path("./tmp_analysis")
        self.temp_dir.mkdir(exist_ok=True)
        self._initialize_chain(
            prompt_template="""Analyze these code quality results and generate specific improvements:
            {analysis_results}
            Provide both explanations and code examples."""
        )

    def _load_config(self, config_path):
        default_config = {
            'metrics': {
                'complexity_threshold': 10,
                'coverage_threshold': 80,
                'duplication_threshold': 15
            },
            'auto_fix': True,
            'report_formats': ['html', 'json']
        }
        try:
            with open(config_path) as f:
                return json.load(f)
        except:
            return default_config

    def analyze(self, target: str) -> Dict[str, Any]:
        """Multi-mode analysis entry point"""
        start_time = time.time()
        try:
            if Path(target).exists():
                return self._analyze_file(target)
            return self._analyze_code(target)
        except Exception as e:
            return self._handle_error(e, "analysis")
        finally:
            self.logger.info(f"Analysis completed in {time.time() - start_time:.2f}s")

    def _analyze_code(self, code: str) -> Dict[str, Any]:
        """Full analysis pipeline for code strings"""
        with tempfile.NamedTemporaryFile(dir=self.temp_dir, suffix=".py", delete=False) as tmp:
            tmp.write(code.encode())
            tmp_path = tmp.name
        
        results = self._perform_analysis(tmp_path)
        results['auto_fixes'] = self._generate_auto_fixes(results) if self.config['auto_fix'] else []
        # results['report_path'] = self._generate_report(results)
        
        Path(tmp_path).unlink()
        return self._format_response(results)

    def _analyze_file(self, file_path: str) -> Dict[str, Any]:
        """Analysis pipeline for existing files"""
        results = self._perform_analysis(file_path)
        # results['historical'] = self._compare_with_history(file_path)
        results['auto_fixes'] = self._generate_auto_fixes(results) if self.config['auto_fix'] else []
        # results['report_path'] = self._generate_report(results)
        return self._format_response(results)

    def _perform_analysis(self, file_path: str) -> Dict[str, Any]:
        """Core analysis logic"""
        with open(file_path) as f:
            code = f.read()
        
        return {
            'quality_score': self._calculate_quality_score(code),
            'security': self._security_analysis(file_path),
            'complexity': self._complexity_analysis(code),
            'documentation': self._doc_analysis(code),
            'duplication': self._duplication_analysis(file_path),
            'coverage': self._test_coverage_analysis(file_path),
            'architecture': self._arch_analysis(code),
            'historical': None,
            'llm_suggestions': self._generate_ai_suggestions(code)
        }

    def _security_analysis(self, file_path: str) -> Dict[str, Any]:
        """Bandit security analysis"""
        try:
            b_mgr = bandit_manager.BanditManager()
            b_mgr.discover_files([file_path], None)
            b_mgr.run_tests()
            return {
                'score': b_mgr.results.get_score(),
                'issues': [self._format_issue(i) for i in b_mgr.results.get_issues()]
            }
        except Exception as e:
            self.logger.error(f"Security analysis failed: {e}")
            return {'score': 0, 'issues': []}

    def _complexity_analysis(self, code: str) -> Dict[str, Any]:
        """Radon complexity analysis"""
        try:
            cc_results = cc_visit(code)
            return {
                'max_complexity': max([c.complexity for c in cc_results], default=0),
                'average_complexity': sum(c.complexity for c in cc_results)/len(cc_results) if cc_results else 0,
                'threshold': self.config['metrics']['complexity_threshold']
            }
        except Exception as e:
            self.logger.error(f"Complexity analysis failed: {e}")
            return {}

    def _doc_analysis(self, code: str) -> Dict[str, Any]:
        """AST-based documentation analysis"""
        try:
            tree = ast.parse(code)
            functions = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
            documented = sum(1 for f in functions if ast.get_docstring(f))
            return {
                'coverage': (documented/len(functions))*100 if functions else 100,
                'undocumented': [f.name for f in functions if not ast.get_docstring(f)]
            }
        except Exception as e:
            self.logger.error(f"Doc analysis failed: {e}")
            return {}

    def _duplication_analysis(self, file_path: str) -> Dict[str, Any]:
        """Flake8-based duplication check"""
        try:
            result = subprocess.run(
                ['flake8', '--duplicates', '10', file_path],
                capture_output=True, text=True
            )
            duplicates = [line.split(':')[-1].strip() for line in result.stdout.splitlines()]
            return {
                'count': len(duplicates),
                'examples': duplicates[:3],
                'percentage': (len(duplicates)/self._count_lines(file_path))*100
            }
        except Exception as e:
            self.logger.error(f"Duplication check failed: {e}")
            return {}

    def _test_coverage_analysis(self, file_path: str) -> Dict[str, Any]:
        """Coverage.py integration"""
        try:
            cov_result = subprocess.run(
                ['coverage', 'run', '-m', 'pytest', str(file_path)],
                capture_output=True, text=True
            )
            report_result = subprocess.run(
                ['coverage', 'json'],
                capture_output=True, text=True
            )
            with open('coverage.json') as f:
                coverage_data = json.load(f)
            return {
                'coverage': coverage_data['totals']['percent_covered'],
                'missing': coverage_data['files'].get(str(file_path), {}).get('missing_lines', [])
            }
        except Exception as e:
            self.logger.error(f"Test coverage analysis failed: {e}")
            return {'coverage': 0, 'missing': []}

    def _arch_analysis(self, code: str) -> Dict[str, Any]:
        """Architectural quality checks"""
        try:
            tree = ast.parse(code)
            imports = [n for n in ast.walk(tree) if isinstance(n, ast.Import)]
            return {
                'circular_imports': self._detect_circular_imports(imports),
                'layer_violations': self._detect_layer_violations(code)
            }
        except Exception as e:
            self.logger.error(f"Arch analysis failed: {e}")
            return {}

    def _generate_auto_fixes(self, results: Dict[str, Any]) -> List[str]:
        """LLM-powered code fixes"""
        try:
            response = self.chain.invoke({"analysis_results": json.dumps(results, indent=2)})
            return response.content.split('\n')
        except Exception as e:
            self.logger.error(f"Auto-fix generation failed: {e}")
            return []

    # def _generate_report(self, results: Dict[str, Any]) -> str:
    #     """Jinja2 HTML report generation"""
    #     env = Environment(loader=FileSystemLoader('templates'))
    #     template = env.get_template('code_report.html')
    #     report_path = Path('reports') / f"report_{time.strftime('%Y%m%d%H%M%S')}.html"
    #     report_path.parent.mkdir(exist_ok=True)
        
    #     with open(report_path, 'w') as f:
    #         f.write(template.render(results=results))
        
    #     return str(report_path)

    def _calculate_quality_score(self, code: str) -> float:
        """Calculates a quality score based on complexity and documentation coverage."""
        doc_data = self._doc_analysis(code)
        complexity_data = self._complexity_analysis(code)
        quality = 10.0

        # Deduct points if complexity exceeds the threshold
        if complexity_data.get('max_complexity', 0) > self.config['metrics']['complexity_threshold']:
            quality -= 2.0

        # Deduct points if documentation coverage is low
        if doc_data.get('coverage', 100) < 50:
            quality -= 2.0

        return max(quality, 0)

    def _generate_ai_suggestions(self, code: str) -> List[str]:
        """Generates AI-powered suggestions for improving code quality.
           This placeholder provides simple, heuristic-based recommendations."""
        suggestions = []

        # Check for lack of docstrings in functions
        tree = ast.parse(code)
        functions = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
        undocumented = [f.name for f in functions if not ast.get_docstring(f)]
        if undocumented:
            suggestions.append("Add docstrings to the following functions: " + ", ".join(undocumented))

        # Check if functions use basic arithmetic without error handling
        if 'def calculate' in code:
            suggestions.append("Ensure the 'calculate' function validates its inputs.")
        if 'def multiply' in code:
            suggestions.append("Ensure the 'multiply' function handles edge cases (e.g., zero values).")
        
        # Default suggestion if no specific issues found
        if not suggestions:
            suggestions.append("Review your code for possible improvements in structure and error handling.")
        
        return suggestions

    def _count_lines(self, file_path: str) -> int:
        """Counts the number of lines in the given file."""
        try:
            with open(file_path, "r") as f:
                return sum(1 for _ in f)
        except Exception as e:
            self.logger.error(f"Failed to count lines in {file_path}: {e}")
            return 0

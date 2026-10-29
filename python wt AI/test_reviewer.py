# test_reviewer.py
import unittest
from static_analyzer import analyze_code
from report_generator import write_report
import tempfile
import os
from pathlib import Path


class TestStaticAnalyzer(unittest.TestCase):

    def test_syntax_error(self):
        code = "def bad_syntax(:"
        issues = analyze_code(code)
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0]["category"], "Syntax")
        self.assertEqual(issues[0]["severity"], "Error")

    def test_wildcard_import(self):
        code = "from math import *"
        issues = analyze_code(code)
        wildcard_issues = [i for i in issues if "Wildcard import" in i["message"]]
        self.assertEqual(len(wildcard_issues), 1)
        self.assertEqual(wildcard_issues[0]["severity"], "Warning")

    def test_dangerous_calls(self):
        code = """
def run(x):
    '''Docstring'''
    eval(x)
    exec(x)
    compile(x, '', 'exec')
"""
        issues = analyze_code(code)
        danger_issues = [i for i in issues if i["category"] == "Security"]
        self.assertEqual(len(danger_issues), 3)
        for issue in danger_issues:
            self.assertEqual(issue["severity"], "Critical")

    def test_missing_docstring(self):
        code = """
def public_func():
    return 42

def _private_func():
    return 10
"""
        issues = analyze_code(code)
        doc_issues = [i for i in issues if "missing a docstring" in i["message"]]
        # Only public_func should be flagged
        self.assertEqual(len(doc_issues), 1)
        self.assertIn("public_func", doc_issues[0]["message"])

    def test_docstring_present(self):
        code = """
def public_func():
    '''This function has a valid docstring.'''
    return 42
"""
        issues = analyze_code(code)
        doc_issues = [i for i in issues if "missing a docstring" in i["message"]]
        self.assertEqual(len(doc_issues), 0)


class TestReportGenerator(unittest.TestCase):

    def test_write_report(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            report_path = os.path.join(tmpdir, "test_report.md")
            results = {
                "sample.py": [
                    {
                        "severity": "Critical",
                        "category": "Security",
                        "message": "Dangerous call",
                        "refactor": "safe_call()"
                    }
                ]
            }
            write_report(results, report_path)
            content = Path(report_path).read_text(encoding="utf-8")
            self.assertIn("# Code Review Report", content)
            self.assertIn("## File: sample.py", content)
            self.assertIn("Critical (Security)", content)
            self.assertIn("safe_call()", content)


if __name__ == "__main__":
    unittest.main()


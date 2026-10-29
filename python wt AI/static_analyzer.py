# static_analyzer.py
import ast


def analyze_code(code: str, filename: str = "") -> list[dict]:
    """
    Analyze the given Python code (as a string) and return a list of issues.
    Each issue is a dict with keys: severity, category, message, refactor.
    """
    issues = []
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        # Syntax errors are treated as 'Error' severity
        issues.append({
            "severity": "Error",
            "category": "Syntax",
            "message": f"Syntax error: {e}",
            "refactor": "Fix the syntax error in the code."
        })
        return issues

    # Walk the AST and look for patterns
    for node in ast.walk(tree):
        # Detect wildcard imports (e.g. from module import *)
        if isinstance(node, ast.ImportFrom):
            for alias in node.names:
                if alias.name == "*":
                    module = node.module if node.module else ""
                    issues.append({
                        "severity": "Warning",
                        "category": "Style",
                        "message": f"Wildcard import detected in '{module}': use explicit imports instead",
                        "refactor": (
                            f"# Replace wildcard import:\n"
                            f"# from {module} import *\n"
                            f"# with explicit names, e.g.:\n"
                            f"from {module} import name1, name2"
                        )
                    })

        # Detect eval/exec/compile (security risks)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            func_name = node.func.id
            if func_name in ("eval", "exec", "compile"):
                issues.append({
                    "severity": "Critical",
                    "category": "Security",
                    "message": f"Dangerous use of {func_name}() detected",
                    "refactor": (
                        f"# Avoid using {func_name}; use safe alternatives.\n"
                        f"import ast\n"
                        f"# Example replacement:\n"
                        f"result = ast.literal_eval(user_input)  # instead of {func_name}(user_input)"
                    )
                })

        # Detect missing docstring on public functions
        if isinstance(node, ast.FunctionDef):
            if not node.name.startswith("_"):  # public function
                # Check if the first statement is a string literal (docstring)
                first = node.body[0] if node.body else None
                has_docstring = (
                    isinstance(first, ast.Expr)
                    and isinstance(first.value, ast.Constant)
                    and isinstance(first.value.value, str)
                )
                if not has_docstring:
                    issues.append({
                        "severity": "Info",
                        "category": "Style",
                        "message": f"Function '{node.name}' is missing a docstring",
                        "refactor": (
                            f"def {node.name}(...):\n"
                            f'    """Describe the function purpose."""\n'
                            f"    ..."
                        )
                    })

    return issues


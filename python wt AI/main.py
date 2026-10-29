# main.py
import argparse
import sys
from pathlib import Path
from rich.console import Console
from rich.syntax import Syntax

from static_analyzer import analyze_code  # our static AST checks
from ai_client import review_with_ai     # our LLM-based review
from report_generator import write_report  # report generator


def main():
    """
    Parse CLI arguments, orchestrate AST static checks and AI code reviews,
    output a Markdown report, and print a formatted summary to the console.
    """
    # Parse command-line argument (file or directory path)
    parser = argparse.ArgumentParser(description="Automated Code Reviewer & Security Linter")
    parser.add_argument("target", type=Path, help="Path to a Python file or directory")
    args = parser.parse_args()

    target = args.target
    if not target.exists():
        print(f"Error: Path '{target}' does not exist.", file=sys.stderr)
        sys.exit(1)

    # Collect Python files to analyze
    if target.is_file() and target.suffix == ".py":
        files = [target]
    elif target.is_dir():
        files = list(target.rglob("*.py"))
        if not files:
            print(f"No Python files found in directory '{target}'.", file=sys.stderr)
            sys.exit(1)
    else:
        print(f"Error: '{target}' is not a Python file or directory.", file=sys.stderr)
        sys.exit(1)

    # Run analysis on each file
    all_results = {}
    for file_path in files:
        code_text = ""
        try:
            code_text = file_path.read_text(encoding="utf-8")
        except Exception as e:
            print(f"Error reading file {file_path}: {e}", file=sys.stderr)
            continue

        # Static AST analysis
        static_issues = analyze_code(code_text, filename=str(file_path))
        # If there's a syntax error, skip AI review
        has_syntax_error = any(issue.get("category") == "Syntax" for issue in static_issues)

        # AI-powered review (only if no syntax errors)
        if not has_syntax_error:
            try:
                ai_issues = review_with_ai(code_text)
            except Exception as e:
                print(f"AI review failed for {file_path}: {e}", file=sys.stderr)
                ai_issues = []
        else:
            ai_issues = []

        # Combine and sort issues (Critical > Warning > Info)
        combined = static_issues + ai_issues
        severity_rank = {"Error": 4, "Critical": 3, "Warning": 2, "Info": 1}
        combined.sort(key=lambda issue: severity_rank.get(issue.get("severity"), 0), reverse=True)
        all_results[str(file_path)] = combined

    # Write Markdown report
    report_filename = "code_review_report.md"
    write_report(all_results, report_filename)

    # Print summary to terminal using Rich
    console = Console()
    console.print("[bold underline]Code Review Summary[/bold underline]\n")
    for fname, issues in all_results.items():
        console.print(f"[cyan]{fname}[/cyan]")
        if not issues:
            console.print("  [green]No issues found.[/green]\n")
            continue
        for issue in issues:
            sev = issue.get("severity", "Info")
            cat = issue.get("category", "")
            msg = issue.get("message", "")
            color = {"Error": "red", "Critical": "red", "Warning": "yellow"}.get(sev, "green")
            console.print(f"  [{color}]{sev}[/] ({cat}) - {msg}")
            snippet = issue.get("refactor", "").strip()
            if snippet:
                console.print("    Suggested refactor:", style="italic")
                # Use Rich syntax highlighting for the code snippet
                syntax = Syntax(snippet, "python", theme="monokai", line_numbers=False)
                console.print(syntax)
        console.print()


if __name__ == "__main__":
    main()


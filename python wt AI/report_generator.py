# report_generator.py
from datetime import datetime, timezone


def write_report(results: dict[str, list[dict]], output_path: str):
    """
    Write a Markdown report of the results.
    `results` is a mapping from filename to list of issue dicts.
    """
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# Code Review Report\n\n")
        try:
            timestamp = datetime.now(timezone.utc).isoformat()
        except Exception:
            timestamp = datetime.utcnow().isoformat()
        f.write(f"_Generated on {timestamp} UTC_\n\n")
        for filename, issues in results.items():
            f.write(f"## File: {filename}\n\n")
            if not issues:
                f.write("No issues found. :tada:\n\n")
                continue
            for issue in issues:
                severity = issue.get("severity", "")
                category = issue.get("category", "")
                message = issue.get("message", "")
                refactor = issue.get("refactor", "").rstrip()
                f.write(f"- **{severity} ({category})**: {message}\n\n")
                if refactor:
                    f.write("  Suggested refactor:\n\n")
                    f.write("  ```python\n")
                    # Indent snippet lines for Markdown readability
                    for line in refactor.splitlines():
                        f.write(f"  {line}\n")
                    f.write("  ```\n\n")


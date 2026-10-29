# ai_client.py
import os
import json
import openai

# Set legacy api key if attribute exists
openai.api_key = os.getenv("OPENAI_API_KEY")


def review_with_ai(code: str) -> list[dict]:
    """
    Send the code to the LLM and parse the JSON-formatted review results.
    Returns a list of issue dicts similar to static analysis.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("[Warning] OPENAI_API_KEY environment variable is not set. Skipping AI review.")
        return []

    system_prompt = (
        "You are a Python code review assistant. "
        "Identify security vulnerabilities, performance issues, and style problems in the code. "
        "Answer in JSON format with each issue as an object containing "
        "'severity', 'category', 'message', and 'refactor'."
    )
    user_prompt = (
        "Review the following Python code:\n"
        "```python\n"
        f"{code}\n"
        "```\n"
        "List any issues found as a JSON array of objects. "
        "Each object must have:\n"
        "- severity (Critical/Warning/Info)\n"
        "- category (Security/Performance/Style)\n"
        "- message: a description of the issue\n"
        "- refactor: a suggested code fix snippet\n"
    )

    text = ""
    # Support both modern OpenAI SDK (v1.0+) and legacy SDK (<1.0)
    if hasattr(openai, "OpenAI"):
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0
        )
        text = response.choices[0].message.content or ""
    else:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0
        )
        text = response.choices[0].message.content or ""

    # Clean markdown fences if the model wraps the output in ```json ... ```
    cleaned_text = text.strip()
    if cleaned_text.startswith("```"):
        lines = cleaned_text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        cleaned_text = "\n".join(lines).strip()

    # Attempt to parse JSON output
    try:
        issues = json.loads(cleaned_text)
        if isinstance(issues, list):
            return issues
        if isinstance(issues, dict) and "issues" in issues and isinstance(issues["issues"], list):
            return issues["issues"]
        return []
    except json.JSONDecodeError:
        # If parsing fails, return no issues (could log for debugging)
        return []


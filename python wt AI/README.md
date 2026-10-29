# Automated Code Reviewer & Security Linter (MVP)

A modular command-line Python tool that statically analyzes Python source code using AST (Abstract Syntax Tree) checks and invokes an LLM (OpenAI GPT-4) for deeper code quality, security, and performance reviews.

## Architecture & Project Structure

- **`main.py`**: CLI entry point. Parses command-line arguments via `argparse`, discovers `.py` files using `pathlib.Path`, coordinates the static analysis and AI reviews, generates the Markdown report, and prints a formatted terminal summary via `Rich`.
- **`static_analyzer.py`**: AST-based static linter. Detects wildcard imports (`from module import *`), dangerous function calls (`eval`, `exec`, `compile`), syntax errors, and missing docstrings on public functions.
- **`ai_client.py`**: AI reviewer communicating with OpenAI Chat Completions. Instructs the model to inspect code and return structured JSON reviews (supporting both modern OpenAI SDK `1.x+` and legacy `0.28`).
- **`report_generator.py`**: Report writer producing a structured Markdown file (`code_review_report.md`) containing timestamps, categorized issues, and syntax-highlighted refactoring snippets.
- **`requirements.txt`**: Project dependencies (`openai`, `rich`).
- **`example_test.py`**: Sample file with intentional anti-patterns for testing.

---

## Prerequisites & Installation

1. **Python 3.10+** installed on your system.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set your OpenAI API key in your environment:
   - **Linux / macOS**:
     ```bash
     export OPENAI_API_KEY="sk-..."
     ```
   - **Windows (PowerShell)**:
     ```powershell
     $env:OPENAI_API_KEY="sk-..."
     ```
   - **Windows (CMD)**:
     ```cmd
     set OPENAI_API_KEY=sk-...
     ```

*(Note: If `OPENAI_API_KEY` is not provided, the static analyzer will still function and report static AST issues, skipping the AI pass.)*

---

## Usage

### Option 1: Native Python (Recommended)
- **Analyze a single file:**
  ```bash
  python main.py example_test.py
  ```
- **Analyze an entire directory:**
  ```bash
  python main.py .
  ```
- **Run the unit tests:**
  ```bash
  python -m unittest test_reviewer.py
  ```

### Option 2: NPM Scripts
You can also run the project using npm:
- **Run on example file:**
  ```bash
  npm start
  ```
- **Scan entire project:**
  ```bash
  npm run scan
  ```
- **Run unit test suite:**
  ```bash
  npm test
  ```

---

## Output

1. **Console Output**: A colorful terminal summary powered by `rich`, color-coded by severity:
   - `Error` / `Critical` (Red)
   - `Warning` (Yellow)
   - `Info` (Green)
   - Syntax-highlighted refactoring suggestions for each finding.
2. **Markdown Report**: Automatically saved to `code_review_report.md`.


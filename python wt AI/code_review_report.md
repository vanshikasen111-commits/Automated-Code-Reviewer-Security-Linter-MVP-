# Code Review Report

_Generated on 2026-10-29T14:13:36.851299+00:00 UTC_

## File: example_test.py

- **Critical (Security)**: Dangerous use of eval() detected

  Suggested refactor:

  ```python
  # Avoid using eval; use safe alternatives.
  import ast
  # Example replacement:
  result = ast.literal_eval(user_input)  # instead of eval(user_input)
  ```

- **Warning (Style)**: Wildcard import detected in 'math': use explicit imports instead

  Suggested refactor:

  ```python
  # Replace wildcard import:
  # from math import *
  # with explicit names, e.g.:
  from math import name1, name2
  ```

- **Info (Style)**: Function 'calculate_area' is missing a docstring

  Suggested refactor:

  ```python
  def calculate_area(...):
      """Describe the function purpose."""
      ...
  ```

- **Info (Style)**: Function 'unsafe_calculator' is missing a docstring

  Suggested refactor:

  ```python
  def unsafe_calculator(...):
      """Describe the function purpose."""
      ...
  ```


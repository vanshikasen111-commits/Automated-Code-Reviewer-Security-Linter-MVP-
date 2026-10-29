@echo off
setlocal enabledelayedexpansion
title "Automated Code Reviewer & Security Linter"

:: 1. Locate Python executable automatically
set "PY_EXE=%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
if not exist "!PY_EXE!" (
    set "PY_EXE=python"
)

:: If user supplied a command line argument directly (e.g. run.bat filename.py)
if not "%~1"=="" (
    "!PY_EXE!" main.py %*
    goto :done
)

cls
echo ================================================================
echo    AUTOMATED CODE REVIEWER ^& SECURITY LINTER (MVP)
echo ================================================================
echo.
echo   [1] Run Quick Demo on example_test.py (Default - press Enter)
echo   [2] Scan Entire Current Directory (.)
echo   [3] Enter a custom file or folder path
echo   [4] Run Unit Tests (test_reviewer.py)
echo   [5] Exit
echo.
echo ================================================================
set "choice=1"
set /p choice="Select an option [1-5] (default 1): "

if "%choice%"=="1" (
    echo.
    echo Running review on example_test.py...
    echo.
    "!PY_EXE!" main.py example_test.py
    goto :done
)
if "%choice%"=="2" (
    echo.
    echo Scanning all Python files in the current folder...
    echo.
    "!PY_EXE!" main.py .
    goto :done
)
if "%choice%"=="3" (
    echo.
    set /p target_path="Enter path to file or directory: "
    echo.
    "!PY_EXE!" main.py "!target_path!"
    goto :done
)
if "%choice%"=="4" (
    echo.
    echo Running unit tests...
    echo.
    "!PY_EXE!" -m unittest test_reviewer.py
    goto :done
)
if "%choice%"=="5" (
    exit /b 0
)

echo.
echo Running default review on example_test.py...
"!PY_EXE!" main.py example_test.py

:done
echo.
echo ================================================================
echo Done! Markdown report updated: code_review_report.md
echo ================================================================
echo.
pause

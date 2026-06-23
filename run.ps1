<#
.SYNOPSIS
    Task runner script for Portfolio OS.
.DESCRIPTION
    Simplifies environment installation, formatting, linting, testing, and running the application.
.PARAMETER Action
    The action to execute: 'install', 'format', 'lint', 'test', 'run'.
.PARAMETER ArgsList
    Optional arguments list passed directly to the CLI command when Action is 'run'.
.EXAMPLE
    .\run.ps1 -Action test
    .\run.ps1 -Action run -ArgsList "init my_portfolio"
#>
param (
    [Parameter(Mandatory=$true, Position=0)]
    [ValidateSet("install", "format", "lint", "test", "run")]
    [string]$Action,

    [Parameter(Position=1)]
    [string]$ArgsList = ""
)

$venv_python = ".\.venv\Scripts\python.exe"
$venv_pip = ".\.venv\Scripts\pip.exe"
$venv_pytest = ".\.venv\Scripts\pytest.exe"
$venv_black = ".\.venv\Scripts\black.exe"
$venv_ruff = ".\.venv\Scripts\ruff.exe"
$venv_mypy = ".\.venv\Scripts\mypy.exe"
$venv_pre_commit = ".\.venv\Scripts\pre-commit.exe"

# Helper check for virtual environment
if (-not (Test-Path $venv_python)) {
    Write-Warning "Virtual environment (.venv) not found. Please ensure it is initialized at .\.venv"
    # Fallback to system path command names if virtualenv isn't there
    $venv_python = "python"
    $venv_pip = "pip"
    $venv_pytest = "pytest"
    $venv_black = "black"
    $venv_ruff = "ruff"
    $venv_mypy = "mypy"
    $venv_pre_commit = "pre-commit"
}

switch ($Action) {
    "install" {
        Write-Host "Installing project and developer dependencies..." -ForegroundColor Cyan
        & $venv_python -m pip install -r requirements-dev.txt
        Write-Host "Installing pre-commit hooks..." -ForegroundColor Cyan
        & $venv_pre_commit install
        Write-Host "Setup completed successfully!" -ForegroundColor Green
    }
    "format" {
        Write-Host "Running Black code formatter..." -ForegroundColor Cyan
        & $venv_black .
        Write-Host "Running Ruff linter with autofixes..." -ForegroundColor Cyan
        & $venv_ruff check --fix .
        Write-Host "Formatting completed!" -ForegroundColor Green
    }
    "lint" {
        Write-Host "Running Ruff linter checks..." -ForegroundColor Cyan
        & $venv_ruff check .
        Write-Host "Running MyPy strict type checker..." -ForegroundColor Cyan
        & $venv_mypy src tests
        Write-Host "Linting completed!" -ForegroundColor Green
    }
    "test" {
        Write-Host "Running pytest with coverage..." -ForegroundColor Cyan
        & $venv_python -X utf8 -m pytest
    }
    "run" {
        if ($ArgsList) {
            $parsedArgs = $ArgsList -split " "
            & $venv_python -X utf8 -m src.main $parsedArgs
        } else {
            & $venv_python -X utf8 -m src.main
        }
    }
}

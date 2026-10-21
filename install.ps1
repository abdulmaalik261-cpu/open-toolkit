# One-line installer for open-toolkit on Windows PowerShell.
# Usage: irm https://raw.githubusercontent.com/abdulmaalik261-cpu/open-toolkit/main/install.ps1 | iex

$ErrorActionPreference = "Stop"

if (-not (Get-Command py -ErrorAction SilentlyContinue)) {
    Write-Error "Python not found. Install it from https://www.python.org/downloads/ (check 'Add to PATH') and re-run."
    exit 1
}

Write-Host "Installing open-toolkit..."
py -m pip install --user --upgrade open-toolkit

Write-Host ""
Write-Host "Done. Try: toolkit --help"
Write-Host "If 'toolkit' is not recognized, restart your terminal or use: py -m open_toolkit.cli"

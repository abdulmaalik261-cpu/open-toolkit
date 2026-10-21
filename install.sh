#!/usr/bin/env bash
# One-line installer for open-toolkit on Linux, macOS, or Android (Termux).
# Usage: curl -fsSL https://raw.githubusercontent.com/YOUR_USERNAME/open-toolkit/main/install.sh | bash
set -euo pipefail

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 not found." >&2
  if command -v pkg >/dev/null 2>&1; then
    echo "Detected Termux — installing python..." >&2
    pkg install -y python
  else
    echo "Please install Python 3.9+ first, then re-run this script." >&2
    exit 1
  fi
fi

echo "Installing open-toolkit..."
python3 -m pip install --user --upgrade open-toolkit

echo
echo "Done. Try: toolkit --help"
echo "If 'toolkit' is not found, add your Python user bin dir to PATH"
echo "(e.g. ~/.local/bin on Linux/macOS, or run 'python3 -m open_toolkit.cli')."

# open-toolkit

[![CI](https://github.com/abdulmaalik261-cpu/open-toolkit/actions/workflows/ci.yml/badge.svg)](https://github.com/abdulmaalik261-cpu/open-toolkit/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue)](pyproject.toml)

A single, open-source command-line toolkit that bundles four small, genuinely
useful utilities into one install. No accounts, no cloud, no tracking — it
runs entirely on your own machine (or phone).

**[Docs site →](https://abdulmaalik261-cpu.github.io/open-toolkit/)**

```bash
pip install open-toolkit
toolkit --help
```

| Command | What it does |
|---|---|
| `toolkit diagram` | Walk a Python codebase and generate a Mermaid dependency diagram of how its modules import each other. Also ships as a Claude Skill (`skill/diagram/`) so an AI agent can call it directly. |
| `toolkit sign` | A tiny self-hosted e-signature tool: stamp a text or image signature onto a PDF at exact coordinates. No subscription, no third-party server. |
| `toolkit fizzbuzz` | A deliberately, hilariously over-engineered FizzBuzz — abstract factories, a strategy registry, dependency injection, the works — for a laugh and as a joke showcase of enterprise-pattern excess. |
| `toolkit doc2md` | Convert a PDF, DOCX, HTML file, or a live URL into clean Markdown in one command. |

## Why one toolkit instead of four repos?

Because most people don't want to manage four separate installs for
small, everyday jobs. `pip install open-toolkit` gets you all four, and
each subcommand is independent — use one, use all four, it doesn't matter.

## Install

### Linux / macOS

```bash
python3 -m pip install --user open-toolkit
```

### Windows (PC)

```powershell
py -m pip install --user open-toolkit
```

### Android (via Termux)

1. Install [Termux](https://f-droid.org/packages/com.termux/) from F-Droid.
2. In Termux:
   ```bash
   pkg update && pkg install python
   pip install open-toolkit
   ```
3. Run `toolkit --help` from the Termux shell.

### From source (any platform)

```bash
git clone https://github.com/abdulmaalik261-cpu/open-toolkit.git
cd open-toolkit
python3 -m pip install --user -e .
```

See `install.sh` (Linux/macOS/Termux) or `install.ps1` (Windows) for
one-line setup scripts.

## Usage

### diagram

```bash
toolkit diagram ./my_project -o architecture.md
```

Produces a Mermaid `graph TD` block you can paste into any Markdown
viewer that renders Mermaid (GitHub, Obsidian, Notion, Claude artifacts).

### sign

```bash
# Check page size first so you know where to place the signature
toolkit sign info contract.pdf

# Stamp a typed signature on page 1 at (x=400, y=80) points from bottom-left
toolkit sign apply contract.pdf --page 1 --x 400 --y 80 --text "Jane Doe"

# Or stamp an image of your actual signature
toolkit sign apply contract.pdf --page 1 --x 400 --y 80 --image signature.png
```

### fizzbuzz

```bash
toolkit fizzbuzz 1 30
```

### doc2md

```bash
toolkit doc2md report.pdf -o report.md
toolkit doc2md https://example.com/article -o article.md
```

## Development

```bash
git clone https://github.com/abdulmaalik261-cpu/open-toolkit.git
cd open-toolkit
python3 -m pip install -e ".[dev]"
pytest
```

## Contributing

PRs welcome — see [CONTRIBUTING.md](CONTRIBUTING.md). Each subcommand
lives in its own file under `open_toolkit/commands/`, so adding a fifth
tool is just: write a module with a `run(args)` and `add_subparser(subparsers)`,
then register it in `open_toolkit/cli.py`.

## License

MIT — see [LICENSE](LICENSE).

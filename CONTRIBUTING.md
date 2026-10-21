# Contributing

Thanks for considering a contribution!

## Adding a new subcommand

1. Create `open_toolkit/commands/your_tool.py` with:
   - a `run(args) -> int` function that does the work
   - an `add_subparser(subparsers)` function that registers the CLI arguments
2. Register it in `open_toolkit/cli.py`:
   ```python
   from open_toolkit.commands import your_tool
   ...
   your_tool.add_subparser(subparsers)
   ```
3. Add tests under `tests/test_your_tool.py`.
4. Add a row to the table in `README.md`.

## Running tests

```bash
python3 -m pip install -e ".[dev]"
pytest
```

## Code style

- Keep each subcommand self-contained and dependency-light.
- Prefer the standard library where reasonable.
- Exit codes: `0` on success, non-zero on error, with a message on stderr.

## Reporting bugs / requesting features

Open a GitHub issue with steps to reproduce (for bugs) or the use case
(for features) — issue templates are provided for both.

## Code of conduct

Be civil. See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

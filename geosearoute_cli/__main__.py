"""Module entry point for geosearoute-cli."""

import sys

from .cli import main as cli_main


def main_wrapper():
    """Run the CLI and exit with the returned status code."""
    try:
        raise SystemExit(cli_main())
    except KeyboardInterrupt:
        print("Operation cancelled.", file=sys.stderr)
        raise SystemExit(1)
    except SystemExit:
        raise
    except Exception as exc:  # pragma: no cover - defensive wrapper
        print(f"Fatal error: {exc}", file=sys.stderr)
        raise SystemExit(2)


def main_entry():
    """Compatibility wrapper for console script entry points."""
    main_wrapper()


main = main_entry


if __name__ == "__main__":
    main_wrapper()

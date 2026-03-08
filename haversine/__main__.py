"""
Entry point for haversine CLI calculator.

This module provides the main entry point for both `python -m haversine` and 
`uv run haversine` execution patterns. It demonstrates proper Python package
structure while maintaining the zero-dependency approach.

The entry point delegates to the CLI module to maintain separation of concerns
and enable easier testing of CLI functionality.

Usage:
    python -m haversine <lat1> <lon1> <lat2> <lon2>
    uv run haversine <lat1> <lon1> <lat2> <lon2>

Exit Codes:
    0: Successful calculation and output
    1: User error (invalid input, wrong arguments)
    2: System error (unexpected failures)

Author: Germaneering Lab
License: Apache V2
"""

import sys
from .cli import main


def main_wrapper():
    """
    Wrapper function for package execution entry point.
    
    This function is called when the package is executed as a module
    (python -m haversine) or via uv run. It provides a clean entry point
    that properly exits with the appropriate code.
    
    This wrapper exists to ensure proper exit code handling when the 
    package is run in different contexts.
    """
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        # Handle Ctrl+C at the top level
        print("\nOperation cancelled.", file=sys.stderr)  
        sys.exit(1)
    except Exception as e:
        # Top-level error handler for catastrophic failures
        print(f"Fatal error: {e}", file=sys.stderr)
        print("Please report this issue to the Germaneering Lab.", file=sys.stderr)
        sys.exit(2)


if __name__ == '__main__':
    # This block executes when the module is run directly:
    # python -m haversine <args>
    # python haversine/__main__.py <args>
    
    main_wrapper()
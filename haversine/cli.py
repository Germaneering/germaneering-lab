"""
Command-line interface for haversine distance calculator.

This module implements the CLI functionality for the haversine calculator,
providing basic argument parsing and output formatting for User Story 1.
The interface demonstrates clear CLI patterns while maintaining the Deep Code
principle through educational error messages and usage information.

Author: Germaneering Lab
License: Apache V2
"""

import sys
import argparse
from typing import List, Optional, Union
from .models import GeographicPoint
from .calculator import DistanceCalculation
from .validator import CoordinateValidator, CoordinateValidationError


def create_argument_parser() -> argparse.ArgumentParser:
    """
    Create and configure the command-line argument parser.
    
    Sets up the basic argument structure for User Story 1: accepting four
    coordinate arguments and providing help information that demonstrates
    the educational purpose of the tool.
    
    Returns:
        Configured ArgumentParser object
    """
    parser = argparse.ArgumentParser(
        prog='haversine',
        description=(
            'Calculate great-circle distance between two points using the haversine formula.\n'
            'This tool demonstrates the Germaneering "Deep Code" principle by implementing\n'
            'geographic calculations from mathematical primitives.'
        ),
        epilog=(
            'Examples:\n'
            '  haversine 40.7128 -74.0060 34.0522 -118.2437  # NYC to LA\n'
            '  haversine 51.5074 -0.1278 48.8566 2.3522      # London to Paris\n'
            '  haversine 0 0 0 0                              # Same point (returns 0)'
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Positional arguments for coordinates (User Story 1 requirement)
    parser.add_argument(
        'lat1',
        type=float,
        help='Origin latitude in decimal degrees [-90, 90]'
    )
    parser.add_argument(
        'lon1', 
        type=float,
        help='Origin longitude in decimal degrees [-180, 180]'
    )
    parser.add_argument(
        'lat2',
        type=float, 
        help='Destination latitude in decimal degrees [-90, 90]'
    )
    parser.add_argument(
        'lon2',
        type=float,
        help='Destination longitude in decimal degrees [-180, 180]'
    )
    
    # Version information
    parser.add_argument(
        '--version',
        action='version',
        version='haversine-cli 1.0.0 (Germaneering Lab)'
    )
    
    # User Story 3: Output formatting options
    parser.add_argument(
        '--unit',
        choices=['km', 'miles', 'nautical'],
        default='km',
        help='Distance unit for output (default: km)'
    )
    
    parser.add_argument(
        '--precision', 
        type=int,
        choices=range(0, 7),  # 0 to 6 decimal places
        default=2,
        metavar='0-6',
        help='Number of decimal places in output (default: 2)'
    )
    
    return parser


def parse_coordinates(args: argparse.Namespace) -> tuple[GeographicPoint, GeographicPoint]:
    """
    Parse command-line coordinates into validated GeographicPoint objects.
    
    This function converts the raw coordinate arguments into GeographicPoint
    instances with enhanced validation using the CoordinateValidator. Provides
    clear, educational error messages that help users understand geographic
    coordinate constraints.
    
    Args:
        args: Parsed command-line arguments containing lat1, lon1, lat2, lon2
        
    Returns:
        Tuple of (origin, destination) GeographicPoint objects
        
    Raises:
        CoordinateValidationError: If coordinates are outside valid ranges
        ValueError: If coordinates have other validation issues
    """
    try:
        # Extract coordinate values
        lat1, lon1, lat2, lon2 = args.lat1, args.lon1, args.lat2, args.lon2
        
        # Validate coordinate ranges using explicit validator
        # This provides better error messages than GeographicPoint validation
        CoordinateValidator.validate_coordinate_pair(lat1, lon1)
        CoordinateValidator.validate_coordinate_pair(lat2, lon2)
        
        # Create validated GeographicPoint objects
        origin = GeographicPoint(lat1, lon1)
        destination = GeographicPoint(lat2, lon2) 
        return origin, destination
        
    except CoordinateValidationError as e:
        # Provide educational error message with examples
        examples = CoordinateValidator.get_coordinate_examples()
        nyc = examples["cities"]["NYC"]
        london = examples["cities"]["London"]
        
        error_msg = (
            f"{str(e)}\n\n"
            f"Geographic coordinate constraints:\n"
            f"  • Latitude: [-90, 90] degrees (North/South poles)\n"
            f"  • Longitude: [-180, 180] degrees (International Date Line)\n\n"
            f"Examples of valid coordinates:\n"
            f"  • NYC: {nyc['lat']} {nyc['lon']}\n"
            f"  • London: {london['lat']} {london['lon']}\n"
            f"  • Equator/Prime Meridian: 0 0"
        )
        raise ValueError(error_msg) from e
        
    except (ValueError, TypeError) as e:
        # Handle other coordinate parsing errors
        raise ValueError(f"Invalid coordinate format: {e}") from e


def format_basic_output(distance_calc: DistanceCalculation) -> str:
    """
    Format distance calculation result for basic output (User Story 1).
    
    Provides simple "number km" format as required for the basic distance
    calculation user story. Uses 2 decimal places for reasonable precision
    without overwhelming detail.
    
    Args:
        distance_calc: DistanceCalculation object with computed distance
        
    Returns:
        Formatted distance string
        
    Example:
        "3936.75 km"
    """
    return f"{distance_calc.distance_km:.2f} km"


def format_enhanced_output(distance_calc: DistanceCalculation, unit: str = 'km', precision: int = 2) -> str:
    """
    Format distance calculation result with custom unit and precision (User Story 3).
    
    Provides flexible output formatting with support for multiple units and
    configurable decimal precision. Demonstrates the educational aspects by
    showing distance calculations in various standard measurement systems.
    
    Args:
        distance_calc: DistanceCalculation object with computed distance
        unit: Output unit ('km', 'miles', 'nautical')
        precision: Number of decimal places (0-6)
        
    Returns:
        Formatted distance string with specified unit and precision
        
    Examples:
        format_enhanced_output(calc, 'km', 2) -> "3936.75 km"
        format_enhanced_output(calc, 'miles', 1) -> "2446.4 miles"
        format_enhanced_output(calc, 'nautical', 3) -> "2125.567 nautical miles"
    """
    # Get distance in the requested unit
    if unit == 'km':
        distance_value = distance_calc.distance_km
        unit_label = 'km'
    elif unit == 'miles':
        distance_value = distance_calc.distance_miles
        unit_label = 'miles'
    elif unit == 'nautical':
        distance_value = distance_calc.distance_nautical  
        unit_label = 'nautical miles'
    else:
        # Fallback - should not happen with argument parser validation
        distance_value = distance_calc.distance_km
        unit_label = 'km'
    
    # Format with specified precision
    format_spec = f"{{:.{precision}f}}"
    formatted_distance = format_spec.format(distance_value)
    
    return f"{formatted_distance} {unit_label}"


def print_usage_examples() -> None:
    """
    Print comprehensive usage examples and educational information.
    
    This function provides detailed examples demonstrating proper coordinate
    format and showcasing the educational value of the tool through real-world
    geographic calculations.
    """
    examples = CoordinateValidator.get_coordinate_examples()
    
    print("\nUSAGE EXAMPLES:", file=sys.stderr)
    print("  Calculate distance between major cities:", file=sys.stderr)
    
    nyc = examples["cities"]["NYC"] 
    london = examples["cities"]["London"]
    tokyo = examples["cities"]["Tokyo"]
    
    print(f"    haversine {nyc['lat']} {nyc['lon']} {london['lat']} {london['lon']}  # NYC to London", file=sys.stderr)
    print(f"    haversine {london['lat']} {london['lon']} {tokyo['lat']} {tokyo['lon']}  # London to Tokyo", file=sys.stderr)
    print("", file=sys.stderr)
    
    print("  Test with edge cases:", file=sys.stderr)
    north_pole = examples["extremes"]["North Pole"]
    south_pole = examples["extremes"]["South Pole"] 
    print(f"    haversine {north_pole['lat']} {north_pole['lon']} {south_pole['lat']} {south_pole['lon']}  # Pole to pole", file=sys.stderr)
    print("    haversine 0 0 0 0                                    # Same point (zero distance)", file=sys.stderr)
    print("", file=sys.stderr)
    
    print("COORDINATE FORMAT:", file=sys.stderr) 
    print("  • Latitude: [-90, 90] degrees (North/South poles)", file=sys.stderr)
    print("  • Longitude: [-180, 180] degrees (International Date Line)", file=sys.stderr)
    print("  • Use decimal degrees format (e.g., 40.7128 -74.0060)", file=sys.stderr)
    print("", file=sys.stderr)


def handle_user_error(error_message: str, show_examples: bool = True) -> int:
    """
    Handle user input errors with structured error reporting.
    
    Provides consistent error formatting with optional usage examples to help
    users understand proper input format and geographic coordinate constraints.
    
    Args:
        error_message: Primary error description
        show_examples: Whether to display usage examples
        
    Returns:
        Exit code 1 (user error)
    """
    print(f"ERROR: {error_message}", file=sys.stderr)
    print("", file=sys.stderr)
    
    if show_examples:
        print_usage_examples()
    
    print("For complete help: haversine --help", file=sys.stderr)
    return 1


def run_basic_calculation(args: List[str] = None) -> int:
    """
    Run the haversine distance calculation CLI interface (User Stories 1, 2, & 3).
    
    This function implements:
    - User Story 1: Basic distance calculation with coordinate arguments
    - User Story 2: Enhanced input validation and structured error handling
    - User Story 3: Output formatting options with --unit and --precision flags
    
    Provides proper exit codes and educational error messages following CLI standards.
    
    Args:
        args: Command-line arguments (defaults to sys.argv[1:])
        
    Returns:
        Exit code: 0 for success, 1 for user errors, 2 for system errors
        
    Side Effects:
        Prints distance result to stdout or error message to stderr
    """
    if args is None:
        args = sys.argv[1:]
    
    parser = create_argument_parser()
    
    try:
        # Parse command-line arguments
        parsed_args = parser.parse_args(args)
        
        # Convert arguments to validated GeographicPoint objects
        origin, destination = parse_coordinates(parsed_args)
        
        # Perform distance calculation
        distance_calc = DistanceCalculation(origin, destination)
        
        # Output result with appropriate formatting 
        # Use enhanced formatting if unit or precision options were specified
        if hasattr(parsed_args, 'unit') and (parsed_args.unit != 'km' or parsed_args.precision != 2):
            # User Story 3: Enhanced output formatting
            result = format_enhanced_output(distance_calc, parsed_args.unit, parsed_args.precision)
        else:
            # User Story 1: Basic output format for backward compatibility
            result = format_basic_output(distance_calc)
        
        print(result)
        
        return 0  # Success
        
    except SystemExit as e:
        # Handle argparse errors (insufficient args, non-numeric values, etc.)
        # argparse calls sys.exit() directly for argument errors
        if e.code == 0:
            # Help or version was requested - this is normal  
            return 0
        else:
            # Argument parsing error - return as user error
            return e.code if e.code is not None else 1
        
    except ValueError as e:
        # User input errors (coordinates out of range, invalid format, etc.)
        # Use structured error handling for better user experience
        return handle_user_error(str(e), show_examples=True)
        
    except TypeError as e:
        # Type conversion errors (shouldn't happen with argparse, but defensive)
        return handle_user_error(f"Invalid argument type: {e}", show_examples=True)
        
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("\nCalculation cancelled by user.", file=sys.stderr)
        return 1  # User interruption
        
    except Exception as e:
        # Unexpected system errors
        print(f"INTERNAL ERROR: {e}", file=sys.stderr)
        print("This indicates a bug in the haversine calculator.", file=sys.stderr)
        print("Please report this issue to the Germaneering Lab.", file=sys.stderr)
        return 2  # System error


def main() -> int:
    """
    Main entry point for the haversine CLI application.
    
    This function serves as the primary entry point called from __main__.py
    and provides a clean interface for testing and external usage.
    
    Returns:
        Exit code appropriate for the operation result
    """
    return run_basic_calculation()
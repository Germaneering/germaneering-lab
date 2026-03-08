"""
Integration tests for CLI interface functionality.

These tests validate the command-line interface behavior for User Story 1
(Basic Distance Calculation), ensuring proper argument parsing, output formatting,
and error handling. Tests serve as both validation and documentation of expected
CLI behavior.

Author: Germaneering Lab
License: Apache V2
"""

import unittest
import sys
import io
from contextlib import redirect_stdout, redirect_stderr
from haversine.cli import (
    create_argument_parser, 
    parse_coordinates, 
    format_basic_output,
    format_enhanced_output,
    run_basic_calculation
)
from haversine.models import GeographicPoint
from haversine.calculator import DistanceCalculation


class TestArgumentParser(unittest.TestCase):
    """Test cases for command-line argument parsing."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.parser = create_argument_parser()
    
    def test_valid_arguments(self):
        """Test parsing of valid coordinate arguments."""
        # NYC to LA coordinates
        args = self.parser.parse_args(['40.7128', '-74.0060', '34.0522', '-118.2437'])
        
        self.assertEqual(args.lat1, 40.7128)
        self.assertEqual(args.lon1, -74.0060)
        self.assertEqual(args.lat2, 34.0522)
        self.assertEqual(args.lon2, -118.2437)
    
    def test_integer_coordinates(self):
        """Test parsing of integer coordinate arguments."""
        args = self.parser.parse_args(['40', '-74', '34', '-118'])
        
        self.assertEqual(args.lat1, 40.0)
        self.assertEqual(args.lon1, -74.0)
        self.assertEqual(args.lat2, 34.0)
        self.assertEqual(args.lon2, -118.0)
    
    def test_insufficient_arguments(self):
        """Test error handling for insufficient arguments."""
        with self.assertRaises(SystemExit):
            self.parser.parse_args(['40.7128', '-74.0060'])  # Missing lat2, lon2
            
        with self.assertRaises(SystemExit):
            self.parser.parse_args([])  # No arguments
    
    def test_non_numeric_arguments(self):
        """Test error handling for non-numeric coordinate arguments.""" 
        with self.assertRaises(SystemExit):
            self.parser.parse_args(['abc', '-74.0060', '34.0522', '-118.2437'])
            
        with self.assertRaises(SystemExit):  
            self.parser.parse_args(['40.7128', 'xyz', '34.0522', '-118.2437'])
    
    def test_help_argument(self):
        """Test that help argument displays usage information."""
        with self.assertRaises(SystemExit) as cm:
            self.parser.parse_args(['--help'])
        
        # argparse raises SystemExit with code 0 for help
        self.assertEqual(cm.exception.code, 0)
    
    def test_version_argument(self):
        """Test that version argument displays version information."""
        with self.assertRaises(SystemExit) as cm:
            self.parser.parse_args(['--version'])
        
        # argparse raises SystemExit with code 0 for version
        self.assertEqual(cm.exception.code, 0)


class TestCoordinateParsing(unittest.TestCase):
    """Test cases for coordinate parsing and validation."""
    
    def test_valid_coordinate_parsing(self):
        """Test parsing of valid coordinates into GeographicPoint objects."""
        # Create mock args object
        class MockArgs:
            def __init__(self, lat1, lon1, lat2, lon2):
                self.lat1 = lat1
                self.lon1 = lon1  
                self.lat2 = lat2
                self.lon2 = lon2
        
        args = MockArgs(40.7128, -74.0060, 34.0522, -118.2437)
        origin, destination = parse_coordinates(args)
        
        self.assertIsInstance(origin, GeographicPoint)
        self.assertIsInstance(destination, GeographicPoint)
        self.assertEqual(origin.latitude, 40.7128)
        self.assertEqual(origin.longitude, -74.0060)
        self.assertEqual(destination.latitude, 34.0522)
        self.assertEqual(destination.longitude, -118.2437)
    
    def test_invalid_coordinate_ranges(self):
        """Test error handling for coordinates outside valid ranges."""
        class MockArgs:
            def __init__(self, lat1, lon1, lat2, lon2):
                self.lat1 = lat1
                self.lon1 = lon1
                self.lat2 = lat2
                self.lon2 = lon2
        
        # Invalid latitude (>90)
        args = MockArgs(95.0, -74.0060, 34.0522, -118.2437)
        with self.assertRaises(ValueError) as cm:
            parse_coordinates(args)
        # Check for enhanced coordinate validation error message
        self.assertIn("Latitude 95.0 is outside valid range", str(cm.exception))
        self.assertIn("Geographic coordinate constraints", str(cm.exception))
        
        # Invalid longitude (>180)
        args = MockArgs(40.7128, 200.0, 34.0522, -118.2437)
        with self.assertRaises(ValueError) as cm:
            parse_coordinates(args)
        # Check for enhanced coordinate validation error message  
        self.assertIn("Longitude 200.0 is outside valid range", str(cm.exception))
        self.assertIn("Geographic coordinate constraints", str(cm.exception))


class TestOutputFormatting(unittest.TestCase):
    """Test cases for distance output formatting."""
    
    def test_basic_output_format(self):
        """Test basic distance output formatting for User Story 1."""
        origin = GeographicPoint(40.7128, -74.0060)  # NYC
        destination = GeographicPoint(34.0522, -118.2437)  # LA
        calc = DistanceCalculation(origin, destination)
        
        output = format_basic_output(calc)
        
        # Should be in format "XXXX.XX km"
        self.assertRegex(output, r'^\d+\.\d{2} km$')
        self.assertIn('km', output)
        
        # Should contain reasonable distance value for NYC-LA
        # Extract numeric part
        distance_str = output.split()[0]
        distance_value = float(distance_str)
        self.assertGreater(distance_value, 3000)  # More than 3000 km
        self.assertLess(distance_value, 5000)     # Less than 5000 km
    
    def test_zero_distance_formatting(self):
        """Test formatting of zero distance (identical coordinates)."""
        london = GeographicPoint(51.5074, -0.1278)
        calc = DistanceCalculation(london, london)
        
        output = format_basic_output(calc)
        self.assertEqual(output, "0.00 km")
    
    def test_decimal_precision(self):
        """Test that output maintains 2 decimal places."""
        origin = GeographicPoint(51.5074, -0.1278)   # London
        destination = GeographicPoint(48.8566, 2.3522)  # Paris
        calc = DistanceCalculation(origin, destination)
        
        output = format_basic_output(calc)
        
        # Extract numeric part and check decimal places
        distance_str = output.split()[0]
        # Should have exactly 2 decimal places
        self.assertRegex(distance_str, r'^\d+\.\d{2}$')
    
    def test_enhanced_output_kilometers(self):
        """Test enhanced output formatting with kilometers and various precision."""
        origin = GeographicPoint(40.7128, -74.0060)  # NYC
        destination = GeographicPoint(34.0522, -118.2437)  # LA  
        distance_calc = DistanceCalculation(origin, destination)
        
        # Test different precision levels
        result_0 = format_enhanced_output(distance_calc, 'km', 0)
        self.assertEqual(result_0, '3936 km')
        
        result_1 = format_enhanced_output(distance_calc, 'km', 1)
        self.assertEqual(result_1, '3935.7 km')
        
        result_3 = format_enhanced_output(distance_calc, 'km', 3)
        self.assertEqual(result_3, '3935.746 km')
    
    def test_enhanced_output_miles(self):
        """Test enhanced output formatting with miles and various precision."""
        origin = GeographicPoint(40.7128, -74.0060)  # NYC
        destination = GeographicPoint(34.0522, -118.2437)  # LA
        distance_calc = DistanceCalculation(origin, destination)
        
        # Test different precision levels
        result_0 = format_enhanced_output(distance_calc, 'miles', 0)
        self.assertEqual(result_0, '2446 miles')
        
        result_2 = format_enhanced_output(distance_calc, 'miles', 2)
        self.assertEqual(result_2, '2445.56 miles')
        
        result_4 = format_enhanced_output(distance_calc, 'miles', 4)
        self.assertEqual(result_4, '2445.5586 miles')
    
    def test_enhanced_output_nautical(self):
        """Test enhanced output formatting with nautical miles."""
        origin = GeographicPoint(40.7128, -74.0060)  # NYC
        destination = GeographicPoint(34.0522, -118.2437)  # LA
        distance_calc = DistanceCalculation(origin, destination)
        
        # Test different precision levels
        result_1 = format_enhanced_output(distance_calc, 'nautical', 1)
        self.assertEqual(result_1, '2125.1 nautical miles')
        
        result_3 = format_enhanced_output(distance_calc, 'nautical', 3)
        self.assertEqual(result_3, '2125.134 nautical miles')
    
    def test_enhanced_output_zero_distance(self):
        """Test enhanced output formatting with zero distance."""
        origin = GeographicPoint(0, 0)
        destination = GeographicPoint(0, 0)
        distance_calc = DistanceCalculation(origin, destination)
        
        # Test with different units
        result_km = format_enhanced_output(distance_calc, 'km', 1)
        self.assertEqual(result_km, '0.0 km')
        
        result_miles = format_enhanced_output(distance_calc, 'miles', 2) 
        self.assertEqual(result_miles, '0.00 miles')
        
        result_nautical = format_enhanced_output(distance_calc, 'nautical', 0)
        self.assertEqual(result_nautical, '0 nautical miles')


class TestEnhancedCLIArguments(unittest.TestCase):
    """Test cases for User Story 3 CLI argument parsing and integration."""
    
    def test_unit_argument_validation(self):
        """Test that --unit argument accepts valid units."""
        parser = create_argument_parser()
        
        # Test valid units
        for unit in ['km', 'miles', 'nautical']:
            with self.subTest(unit=unit):
                args = parser.parse_args(['0', '0', '1', '1', '--unit', unit])
                self.assertEqual(args.unit, unit)
    
    def test_precision_argument_validation(self):
        """Test that --precision argument accepts valid range."""
        parser = create_argument_parser()
        
        # Test valid precision values
        for precision in range(0, 7):  # 0-6 inclusive
            with self.subTest(precision=precision):
                args = parser.parse_args(['0', '0', '1', '1', '--precision', str(precision)])
                self.assertEqual(args.precision, precision)
    
    def test_default_argument_values(self):
        """Test default values for unit and precision arguments."""
        parser = create_argument_parser()
        args = parser.parse_args(['0', '0', '1', '1'])
        
        self.assertEqual(args.unit, 'km')
        self.assertEqual(args.precision, 2)
    
    def test_combined_unit_precision_arguments(self):
        """Test using both --unit and --precision arguments together."""
        parser = create_argument_parser()
        args = parser.parse_args(['40', '-74', '34', '-118', '--unit', 'nautical', '--precision', '4'])
        
        self.assertEqual(args.unit, 'nautical')
        self.assertEqual(args.precision, 4)


class TestCLIIntegration(unittest.TestCase):
    """Integration tests for complete CLI functionality."""
    
    def test_successful_calculation(self):
        """Test complete successful distance calculation via CLI."""
        # NYC to LA calculation
        args = ['40.7128', '-74.0060', '34.0522', '-118.2437']
        
        # Capture stdout
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        
        with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
            exit_code = run_basic_calculation(args)
        
        # Check successful exit
        self.assertEqual(exit_code, 0)
        
        # Check output format
        output = stdout_capture.getvalue().strip()
        self.assertRegex(output, r'^\d+\.\d{2} km$')
        
        # Should have no error output
        stderr_output = stderr_capture.getvalue()
        self.assertEqual(stderr_output, '')
    
    def test_identical_coordinates(self):
        """Test CLI with identical coordinates (zero distance)."""
        args = ['51.5074', '-0.1278', '51.5074', '-0.1278']  # London to London
        
        stdout_capture = io.StringIO()
        
        with redirect_stdout(stdout_capture):
            exit_code = run_basic_calculation(args)
        
        self.assertEqual(exit_code, 0)
        output = stdout_capture.getvalue().strip()
        self.assertEqual(output, '0.00 km')
    
    def test_invalid_coordinate_range_error(self):
        """Test CLI error handling for invalid coordinate ranges."""
        args = ['95.0', '-74.0060', '34.0522', '-118.2437']  # Invalid latitude
        
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        
        with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
            exit_code = run_basic_calculation(args)
        
        # Should exit with error code 1 (user error)
        self.assertEqual(exit_code, 1)
        
        # Should have error message on stderr
        stderr_output = stderr_capture.getvalue()
        # Check for enhanced structured error message format
        self.assertIn('ERROR:', stderr_output)  # New structured error format
        self.assertIn('latitude', stderr_output.lower())
        self.assertIn('USAGE EXAMPLES:', stderr_output)  # Should include usage examples
        
        # Should have no stdout output
        stdout_output = stdout_capture.getvalue()
        self.assertEqual(stdout_output, '')
    
    def test_insufficient_arguments_error(self):
        """Test CLI error handling for insufficient arguments."""
        args = ['40.7128', '-74.0060']  # Missing destination coordinates
        
        stderr_capture = io.StringIO()
        
        with redirect_stderr(stderr_capture):
            exit_code = run_basic_calculation(args)
        
        # Should exit with error code (argparse exits with 2 for argument errors)
        self.assertNotEqual(exit_code, 0)
    
    def test_non_numeric_argument_error(self):
        """Test CLI error handling for non-numeric arguments.""" 
        args = ['abc', '-74.0060', '34.0522', '-118.2437']  # Non-numeric latitude
        
        stderr_capture = io.StringIO()
        
        with redirect_stderr(stderr_capture):
            exit_code = run_basic_calculation(args)
        
        # Should exit with error code (argparse exits with 2 for type errors)
        self.assertNotEqual(exit_code, 0)
    
    def test_edge_case_coordinates(self):
        """Test CLI with edge case coordinates (poles, date line)."""
        test_cases = [
            # North pole to equator  
            (['90.0', '0.0', '0.0', '0.0'], True),
            # Across international date line
            (['0.0', '179.0', '0.0', '-179.0'], True),
            # Boundary coordinates
            (['-90.0', '-180.0', '90.0', '180.0'], True),
        ]
        
        for args, should_succeed in test_cases:
            with self.subTest(args=args):
                stdout_capture = io.StringIO()
                stderr_capture = io.StringIO()
                
                with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
                    exit_code = run_basic_calculation(args)
                
                if should_succeed:
                    self.assertEqual(exit_code, 0, f"Failed for args: {args}")
                    output = stdout_capture.getvalue().strip()
                    self.assertRegex(output, r'^\d+\.\d{2} km$')
    
    def test_performance_requirement(self):
        """Test that calculation completes within performance requirement (<1 second)."""
        import time
        
        args = ['40.7128', '-74.0060', '34.0522', '-118.2437']
        
        start_time = time.time()
        exit_code = run_basic_calculation(args)
        end_time = time.time()
        
        execution_time = end_time - start_time
        
        # Should complete successfully
        self.assertEqual(exit_code, 0)
        
        # Should complete in less than 1 second (performance requirement)
        self.assertLess(execution_time, 1.0, 
                       f"Calculation took {execution_time:.3f} seconds, should be <1.0")


if __name__ == '__main__':
    unittest.main()
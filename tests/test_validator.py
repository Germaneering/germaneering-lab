"""
Tests for haversine coordinate validation module.

This module tests coordinate validation functionality following Test-First
Development principles and Germaneering "Deep Code" doctrine.

Author: Germaneering Lab  
License: MIT
"""

import unittest
import math
from haversine.validator import CoordinateValidator, CoordinateValidationError


class TestCoordinateValidationError(unittest.TestCase):
    """Test coordinate validation error handling."""
    
    def test_error_properties(self):
        """Test that validation error contains coordinate context."""
        error = CoordinateValidationError("latitude", 91.0, "Invalid latitude")
        self.assertEqual(error.coordinate_type, "latitude")
        self.assertEqual(error.value, 91.0)
        self.assertIn("Invalid latitude", str(error))


class TestLatitudeValidation(unittest.TestCase):
    """Test latitude coordinate validation."""
    
    def test_valid_latitudes(self):
        """Test that valid latitude values pass validation."""
        valid_latitudes = [
            -90.0,  # South Pole
            -45.0,  # Southern hemisphere
            0.0,    # Equator  
            45.0,   # Northern hemisphere
            90.0,   # North Pole
            40.7128,  # NYC latitude
            51.5074,  # London latitude
        ]
        
        for lat in valid_latitudes:
            with self.subTest(latitude=lat):
                # Should not raise any exception
                CoordinateValidator.validate_latitude(lat)
    
    def test_invalid_latitudes_too_high(self):
        """Test that latitude values above 90 degrees raise errors."""
        invalid_latitudes = [90.1, 91.0, 100.0, 180.0, 360.0]
        
        for lat in invalid_latitudes:
            with self.subTest(latitude=lat):
                with self.assertRaises(CoordinateValidationError) as context:
                    CoordinateValidator.validate_latitude(lat)
                error = context.exception
                self.assertEqual(error.coordinate_type, "latitude")
                self.assertEqual(error.value, lat)
                self.assertIn("outside valid range", str(error))
    
    def test_invalid_latitudes_too_low(self):
        """Test that latitude values below -90 degrees raise errors."""
        invalid_latitudes = [-90.1, -91.0, -100.0, -180.0, -360.0]
        
        for lat in invalid_latitudes:
            with self.subTest(latitude=lat):
                with self.assertRaises(CoordinateValidationError) as context:
                    CoordinateValidator.validate_latitude(lat)
                error = context.exception
                self.assertEqual(error.coordinate_type, "latitude")
                self.assertEqual(error.value, lat)


class TestLongitudeValidation(unittest.TestCase):
    """Test longitude coordinate validation."""
    
    def test_valid_longitudes(self):
        """Test that valid longitude values pass validation."""
        valid_longitudes = [
            -180.0,    # Date line (western side)
            -90.0,     # Western hemisphere
            0.0,       # Prime meridian
            90.0,      # Eastern hemisphere  
            180.0,     # Date line (eastern side)
            -74.0060,  # NYC longitude
            -0.1278,   # London longitude
            139.6503,  # Tokyo longitude
        ]
        
        for lon in valid_longitudes:
            with self.subTest(longitude=lon):
                # Should not raise any exception
                CoordinateValidator.validate_longitude(lon)
    
    def test_invalid_longitudes_too_high(self):
        """Test that longitude values above 180 degrees raise errors."""
        invalid_longitudes = [180.1, 181.0, 200.0, 360.0, 720.0]
        
        for lon in invalid_longitudes:
            with self.subTest(longitude=lon):
                with self.assertRaises(CoordinateValidationError) as context:
                    CoordinateValidator.validate_longitude(lon)
                error = context.exception
                self.assertEqual(error.coordinate_type, "longitude")
                self.assertEqual(error.value, lon)
                self.assertIn("outside valid range", str(error))
    
    def test_invalid_longitudes_too_low(self):
        """Test that longitude values below -180 degrees raise errors."""
        invalid_longitudes = [-180.1, -181.0, -200.0, -360.0, -720.0]
        
        for lon in invalid_longitudes:
            with self.subTest(longitude=lon):
                with self.assertRaises(CoordinateValidationError) as context:
                    CoordinateValidator.validate_longitude(lon)
                error = context.exception
                self.assertEqual(error.coordinate_type, "longitude")
                self.assertEqual(error.value, lon)


class TestCoordinatePairValidation(unittest.TestCase):
    """Test validation of complete coordinate pairs."""
    
    def test_valid_coordinate_pairs(self):
        """Test that valid coordinate pairs pass validation."""
        valid_pairs = [
            (0.0, 0.0),        # Origin (Equator + Prime Meridian)
            (90.0, 0.0),       # North Pole
            (-90.0, 0.0),      # South Pole
            (0.0, 180.0),      # Equator + Date Line
            (40.7128, -74.0060),  # NYC
            (51.5074, -0.1278),   # London
            (35.6762, 139.6503),  # Tokyo
        ]
        
        for lat, lon in valid_pairs:
            with self.subTest(coordinates=(lat, lon)):
                # Should not raise any exception
                CoordinateValidator.validate_coordinate_pair(lat, lon)
    
    def test_invalid_latitude_in_pair(self):
        """Test that invalid latitude in pair raises appropriate error."""
        with self.assertRaises(CoordinateValidationError) as context:
            CoordinateValidator.validate_coordinate_pair(91.0, 0.0)
        self.assertEqual(context.exception.coordinate_type, "latitude")
    
    def test_invalid_longitude_in_pair(self):
        """Test that invalid longitude in pair raises appropriate error."""
        with self.assertRaises(CoordinateValidationError) as context:
            CoordinateValidator.validate_coordinate_pair(0.0, -181.0)
        self.assertEqual(context.exception.coordinate_type, "longitude")
    
    def test_both_coordinates_invalid(self):
        """Test that first invalid coordinate is caught when both are invalid."""
        # Should catch latitude error first (latitude validation runs first)
        with self.assertRaises(CoordinateValidationError) as context:
            CoordinateValidator.validate_coordinate_pair(91.0, -181.0)
        self.assertEqual(context.exception.coordinate_type, "latitude")


class TestNumericValidation(unittest.TestCase):
    """Test validation of numeric string inputs."""
    
    def test_valid_numeric_strings(self):
        """Test that valid numeric strings are accepted."""
        valid_strings = [
            "0",
            "0.0",
            "1.5",
            "-1.5",
            "90",
            "-90",
            "180",
            "-180", 
            "40.7128",
            "-74.0060",
            "1e2",      # Scientific notation
            "-1.5e-2",  # Negative scientific notation
        ]
        
        for num_str in valid_strings:
            with self.subTest(string=num_str):
                self.assertTrue(CoordinateValidator.is_numeric_string(num_str))
    
    def test_invalid_numeric_strings(self):
        """Test that non-numeric strings are rejected."""
        invalid_strings = [
            "",          # Empty string
            "abc",       # Letters
            "12.34.56",  # Multiple decimal points
            "1.2.3e4",   # Invalid scientific notation
            "12°",       # Degree symbol
            "N",         # Cardinal direction
            "12 34",     # Space in number
            "12,34",     # Comma decimal separator
            "∞",         # Infinity symbol
            "inf",       # Infinity string
            "-inf",      # Negative infinity string
            "NaN",       # Not a Number
            None,        # None type
        ]
        
        for invalid_str in invalid_strings:
            with self.subTest(string=invalid_str):
                self.assertFalse(CoordinateValidator.is_numeric_string(invalid_str))


class TestSpecialValues(unittest.TestCase):
    """Test validation behavior with special floating-point values."""
    
    def test_infinity_coordinates(self):
        """Test that infinite coordinates are rejected."""
        with self.assertRaises(CoordinateValidationError):
            CoordinateValidator.validate_latitude(float('inf'))
        
        with self.assertRaises(CoordinateValidationError):
            CoordinateValidator.validate_longitude(float('-inf'))
    
    def test_nan_coordinates(self):
        """Test that NaN coordinates are rejected."""
        with self.assertRaises(CoordinateValidationError):
            CoordinateValidator.validate_latitude(float('nan'))
        
        with self.assertRaises(CoordinateValidationError):
            CoordinateValidator.validate_longitude(float('nan'))


class TestValidationExamples(unittest.TestCase):
    """Test coordinate example functionality."""
    
    def test_examples_structure(self):
        """Test that coordinate examples have expected structure."""
        examples = CoordinateValidator.get_coordinate_examples()
        
        # Check top-level keys
        self.assertIn("cities", examples)
        self.assertIn("extremes", examples)
        self.assertIn("origin", examples)
        
        # Check cities structure
        self.assertIn("NYC", examples["cities"])
        self.assertIn("lat", examples["cities"]["NYC"])
        self.assertIn("lon", examples["cities"]["NYC"])
        
        # Check that all examples are valid coordinates
        for example_dict in [examples["cities"], examples["extremes"]]:
            for location, coords in example_dict.items():
                with self.subTest(location=location):
                    lat, lon = coords["lat"], coords["lon"]
                    # Should not raise validation errors
                    CoordinateValidator.validate_coordinate_pair(lat, lon)


if __name__ == '__main__':
    unittest.main()
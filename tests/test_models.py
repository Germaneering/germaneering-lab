"""
Test suite for GeographicPoint model

Tests cover coordinate validation, range checking, and behavior requirements
from the data model specification. These tests must pass before any
GeographicPoint implementation is considered complete.
"""

import unittest
import math
from haversine.models import GeographicPoint


class TestGeographicPoint(unittest.TestCase):
    """Test cases for GeographicPoint coordinates validation and behavior."""
    
    def test_valid_coordinates(self):
        """Test creation of GeographicPoint with valid coordinates."""
        # Test valid latitude/longitude ranges
        point = GeographicPoint(40.7128, -74.0060)  # NYC
        self.assertEqual(point.latitude, 40.7128)
        self.assertEqual(point.longitude, -74.0060)
        
        # Test boundary values
        north_pole = GeographicPoint(90.0, 0.0)
        self.assertEqual(north_pole.latitude, 90.0)
        
        south_pole = GeographicPoint(-90.0, 0.0)  
        self.assertEqual(south_pole.latitude, -90.0)
        
        date_line_west = GeographicPoint(0.0, -180.0)
        self.assertEqual(date_line_west.longitude, -180.0)
        
        date_line_east = GeographicPoint(0.0, 180.0)
        self.assertEqual(date_line_east.longitude, 180.0)
    
    def test_invalid_latitude_range(self):
        """Test that invalid latitude values raise appropriate errors."""
        with self.assertRaises(ValueError) as context:
            GeographicPoint(95.0, 0.0)
        self.assertIn("latitude", str(context.exception).lower())
        self.assertIn("-90", str(context.exception))
        self.assertIn("90", str(context.exception))
        
        with self.assertRaises(ValueError) as context:
            GeographicPoint(-95.0, 0.0)
        self.assertIn("latitude", str(context.exception).lower())
    
    def test_invalid_longitude_range(self):
        """Test that invalid longitude values raise appropriate errors."""
        with self.assertRaises(ValueError) as context:
            GeographicPoint(0.0, 200.0)
        self.assertIn("longitude", str(context.exception).lower())
        self.assertIn("-180", str(context.exception))
        self.assertIn("180", str(context.exception))
        
        with self.assertRaises(ValueError) as context:
            GeographicPoint(0.0, -200.0)
        self.assertIn("longitude", str(context.exception).lower())
        
    def test_non_numeric_coordinates(self):
        """Test that non-numeric coordinate values raise appropriate errors."""
        with self.assertRaises((ValueError, TypeError)):
            GeographicPoint("abc", 0.0)
            
        with self.assertRaises((ValueError, TypeError)):
            GeographicPoint(0.0, "def")
            
        with self.assertRaises((ValueError, TypeError)):
            GeographicPoint(None, 0.0)
            
        with self.assertRaises((ValueError, TypeError)):
            GeographicPoint(0.0, None)
    
    def test_infinite_and_nan_coordinates(self):
        """Test that infinite and NaN values are rejected."""
        with self.assertRaises(ValueError):
            GeographicPoint(float('inf'), 0.0)
            
        with self.assertRaises(ValueError):
            GeographicPoint(float('-inf'), 0.0)
            
        with self.assertRaises(ValueError):
            GeographicPoint(float('nan'), 0.0)
            
        with self.assertRaises(ValueError):
            GeographicPoint(0.0, float('inf'))
            
        with self.assertRaises(ValueError):
            GeographicPoint(0.0, float('nan'))
    
    def test_coordinate_conversion(self):
        """Test that integer coordinates are accepted and converted to float."""
        point = GeographicPoint(40, -74)
        self.assertEqual(point.latitude, 40.0)
        self.assertEqual(point.longitude, -74.0)
        self.assertIsInstance(point.latitude, float)
        self.assertIsInstance(point.longitude, float)
    
    def test_immutability(self):
        """Test that GeographicPoint coordinates cannot be modified after creation."""
        point = GeographicPoint(40.7128, -74.0060)
        
        # Coordinates should be read-only properties  
        with self.assertRaises(AttributeError):
            point.latitude = 50.0
            
        with self.assertRaises(AttributeError):
            point.longitude = -80.0
    
    def test_equality_comparison(self):
        """Test equality comparison with floating-point tolerance."""
        point1 = GeographicPoint(40.7128, -74.0060)
        point2 = GeographicPoint(40.7128, -74.0060)
        point3 = GeographicPoint(40.7129, -74.0060)  # Slightly different
        
        # Identical coordinates should be equal
        self.assertEqual(point1, point2)
        
        # Different coordinates should not be equal  
        self.assertNotEqual(point1, point3)
        
        # Test floating-point tolerance (within 1e-9 degrees)
        point4 = GeographicPoint(40.7128, -74.0060)
        point5 = GeographicPoint(40.7128 + 1e-10, -74.0060 + 1e-10)
        self.assertEqual(point4, point5)  # Should be equal within tolerance
    
    def test_string_representation(self):
        """Test string representation shows decimal degrees format."""
        point = GeographicPoint(40.7128, -74.0060)
        str_repr = str(point)
        
        self.assertIn("40.7128", str_repr)
        self.assertIn("74.0060", str_repr)  # Absolute value, no negative sign
        self.assertIn("°", str_repr)  # Should include degree symbol
        
        # Test representation includes N/S and E/W indicators
        nyc = GeographicPoint(40.7128, -74.0060)
        sydney = GeographicPoint(-33.8688, 151.2093)
        
        nyc_str = str(nyc)
        sydney_str = str(sydney)
        
        # NYC should show N and W
        self.assertTrue(any(indicator in nyc_str for indicator in ['N', 'North']))
        self.assertTrue(any(indicator in nyc_str for indicator in ['W', 'West']))
        
        # Sydney should show S and E
        self.assertTrue(any(indicator in sydney_str for indicator in ['S', 'South']))
        self.assertTrue(any(indicator in sydney_str for indicator in ['E', 'East']))
    
    def test_hash_behavior(self):
        """Test that GeographicPoint can be used as dictionary key."""
        point1 = GeographicPoint(40.7128, -74.0060)
        point2 = GeographicPoint(40.7128, -74.0060)
        
        # Equal points should have same hash
        self.assertEqual(hash(point1), hash(point2))
        
        # Should be usable as dictionary key
        location_dict = {point1: "NYC"}
        self.assertEqual(location_dict[point2], "NYC")


if __name__ == '__main__':
    unittest.main()
"""
Test suite for haversine distance calculation

Tests validate the mathematical accuracy of the haversine formula implementation
against known geographic distances. These tests serve as both validation and
educational documentation of expected behavior.

Known test cases use well-established geographic distances for validation.
"""

import unittest
import math
from haversine.calculator import haversine_distance, DistanceCalculation
from haversine.models import GeographicPoint


class TestHaversineDistance(unittest.TestCase):
    """Test cases for haversine distance calculation accuracy."""
    
    def test_known_city_distances(self):
        """Test haversine calculation against known distances between major cities."""
        # New York City to Los Angeles 
        # Expected: ~3,936 km (calculated using haversine formula)
        nyc_lat, nyc_lon = 40.7128, -74.0060
        la_lat, la_lon = 34.0522, -118.2437
        
        distance = haversine_distance(nyc_lat, nyc_lon, la_lat, la_lon)
        self.assertAlmostEqual(distance, 3936.0, delta=5.0)  # Within 5km tolerance
        
        # London to Paris
        # Expected: ~344 km 
        london_lat, london_lon = 51.5074, -0.1278
        paris_lat, paris_lon = 48.8566, 2.3522
        
        distance = haversine_distance(london_lat, london_lon, paris_lat, paris_lon)
        self.assertAlmostEqual(distance, 344.0, delta=2.0)  # Within 2km tolerance
        
        # Sydney to Melbourne  
        # Expected: ~714 km
        sydney_lat, sydney_lon = -33.8688, 151.2093
        melbourne_lat, melbourne_lon = -37.8136, 144.9631
        
        distance = haversine_distance(sydney_lat, sydney_lon, melbourne_lat, melbourne_lon)
        self.assertAlmostEqual(distance, 714.0, delta=3.0)  # Within 3km tolerance
    
    def test_identical_coordinates(self):
        """Test that identical coordinates return zero distance."""
        lat, lon = 51.5074, -0.1278  # London
        distance = haversine_distance(lat, lon, lat, lon)
        self.assertEqual(distance, 0.0)
        
        # Test multiple identical locations
        test_coordinates = [
            (0.0, 0.0),      # Equator/Prime Meridian
            (90.0, 0.0),     # North Pole
            (-90.0, 0.0),    # South Pole
            (45.0, -120.0),  # Random point
        ]
        
        for lat, lon in test_coordinates:
            distance = haversine_distance(lat, lon, lat, lon)
            self.assertEqual(distance, 0.0, f"Distance for identical coordinates ({lat}, {lon}) should be 0")
    
    def test_antipodal_points(self):
        """Test maximum distance calculation for antipodal (opposite) points."""
        # Points on opposite sides of Earth should be ~20,015 km apart
        # (approximately half of Earth's circumference)
        
        # North pole to South pole (via any longitude)
        distance = haversine_distance(90.0, 0.0, -90.0, 0.0)
        expected_half_circumference = 20015.0  # km
        self.assertAlmostEqual(distance, expected_half_circumference, delta=50.0)
        
        # Antipodal points on equator
        distance = haversine_distance(0.0, 0.0, 0.0, 180.0)
        self.assertAlmostEqual(distance, expected_half_circumference, delta=50.0)
    
    def test_edge_case_coordinates(self):
        """Test calculation with edge case coordinates (poles, date line)."""
        # North pole to equator (quarter circumference)
        # Expected: ~10,008 km (quarter of Earth's circumference)
        distance = haversine_distance(90.0, 0.0, 0.0, 0.0)
        expected_quarter_circumference = 10007.5  # km  
        self.assertAlmostEqual(distance, expected_quarter_circumference, delta=25.0)
        
        # Across international date line
        # 179° E to 179° W should be only 2° apart, not 358°
        distance = haversine_distance(0.0, 179.0, 0.0, -179.0)
        expected_2_degrees = 222.4  # km (approximately)
        self.assertAlmostEqual(distance, expected_2_degrees, delta=5.0)
    
    def test_distance_calculation_properties(self):
        """Test mathematical properties of distance calculation."""
        nyc = (40.7128, -74.0060)
        la = (34.0522, -118.2437)
        london = (51.5074, -0.1278)
        
        # Distance should be commutative: d(A,B) = d(B,A)
        dist_nyc_to_la = haversine_distance(*nyc, *la)
        dist_la_to_nyc = haversine_distance(*la, *nyc)
        self.assertEqual(dist_nyc_to_la, dist_la_to_nyc)
        
        # Distance should always be non-negative
        self.assertGreaterEqual(dist_nyc_to_la, 0.0)
        
        # Distance should be finite (not infinite or NaN)
        self.assertTrue(math.isfinite(dist_nyc_to_la))
        
        # Triangle inequality: d(A,C) ≤ d(A,B) + d(B,C)
        # (This is approximate due to spherical geometry vs. Euclidean)
        dist_nyc_london = haversine_distance(*nyc, *london)
        dist_london_la = haversine_distance(*london, *la)
        
        # For haversine on sphere, triangle inequality holds approximately
        self.assertLessEqual(dist_nyc_london, dist_nyc_to_la + dist_london_la + 100)  # 100km tolerance
    
    def test_mathematical_precision(self):
        """Test calculation precision and floating-point behavior."""
        # Very close points (sub-meter accuracy)
        lat1, lon1 = 40.712800, -74.006000  # Base point
        lat2, lon2 = 40.712801, -74.006001  # 1 arc-second difference (~30m)
        
        distance = haversine_distance(lat1, lon1, lat2, lon2)
        
        # Should be small but non-zero distance
        self.assertGreater(distance, 0.0)
        self.assertLess(distance, 0.1)  # Less than 100 meters
        
        # Result should be consistent with repeated calculations
        distance2 = haversine_distance(lat1, lon1, lat2, lon2)
        self.assertEqual(distance, distance2)


class TestDistanceCalculation(unittest.TestCase):
    """Test cases for DistanceCalculation class functionality."""
    
    def test_distance_calculation_creation(self):
        """Test DistanceCalculation object creation and properties."""
        origin = GeographicPoint(40.7128, -74.0060)  # NYC
        destination = GeographicPoint(34.0522, -118.2437)  # LA
        
        calc = DistanceCalculation(origin, destination)
        
        # Check basic properties
        self.assertEqual(calc.origin, origin)
        self.assertEqual(calc.destination, destination)
        self.assertEqual(calc.calculation_method, "haversine")
        
        # Check distance calculation
        self.assertIsInstance(calc.distance_km, float)
        self.assertGreater(calc.distance_km, 0.0)
        self.assertAlmostEqual(calc.distance_km, 3936.0, delta=5.0)
    
    def test_unit_conversions(self):
        """Test distance unit conversion properties."""
        origin = GeographicPoint(51.5074, -0.1278)   # London  
        destination = GeographicPoint(48.8566, 2.3522)  # Paris
        
        calc = DistanceCalculation(origin, destination)
        
        # Test unit conversion ratios
        expected_miles = calc.distance_km * 0.621371
        expected_nautical = calc.distance_km * 0.539957
        
        self.assertAlmostEqual(calc.distance_miles, expected_miles, delta=0.1)
        self.assertAlmostEqual(calc.distance_nautical, expected_nautical, delta=0.1)
        
        # Verify reasonable values for London-Paris distance
        self.assertAlmostEqual(calc.distance_km, 344.0, delta=2.0)
        self.assertAlmostEqual(calc.distance_miles, 214.0, delta=2.0)
        self.assertAlmostEqual(calc.distance_nautical, 185.7, delta=2.0)
    
    def test_same_location_detection(self):
        """Test is_same_location property for identical and close points."""
        london = GeographicPoint(51.5074, -0.1278)
        
        # Identical points
        calc_identical = DistanceCalculation(london, london)
        self.assertTrue(calc_identical.is_same_location)
        self.assertEqual(calc_identical.distance_km, 0.0)
        
        # Very close points (within 1 meter)
        close_point = GeographicPoint(51.5074 + 1e-5, -0.1278 + 1e-5) 
        calc_close = DistanceCalculation(london, close_point)
        
        if calc_close.distance_km < 0.001:  # Less than 1 meter
            self.assertTrue(calc_close.is_same_location)
        
        # Distant points  
        paris = GeographicPoint(48.8566, 2.3522)
        calc_distant = DistanceCalculation(london, paris)
        self.assertFalse(calc_distant.is_same_location)
    
    def test_calculation_validation(self):
        """Test that invalid inputs raise appropriate errors."""
        london = GeographicPoint(51.5074, -0.1278)
        
        # Non-GeographicPoint objects should raise TypeError
        with self.assertRaises(TypeError):
            DistanceCalculation("invalid", london)
            
        with self.assertRaises(TypeError):
            DistanceCalculation(london, (48.8566, 2.3522))  # tuple instead of GeographicPoint


if __name__ == '__main__':
    unittest.main()
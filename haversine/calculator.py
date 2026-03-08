"""
Haversine distance calculation implementation.

This module implements the haversine formula for calculating great-circle 
distances between points on a sphere. The implementation demonstrates the 
Deep Code principle by showing mathematical understanding beneath abstraction - 
using only Python standard library trigonometric functions.

The haversine formula:
    a = sin²(Δφ/2) + cos φ1 ⋅ cos φ2 ⋅ sin²(Δλ/2)
    c = 2 ⋅ atan2( √a, √(1−a) )
    d = R ⋅ c

Where:
    φ is latitude, λ is longitude, R is Earth's radius (6371 km)
    Δφ is the difference in latitudes, Δλ is the difference in longitudes
    d is the distance between the two points

Author: Germaneering Lab
License: Apache V2
"""

import math
from typing import Union
from .models import GeographicPoint


# Earth's radius in kilometers (mean radius used for haversine formula)
EARTH_RADIUS_KM = 6371.0

# Unit conversion factors
KM_TO_MILES = 0.621371
KM_TO_NAUTICAL_MILES = 0.539957


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great-circle distance between two points using the haversine formula.
    
    This function implements the haversine formula from mathematical primitives,
    demonstrating awareness beneath abstraction. All trigonometric calculations
    are performed using Python's standard math module to show the mathematical
    foundation of geographic distance calculations.
    
    The haversine formula is well-suited for calculating distances on a sphere
    and avoids the numerical instability of the law of cosines for small distances.
    
    Args:
        lat1: Origin latitude in decimal degrees
        lon1: Origin longitude in decimal degrees  
        lat2: Destination latitude in decimal degrees
        lon2: Destination longitude in decimal degrees
        
    Returns:
        Distance in kilometers (float)
        
    Raises:
        ValueError: If any coordinate is infinite or NaN
        
    Example:
        >>> # New York City to Los Angeles
        >>> distance = haversine_distance(40.7128, -74.0060, 34.0522, -118.2437)
        >>> round(distance, 1)
        3944.4
        
        >>> # London to Paris  
        >>> distance = haversine_distance(51.5074, -0.1278, 48.8566, 2.3522)
        >>> round(distance, 1) 
        344.0
    """
    # Validate input coordinates for mathematical operations
    coordinates = [lat1, lon1, lat2, lon2]
    for i, coord in enumerate(coordinates):
        if not math.isfinite(coord):
            coord_names = ["lat1", "lon1", "lat2", "lon2"]
            raise ValueError(f"Coordinate {coord_names[i]} must be finite, got {coord}")
    
    # Convert decimal degrees to radians for trigonometric calculations
    # This conversion is fundamental to the mathematical implementation
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    # Calculate differences in coordinates
    # Δφ (delta phi) = difference in latitudes
    # Δλ (delta lambda) = difference in longitudes  
    delta_lat = lat2_rad - lat1_rad
    delta_lon = lon2_rad - lon1_rad
    
    # Haversine formula implementation from mathematical primitives:
    #
    # Step 1: Calculate 'a' using the haversine of the central angle
    # a = sin²(Δφ/2) + cos φ1 ⋅ cos φ2 ⋅ sin²(Δλ/2)
    #
    # This represents the square of half the chord length between points
    sin_half_delta_lat = math.sin(delta_lat / 2)
    sin_half_delta_lon = math.sin(delta_lon / 2)
    
    a = (sin_half_delta_lat * sin_half_delta_lat + 
         math.cos(lat1_rad) * math.cos(lat2_rad) * 
         sin_half_delta_lon * sin_half_delta_lon)
    
    # Step 2: Calculate the central angle 'c' using atan2 for numerical stability
    # c = 2 ⋅ atan2( √a, √(1−a) )
    #
    # atan2 is preferred over asin for better numerical stability
    # especially for antipodal points (opposite sides of Earth)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    # Step 3: Calculate the distance using Earth's radius
    # d = R ⋅ c
    #
    # Earth's mean radius = 6371 km (spherical approximation)
    distance = EARTH_RADIUS_KM * c
    
    return distance


class DistanceCalculation:
    """
    Encapsulates a haversine distance calculation between two geographic points.
    
    This class represents a complete distance calculation with the origin and 
    destination points, calculated distance, and unit conversions. It provides
    a clear interface for accessing distance results in different units while
    maintaining the mathematical calculation method for educational reference.
    
    Attributes:
        origin (GeographicPoint): Starting coordinate
        destination (GeographicPoint): Ending coordinate
        distance_km (float): Calculated distance in kilometers
        calculation_method (str): Always "haversine" for this implementation
        
    Properties:
        distance_miles (float): Distance in statute miles
        distance_nautical (float): Distance in nautical miles  
        is_same_location (bool): True if points are effectively identical (<1m apart)
    """
    
    def __init__(self, origin: GeographicPoint, destination: GeographicPoint):
        """
        Initialize distance calculation between two geographic points.
        
        Args:
            origin: Starting point (GeographicPoint)
            destination: Ending point (GeographicPoint)
            
        Raises:
            TypeError: If arguments are not GeographicPoint instances
            ValueError: If calculation produces invalid results
        """
        # Validate input types
        if not isinstance(origin, GeographicPoint):
            raise TypeError(f"Origin must be GeographicPoint, got {type(origin).__name__}")
        if not isinstance(destination, GeographicPoint):
            raise TypeError(f"Destination must be GeographicPoint, got {type(destination).__name__}")
        
        self._origin = origin
        self._destination = destination
        self._calculation_method = "haversine"
        
        # Perform the distance calculation using haversine formula
        self._distance_km = haversine_distance(
            origin.latitude, origin.longitude,
            destination.latitude, destination.longitude
        )
        
        # Validate calculation result
        if not math.isfinite(self._distance_km):
            raise ValueError(f"Distance calculation produced invalid result: {self._distance_km}")
        if self._distance_km < 0:
            raise ValueError(f"Distance cannot be negative: {self._distance_km}")
    
    @property
    def origin(self) -> GeographicPoint:
        """Get the origin point of the calculation."""
        return self._origin
    
    @property
    def destination(self) -> GeographicPoint:  
        """Get the destination point of the calculation."""
        return self._destination
    
    @property
    def distance_km(self) -> float:
        """Get the calculated distance in kilometers."""
        return self._distance_km
    
    @property
    def calculation_method(self) -> str:
        """Get the calculation method used (always 'haversine')."""
        return self._calculation_method
    
    @property
    def distance_miles(self) -> float:
        """
        Get the calculated distance in statute miles.
        
        Conversion factor: 1 km = 0.621371 miles
        
        Returns:
            Distance in statute miles
        """
        return self._distance_km * KM_TO_MILES
    
    @property
    def distance_nautical(self) -> float:
        """
        Get the calculated distance in nautical miles.
        
        Conversion factor: 1 km = 0.539957 nautical miles
        
        Returns:
            Distance in nautical miles
        """
        return self._distance_km * KM_TO_NAUTICAL_MILES
    
    @property
    def is_same_location(self) -> bool:
        """
        Determine if origin and destination are effectively the same location.
        
        Points are considered the same if they are less than 1 meter (0.001 km) apart.
        This accounts for floating-point precision limitations and practical GPS accuracy.
        
        Returns:
            True if points are within 1 meter of each other
        """
        return self._distance_km < 0.001  # Less than 1 meter
    
    def __str__(self) -> str:
        """
        Provide human-readable string representation of the calculation.
        
        Returns:
            String showing origin, destination, and distance
        """
        return (f"Distance from {self.origin} to {self.destination}: "
                f"{self.distance_km:.2f} km ({self.distance_miles:.2f} miles)")
    
    def __repr__(self) -> str:
        """
        Provide unambiguous string representation for debugging.
        
        Returns:
            String that could recreate the object
        """
        return (f"DistanceCalculation({self.origin!r}, {self.destination!r})")


# Convenience function aliases for backwards compatibility and ease of use
def calculate_distance(origin: GeographicPoint, destination: GeographicPoint) -> DistanceCalculation:
    """
    Convenience function to create a DistanceCalculation object.
    
    Args:
        origin: Starting point
        destination: Ending point
        
    Returns:
        DistanceCalculation object with computed distance
    """
    return DistanceCalculation(origin, destination)
"""
Geographic coordinate models for haversine distance calculation.

This module implements the GeographicPoint class that represents locations 
on Earth's surface using decimal degree coordinates. The implementation 
demonstrates the Deep Code principle by providing clear validation and 
representation of geographic concepts.

Author: Germaneering Lab  
License: Apache V2
"""

import math
from typing import Union


class GeographicPoint:
    """
    Represents a location on Earth's surface using decimal degree coordinates.
    
    This class encapsulates latitude and longitude values with comprehensive 
    validation to ensure coordinates are within valid geographic ranges.
    Implements immutable coordinate storage and provides clear string 
    representation for educational purposes.
    
    Attributes:
        latitude (float): North/South position in decimal degrees [-90.0, 90.0]
        longitude (float): East/West position in decimal degrees [-180.0, 180.0]
    
    Raises:
        ValueError: When coordinates are outside valid ranges or non-numeric
        TypeError: When coordinates cannot be converted to numeric values
    
    Example:
        >>> nyc = GeographicPoint(40.7128, -74.0060)
        >>> str(nyc)
        '40.7128°N, 74.0060°W'
        
        >>> london = GeographicPoint(51.5074, -0.1278) 
        >>> london.latitude
        51.5074
    """
    
    def __init__(self, latitude: Union[float, int], longitude: Union[float, int]):
        """
        Initialize a GeographicPoint with validated coordinates.
        
        Args:
            latitude: North/South position in decimal degrees [-90, 90]
            longitude: East/West position in decimal degrees [-180, 180]
            
        Raises:
            ValueError: If coordinates are outside valid ranges or non-finite
            TypeError: If coordinates cannot be converted to float
        """
        # Convert to float and validate numeric types
        try:
            lat_float = float(latitude)
            lon_float = float(longitude)
        except (ValueError, TypeError) as e:
            raise TypeError(f"Coordinates must be numeric values, got {type(latitude).__name__} and {type(longitude).__name__}") from e
        
        # Check for non-finite values (NaN, infinity)
        if not math.isfinite(lat_float):
            raise ValueError(f"Latitude must be finite, got {lat_float}")
        if not math.isfinite(lon_float):
            raise ValueError(f"Longitude must be finite, got {lon_float}")
            
        # Validate latitude range [-90, 90]
        if not -90.0 <= lat_float <= 90.0:
            raise ValueError(f"Latitude must be between -90 and 90 degrees, got {lat_float}")
            
        # Validate longitude range [-180, 180]  
        if not -180.0 <= lon_float <= 180.0:
            raise ValueError(f"Longitude must be between -180 and 180 degrees, got {lon_float}")
        
        # Store as immutable private attributes
        self._latitude = lat_float
        self._longitude = lon_float
    
    @property
    def latitude(self) -> float:
        """Get the latitude coordinate in decimal degrees."""
        return self._latitude
    
    @property  
    def longitude(self) -> float:
        """Get the longitude coordinate in decimal degrees."""
        return self._longitude
    
    def __eq__(self, other) -> bool:
        """
        Compare two GeographicPoint objects for equality with floating-point tolerance.
        
        Points are considered equal if their coordinates differ by less than 1e-9 degrees
        (approximately 0.1mm at the equator), accounting for floating-point precision.
        
        Args:
            other: Another GeographicPoint object to compare
            
        Returns:
            True if points are equal within tolerance, False otherwise
        """
        if not isinstance(other, GeographicPoint):
            return False
            
        tolerance = 1e-9  # Very small tolerance for floating-point comparison
        return (abs(self.latitude - other.latitude) < tolerance and 
                abs(self.longitude - other.longitude) < tolerance)
    
    def __hash__(self) -> int:
        """
        Generate hash for use as dictionary key.
        
        Rounds coordinates to 9 decimal places to ensure equal points 
        have identical hash values despite floating-point precision.
        
        Returns:
            Hash value based on rounded coordinates
        """
        # Round to 9 decimal places for consistent hashing
        lat_rounded = round(self.latitude, 9)
        lon_rounded = round(self.longitude, 9)
        return hash((lat_rounded, lon_rounded))
    
    def __str__(self) -> str:
        """
        Provide human-readable string representation with cardinal directions.
        
        Format shows absolute coordinate values with N/S and E/W indicators
        for educational clarity about geographic coordinate systems.
        
        Returns:
            String in format "XX.XXXX°N, XX.XXXX°W" style
            
        Examples:
            "40.7128°N, 74.0060°W"  (New York City)
            "33.8688°S, 151.2093°E" (Sydney)
        """
        # Determine cardinal directions
        lat_dir = "N" if self.latitude >= 0 else "S"
        lon_dir = "E" if self.longitude >= 0 else "W"
        
        # Use absolute values for display
        lat_abs = abs(self.latitude)
        lon_abs = abs(self.longitude)
        
        return f"{lat_abs:.4f}°{lat_dir}, {lon_abs:.4f}°{lon_dir}"
    
    def __repr__(self) -> str:
        """
        Provide unambiguous string representation for debugging.
        
        Returns:
            String that could recreate the object
        """
        return f"GeographicPoint({self.latitude}, {self.longitude})"
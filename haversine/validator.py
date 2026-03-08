"""
Input validation module for haversine CLI calculator.

This module provides coordinate validation functionality following the Test-First
Development principle and Germaneering "Deep Code" doctrine by implementing
validation logic from mathematical and geographical primitives.

Author: Germaneering Lab
License: MIT
"""

import math

class CoordinateValidationError(ValueError):
    """Raised when coordinate values are invalid."""
    
    def __init__(self, coordinate_type: str, value: float, message: str):
        self.coordinate_type = coordinate_type
        self.value = value
        super().__init__(message)


class CoordinateValidator:
    """
    Validates coordinate values for latitude and longitude ranges.
    
    This class implements validation logic based on geographical constraints:
    - Latitude: [-90, 90] degrees (North/South poles)
    - Longitude: [-180, 180] degrees (International Date Line)
    """
    
    # Geographical coordinate constraints
    MIN_LATITUDE = -90.0
    MAX_LATITUDE = 90.0
    MIN_LONGITUDE = -180.0
    MAX_LONGITUDE = 180.0
    
    @staticmethod
    def validate_latitude(value: float) -> None:
        """
        Validate latitude coordinate range.
        
        Args:
            value: Latitude in decimal degrees
            
        Raises:
            CoordinateValidationError: If latitude is outside [-90, 90] range
        """
        if not (CoordinateValidator.MIN_LATITUDE <= value <= CoordinateValidator.MAX_LATITUDE):
            raise CoordinateValidationError(
                coordinate_type="latitude",
                value=value,
                message=f"Latitude {value} is outside valid range [{CoordinateValidator.MIN_LATITUDE}, {CoordinateValidator.MAX_LATITUDE}]"
            )
    
    @staticmethod
    def validate_longitude(value: float) -> None:
        """
        Validate longitude coordinate range.
        
        Args:
            value: Longitude in decimal degrees
            
        Raises:
            CoordinateValidationError: If longitude is outside [-180, 180] range
        """
        if not (CoordinateValidator.MIN_LONGITUDE <= value <= CoordinateValidator.MAX_LONGITUDE):
            raise CoordinateValidationError(
                coordinate_type="longitude", 
                value=value,
                message=f"Longitude {value} is outside valid range [{CoordinateValidator.MIN_LONGITUDE}, {CoordinateValidator.MAX_LONGITUDE}]"
            )
    
    @staticmethod
    def validate_coordinate_pair(lat: float, lon: float) -> None:
        """
        Validate a complete coordinate pair.
        
        Args:
            lat: Latitude in decimal degrees
            lon: Longitude in decimal degrees
            
        Raises:
            CoordinateValidationError: If either coordinate is invalid
        """
        CoordinateValidator.validate_latitude(lat)
        CoordinateValidator.validate_longitude(lon)
    
    @staticmethod
    def is_numeric_string(value: str) -> bool:
        """
        Check if a string represents a valid numeric coordinate.
        
        Args:
            value: String to validate
            
        Returns:
            bool: True if string can be converted to float, False otherwise
        """
        try:
            parsed_value = float(value)
            # Reject infinite and NaN values
            if not math.isfinite(parsed_value):
                return False
            return True
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def get_coordinate_examples() -> dict:
        """
        Get examples of valid coordinates for help messages.
        
        Returns:
            dict: Examples organized by category
        """
        return {
            "cities": {
                "NYC": {"lat": 40.7128, "lon": -74.0060},
                "London": {"lat": 51.5074, "lon": -0.1278},
                "Tokyo": {"lat": 35.6762, "lon": 139.6503},
            },
            "extremes": {
                "North Pole": {"lat": 90.0, "lon": 0.0},
                "South Pole": {"lat": -90.0, "lon": 0.0},
                "Date Line": {"lat": 0.0, "lon": 180.0},
            },
            "origin": {"lat": 0.0, "lon": 0.0},  # Equator and Prime Meridian
        }
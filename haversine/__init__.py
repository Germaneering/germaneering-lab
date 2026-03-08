"""
Haversine CLI Calculator

A minimal CLI application that calculates great-circle distance between two 
geographic points using only Python standard library modules. This tool 
demonstrates the Germaneering "Deep Code" principle by implementing the 
haversine formula from mathematical primitives.

Usage:
    python -m haversine <lat1> <lon1> <lat2> <lon2> [OPTIONS]
    uv run haversine <lat1> <lon1> <lat2> <lon2> [OPTIONS]

Author: Germaneering Lab
License: Apache V2
"""

__version__ = "1.0.0"
__author__ = "Germaneering Lab"
__license__ = "Apache V2"

# Import after module definition to avoid circular imports
try:
    # Core components that implement the haversine calculation
    from .models import GeographicPoint
    from .calculator import haversine_distance, DistanceCalculation
    
    __all__ = ["GeographicPoint", "haversine_distance", "DistanceCalculation", "__version__"]
    
except ImportError:
    # Graceful degradation if modules not yet implemented
    __all__ = ["__version__"]
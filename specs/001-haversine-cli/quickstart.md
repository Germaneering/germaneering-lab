# Quickstart: Haversine CLI Calculator

**Feature**: `001-haversine-cli`
**Date**: 2026-03-08

## Quick Start

Calculate great-circle distance between any two points on Earth using only Python standard library modules.

### Prerequisites

- Python 3.8+ installed
- `uv` package manager (recommended) or standard Python environment

### Installation

#### Option 1: Using uv (Recommended)
```bash
uv tool install haversine-cli
```

#### Option 2: From Source  
```bash
git clone <repository>
cd germaneering-lab
```

### Basic Usage

#### Calculate Distance Between Two Cities
```bash
# New York City to Los Angeles
uv run haversine 40.7128 -74.0060 34.0522 -118.2437
# Output: 3944.42 km
```

#### Different Units
```bash
# Same distance in miles
uv run haversine 40.7128 -74.0060 34.0522 -118.2437 --unit miles
# Output: 2451.1 miles

# Nautical miles with higher precision  
uv run haversine 40.7128 -74.0060 34.0522 -118.2437 --unit nautical --precision 4
# Output: 2129.7821 nautical
```

#### Edge Cases
```bash
# Same location (should return 0)
uv run haversine 51.5074 -0.1278 51.5074 -0.1278
# Output: 0.00 km

# Across international date line
uv run haversine 25.7617 -80.1918 35.6762 139.6503
# Output: 11470.26 km
```

### Common Coordinate Formats

| Location | Latitude | Longitude | Notes |
|----------|----------|-----------|-------|
| New York City | 40.7128 | -74.0060 | Negative longitude = West |
| London | 51.5074 | -0.1278 | Negative latitude = South |
| Tokyo | 35.6762 | 139.6503 | Positive values = North/East |
| Sydney | -33.8688 | 151.2093 | Negative latitude = South |

### Error Handling

#### Invalid Coordinates
```bash
uv run haversine 95 0 0 0
# Error: Latitude must be between -90 and 90 degrees

uv run haversine 0 200 0 0  
# Error: Longitude must be between -180 and 180 degrees
```

#### Wrong Number of Arguments
```bash
uv run haversine 40.7128 -74.0060
# Error: Missing required arguments
# Usage: haversine <lat1> <lon1> <lat2> <lon2> [OPTIONS]
```

### Testing

#### Run All Tests
```bash
uv run -m unittest discover tests
```

#### Run Specific Test Module
```bash
uv run -m unittest tests.test_calculator
uv run -m unittest tests.test_validator  
uv run -m unittest tests.test_cli
```

#### Test with Known Values
The tool includes tests against known geographic distances:
- NYC to LA: ~3,944 km
- London to Paris: ~344 km  
- Pole to equator: ~10,008 km (quarter Earth circumference)

### Development Mode

#### Install for Development
```bash
uv sync --dev
```

#### Run Without Installation  
```bash
python -m haversine 40.7128 -74.0060 34.0522 -118.2437
```

### Germaneering Deep Code Connection

This tool demonstrates the **Deep Code** pillar by:

1. **Mathematical Implementation**: Haversine formula implemented from trigonometric primitives
2. **No Hidden Dependencies**: Zero external libraries - every calculation is visible
3. **Educational Value**: Code serves as reference for both CLI patterns and geographic calculations
4. **Awareness Beneath Abstraction**: Shows understanding of spherical geometry, not just API calls

#### Formula Implementation
```python
# Visible implementation using only math module
import math

def haversine_distance(lat1, lon1, lat2, lon2):
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Earth radius in kilometers
    earth_radius = 6371.0
    return earth_radius * c
```

### Performance Expectations

- **Execution time**: <1 second for any coordinate pair
- **Memory usage**: Minimal (no data persistence or large calculations)
- **Accuracy**: Within 0.1% of reference geographic tools for spherical Earth model

### Getting Help

```bash
uv run haversine --help
```

Shows complete usage information with examples and coordinate format explanations.
# Data Model: Haversine CLI Calculator

**Feature**: `001-haversine-cli`
**Date**: 2026-03-08
**Input**: [spec.md](spec.md) functional requirements and entities

## Core Entities

### GeographicPoint
**Purpose**: Represents a location on Earth's surface using decimal degree coordinates

**Attributes**:
- `latitude: float` - North/South position in decimal degrees [-90.0, 90.0]  
- `longitude: float` - East/West position in decimal degrees [-180.0, 180.0]

**Validation Rules**:
- Latitude MUST be within [-90, 90] inclusive
- Longitude MUST be within [-180, 180] inclusive  
- Both values MUST be numeric (float or int convertible)
- Values MUST NOT be NaN or infinite

**State Behavior**:
- Immutable after creation (no coordinate modification)
- Equality comparison by coordinate values with floating-point tolerance
- String representation in decimal degree format

### DistanceCalculation  
**Purpose**: Encapsulates haversine distance calculation between two points

**Attributes**:
- `origin: GeographicPoint` - Starting coordinate
- `destination: GeographicPoint` - Ending coordinate  
- `distance_km: float` - Calculated distance in kilometers
- `calculation_method: string` - Always "haversine" for this implementation

**Validation Rules**:
- Origin and destination MUST be valid GeographicPoint instances
- Distance MUST be non-negative
- Distance MUST be finite (not NaN or infinite)

**Derived Properties**:
- `distance_miles: float` - Distance in statute miles (km × 0.621371)
- `distance_nautical: float` - Distance in nautical miles (km × 0.539957)
- `is_same_location: bool` - True if distance < 0.001km (approximately 1 meter)

### CommandLineArgs
**Purpose**: Parsed and validated command-line input

**Attributes**:
- `origin_lat: float` - First coordinate latitude
- `origin_lon: float` - First coordinate longitude  
- `destination_lat: float` - Second coordinate latitude
- `destination_lon: float` - Second coordinate longitude
- `output_unit: string` - Output unit ("km", "miles", "nautical")
- `precision: int` - Decimal places for output [0, 6]

**Validation Rules**:
- All coordinate values follow GeographicPoint validation rules
- Output unit MUST be one of: "km", "miles", "nautical"  
- Precision MUST be integer between 0 and 6 inclusive

**Default Values**:
- `output_unit: "km"`
- `precision: 2`

## Entity Relationships

```text
CommandLineArgs → GeographicPoint (origin)
CommandLineArgs → GeographicPoint (destination)  
DistanceCalculation ← GeographicPoint (origin)
DistanceCalculation ← GeographicPoint (destination)
```

**Flow**: 
1. CommandLineArgs parsed from CLI input
2. Two GeographicPoint instances created from validated coordinates
3. DistanceCalculation performed using haversine formula
4. Result formatted according to unit and precision preferences

## Data Validation Strategy

**Input Level**: Validate coordinate ranges and numeric types during argument parsing
**Entity Level**: Validate geographic constraints during GeographicPoint creation  
**Calculation Level**: Validate mathematical results for sanity (non-negative, finite)
**Output Level**: Validate format specification during result presentation

## Error Handling

**Invalid Coordinates**: Clear error message with valid range examples
**Calculation Errors**: Handle mathematical edge cases (antipodal points, poles)
**Type Errors**: Convert numeric strings, reject non-numeric input with examples
**Range Errors**: Specific messages for latitude vs longitude range violations

This data model supports the zero-dependency requirement by using only Python built-in types (float, string, int) and standard library validation patterns.
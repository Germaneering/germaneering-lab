# CLI Interface Contract

**Feature**: `001-haversine-cli`
**Date**: 2026-03-08
**Type**: Command Line Interface

## Command Signature

```bash
haversine <lat1> <lon1> <lat2> <lon2> [OPTIONS]
```

### Positional Arguments

| Parameter | Type | Range | Description |
|-----------|------|-------|-------------|
| `lat1` | float | [-90, 90] | Origin latitude in decimal degrees |
| `lon1` | float | [-180, 180] | Origin longitude in decimal degrees |
| `lat2` | float | [-90, 90] | Destination latitude in decimal degrees |
| `lon2` | float | [-180, 180] | Destination longitude in decimal degrees |

### Optional Arguments

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--unit` | string | "km" | Output unit: "km", "miles", "nautical" |
| `--precision` | int | 2 | Decimal places in output [0-6] |
| `--help` | flag | - | Display usage information |
| `--version` | flag | - | Display version information |

## Output Format

### Success (Exit Code 0)
```
<distance> <unit>
```

**Examples**:
```bash
$ haversine 40.7128 -74.0060 34.0522 -118.2437
3944.42 km

$ haversine 40.7128 -74.0060 34.0522 -118.2437 --unit miles --precision 1
2451.1 miles

$ haversine 51.5074 -0.1278 51.5074 -0.1278
0.00 km
```

### Error Cases (Exit Code 1)

#### Insufficient Arguments
```
Error: Missing required arguments
Usage: haversine <lat1> <lon1> <lat2> <lon2> [OPTIONS]
Example: haversine 40.7128 -74.0060 34.0522 -118.2437
```

#### Invalid Coordinate Ranges
```
Error: Latitude must be between -90 and 90 degrees
Got: 95.5

Error: Longitude must be between -180 and 180 degrees  
Got: 200.0
```

#### Invalid Numeric Format
```
Error: Coordinates must be numeric
Got: 'abc' for latitude

Error: Could not parse coordinate value
Got: '40.71.28' for longitude
```

#### Invalid Options
```
Error: Invalid unit 'kilometers'. Must be one of: km, miles, nautical

Error: Precision must be between 0 and 6
Got: 10
```

### Help Output (Exit Code 0)
```
haversine - Calculate great-circle distance between two points

Usage: haversine <lat1> <lon1> <lat2> <lon2> [OPTIONS]

Calculate the haversine distance between two geographic points using coordinates in decimal degrees.

Positional Arguments:
  lat1        Origin latitude [-90, 90]
  lon1        Origin longitude [-180, 180]  
  lat2        Destination latitude [-90, 90]
  lon2        Destination longitude [-180, 180]

Options:
  --unit      Output unit: km, miles, nautical (default: km)
  --precision Decimal places [0-6] (default: 2)
  --help      Show this help message
  --version   Show version information

Examples:
  haversine 40.7128 -74.0060 34.0522 -118.2437
  haversine 51.5074 -0.1278 48.8566 2.3522 --unit miles
  haversine 0 0 0 1 --precision 4

This tool demonstrates the Germaneering "Deep Code" principle by implementing 
the haversine formula from mathematical primitives using only Python standard 
library modules.
```

## Execution Methods

### Primary (via uv)
```bash
uv run haversine <args>
```

### Fallback (direct Python)  
```bash
python -m haversine <args>
```

### Package Installation
```bash
uv add --dev haversine
```

## Contract Validation

**Input validation**: All coordinate and option validation occurs before calculation
**Output consistency**: Distance format identical across all unit types (number + unit)
**Error consistency**: All error messages follow same format with examples
**Exit codes**: 0 for success, 1 for user errors, 2 for system errors
**Performance**: Command completes within 1 second for any coordinate pair

This contract ensures consistent and predictable behavior for all users while maintaining compatibility with both uv and standard Python execution environments.
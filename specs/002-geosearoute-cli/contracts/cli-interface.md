# CLI Interface Contract

**Feature**: `002-geosearoute-cli`  
**Date**: 2026-04-15  
**Type**: Command Line Interface

## Command Signatures

```bash
geosearoute-cli nearest <lat> <lon> [OPTIONS]
geosearoute-cli solve --stop <lon> <lat> --stop <lon> <lat> [--stop <lon> <lat> ...] [OPTIONS]
```

## Configuration Sources

### Environment Variables

| Variable | Description |
|----------|-------------|
| `x_rapidapi_host` | Value used for the `x-rapidapi-host` request header |
| `x_rapidapi_key` | Value used for the `x-rapidapi-key` request header |

### Fixed Service Endpoint

All commands target the fixed base URL:

```text
https://geosearoute.p.rapidapi.com
```

If either required environment variable is missing, the command fails before any HTTP request.

## `nearest` Command

### Positional Arguments

| Parameter | Type | Range | Description |
|-----------|------|-------|-------------|
| `lat` | float | [-90, 90] | Latitude in decimal degrees |
| `lon` | float | [-180, 180] | Longitude in decimal degrees |

### Optional Arguments

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--distance` | float | `500.0` | Search distance in kilometers; must be positive |
| `--help` | flag | - | Show command help |

### Remote Request Contract

```http
GET https://geosearoute.p.rapidapi.com/nearest?lat=<lat>&lon=<lon>&distance=<distance>

Headers:
  x-rapidapi-host: <value from x_rapidapi_host>
  x-rapidapi-key: <value from x_rapidapi_key>
```

## `solve` Command

### Required Arguments

| Flag | Type | Cardinality | Description |
|------|------|-------------|-------------|
| `--stop` | `<lon> <lat>` pair | 2 or more occurrences | Ordered route stops; each occurrence adds one stop |

### Optional Arguments

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--speed` | float | `24.0` | Vessel speed in knots; must be positive |
| `--help` | flag | - | Show command help |

### Remote Request Contract

```http
POST https://geosearoute.p.rapidapi.com/solve?speed=<speed>
Content-Type: application/json
x-rapidapi-host: <value from x_rapidapi_host>
x-rapidapi-key: <value from x_rapidapi_key>

{"stops": [[lon, lat], [lon, lat], ...]}
```

## Output Format

### Success Output (Exit Code 0)

Successful responses are written to stdout as pretty-printed JSON with stable indentation.

**Example**:

```bash
$ uv run geosearoute-cli nearest 57.7 11.9
{
  "point": {
    "lat": 57.701,
    "lon": 11.902
  },
  "distance": 1.24
}
```

```bash
$ uv run geosearoute-cli solve --stop 11.9 57.7 --stop 4.48 51.92 --speed 20
{
  "distance_nm": 423.1,
  "duration_hours": 21.2,
  "geometry": {
    "type": "LineString"
  }
}
```

### Error Output (Non-Zero Exit)

Errors are written to stderr as readable text. If the service returns a structured JSON error body, it is pretty-printed to stderr after a short summary line.

#### Missing Configuration (Exit Code 1)

```text
Error: Missing RapidAPI environment configuration.
Provide environment variable x_rapidapi_host.
Provide environment variable x_rapidapi_key.
```

#### Invalid Input (Exit Code 1)

```text
Error: Stop 2 has invalid latitude 123.4.
Latitude must be between -90 and 90.
```

#### Remote Failure (Exit Code 2)

```text
Error: Service request failed with HTTP 401 Unauthorized.
{
  "error": "invalid api key"
}
```

#### Transport Failure (Exit Code 2)

```text
Error: Could not reach geosearoute service.
Reason: Connection timed out.
```

## Top-Level Help Contract

```text
usage: geosearoute-cli [-h] {nearest,solve} ...

Manual tester for geosearoute service endpoints.

commands:
  nearest    Test GET /nearest with latitude, longitude, and optional distance
  solve      Test POST /solve with ordered stops and optional speed

configuration:
  fixed base URL         https://geosearoute.p.rapidapi.com
  x_rapidapi_host        Value for x-rapidapi-host header
  x_rapidapi_key         Value for x-rapidapi-key header
```

## Execution Methods

### Installed Console Script

```bash
uv run geosearoute-cli --help
```

### Module Execution

```bash
uv run python -m geosearoute_cli --help
```

## Contract Validation

**Input validation**: Coordinates, distances, speeds, and stop counts are validated before network I/O.  
**Configuration behavior**: Base URL is fixed; missing required RapidAPI environment variables fails early.  
**Output consistency**: Successful JSON responses are pretty-printed exactly once on stdout.  
**Error consistency**: All failures are readable and use stable exit code categories.  
**Ordering guarantee**: `solve` stops preserve the exact order supplied on the command line.
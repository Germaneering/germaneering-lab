# Data Model: Sea Route Service Tester CLI

**Feature**: `002-geosearoute-cli`  
**Date**: 2026-04-15  
**Input**: [spec.md](spec.md) functional requirements and entities

## Core Entities

### ServiceConfig
**Purpose**: Represents the runtime configuration required to call the fixed geosearoute RapidAPI endpoint.

**Attributes**:
- `base_url: str` - Fixed HTTPS base URL for the target service
- `rapidapi_host: str` - Non-empty header value for `x-rapidapi-host`
- `rapidapi_key: str` - Non-empty header value for `x-rapidapi-key`

**Validation Rules**:
- `base_url` MUST equal `https://geosearoute.p.rapidapi.com`
- `rapidapi_host` MUST be present in environment variable `x_rapidapi_host` and MUST NOT be blank after trimming whitespace
- `rapidapi_key` MUST be present in environment variable `x_rapidapi_key` and MUST NOT be blank after trimming whitespace
- Missing or invalid header configuration MUST prevent any outbound request

### NearestQuery
**Purpose**: Encapsulates the validated input for the `nearest` command.

**Attributes**:
- `latitude: float` - Input latitude in decimal degrees
- `longitude: float` - Input longitude in decimal degrees
- `distance_km: float` - Search radius in kilometers

**Validation Rules**:
- `latitude` MUST be within [-90, 90]
- `longitude` MUST be within [-180, 180]
- `distance_km` MUST be a positive numeric value

**Default Values**:
- `distance_km: 500.0`

### StopCoordinate
**Purpose**: Represents a single ordered waypoint used in the `solve` command.

**Attributes**:
- `longitude: float` - Stop longitude in decimal degrees
- `latitude: float` - Stop latitude in decimal degrees
- `index: int` - Original stop order as supplied on the command line

**Validation Rules**:
- `longitude` MUST be within [-180, 180]
- `latitude` MUST be within [-90, 90]
- `index` MUST start at 0 and remain contiguous in input order

### SolveQuery
**Purpose**: Encapsulates the validated input for the `solve` command before serialization to the service payload.

**Attributes**:
- `stops: list[StopCoordinate]` - Ordered stop collection for the route
- `speed_knots: float` - Vessel speed for route solving

**Validation Rules**:
- `stops` MUST contain at least two entries
- Each stop MUST contain exactly one longitude and one latitude
- `speed_knots` MUST be a positive numeric value

**Default Values**:
- `speed_knots: 24.0`

### ServiceRequest
**Purpose**: Normalized outbound HTTP request data derived from a command entity and runtime configuration.

**Attributes**:
- `method: str` - HTTP method (`GET` or `POST`)
- `path: str` - Service path (`/nearest` or `/solve`)
- `query_params: dict[str, str | float]` - URL query parameters
- `json_body: dict | None` - JSON request body when required
- `headers: dict[str, str]` - Headers including `x-rapidapi-host` and `x-rapidapi-key`

**Validation Rules**:
- `method` MUST match the target operation contract
- `path` MUST be one of the supported service paths
- `json_body` MUST be `None` for `nearest`
- `json_body` MUST contain `{"stops": [[lon, lat], ...]}` for `solve`

### ServiceResponse
**Purpose**: Captures the normalized result of a remote call for rendering and exit-code classification.

**Attributes**:
- `status_code: int` - HTTP status code from the service, if available
- `payload: dict | list | None` - Parsed JSON content for success or structured error bodies
- `raw_text: str | None` - Raw response body for non-JSON responses
- `is_success: bool` - True when the response represents a successful command outcome
- `error_category: str | None` - One of `validation`, `configuration`, `transport`, `remote`, or `unexpected`

**Validation Rules**:
- Successful responses MUST prefer parsed JSON over raw text when JSON is available
- Non-JSON responses MUST preserve readable raw text for stderr output
- `error_category` MUST be set for every non-success outcome

## Entity Relationships

```text
ServiceConfig -> ServiceRequest
NearestQuery -> ServiceRequest
SolveQuery -> StopCoordinate
SolveQuery -> ServiceRequest
ServiceRequest -> ServiceResponse
```

## State Flow

1. CLI arguments are parsed into raw command values.
2. RapidAPI environment variables are resolved into a `ServiceConfig` with the fixed base URL.
3. Command inputs are validated into either `NearestQuery` or `SolveQuery`.
4. A normalized `ServiceRequest` is assembled from config plus command entity.
5. The HTTP client executes the request and converts the result into a `ServiceResponse`.
6. The CLI renders pretty JSON or readable error output and returns the mapped exit code.

## Data Validation Strategy

**Configuration Level**: Verify presence of `x_rapidapi_host` and `x_rapidapi_key` before command execution while keeping the base URL fixed.  
**Command Level**: Validate coordinate ranges, positive numeric inputs, and minimum stop count before network I/O.  
**Serialization Level**: Ensure `solve` request bodies preserve stop order as `[[lon, lat], ...]`.  
**Response Level**: Parse JSON when possible and gracefully fall back to response text when parsing fails.

## Error Handling

**Configuration Errors**: Missing or invalid RapidAPI header values prevent request execution and return a user-facing stderr message.  
**Input Errors**: Invalid coordinates, negative distance/speed, or fewer than two stops return a validation error before HTTP execution.  
**Transport Errors**: Connection failures, timeouts, or DNS issues are classified as transport failures and surfaced clearly.  
**Remote Errors**: Non-success HTTP responses surface status plus any structured JSON error body or raw response text.  
**Unexpected Errors**: Unhandled exceptions are trapped at the entry-point layer and returned as system-level failures.
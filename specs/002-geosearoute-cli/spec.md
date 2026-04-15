# Feature Specification: Sea Route Service Tester CLI

**Feature Branch**: `002-geosearoute-cli`  
**Created**: 2026-04-15  
**Status**: Draft  
**Input**: User description: "We want to create a simple python based cli app testing our geosearoute service API. Build a Python CLI tool called \"geosearoute-cli\" that tests the service. It must support two commands: \"nearest\" (GET /nearest?lat=&lon=&distance=, default distance 500 km) and \"solve\" (POST /solve?speed=, default speed 24 knots, JSON body {\"stops\":[[lon,lat],...]}). Pretty-print JSON responses. Handle errors and missing key. Use argparse, requests, standard libs only. Provide --help."

## Clarifications

### Session 2026-04-15

- Q: What should the CLI entry point and aligned feature branch name be? → A: Use `geosearoute-cli` as the command-line entry point and align the feature branch name with it.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Find Nearby Sea Route Access (Priority: P1)

A service operator needs to query the nearest sea-route point for a latitude and longitude so they can quickly verify that the service is reachable and returning plausible geographic results.

**Why this priority**: This is the fastest and most common service smoke test. It confirms connectivity, request formatting, and readable output with minimal input.

**Independent Test**: Can be fully tested by running the nearest command with valid coordinates and confirming that the tool sends the request, applies the default search distance when none is provided, and prints the returned result in a readable format.

**Acceptance Scenarios**:

1. **Given** a valid service endpoint and valid coordinates, **When** the user runs the nearest command without an explicit distance, **Then** the tool sends the request with the default search distance and displays the response as formatted JSON
2. **Given** a valid service endpoint, valid coordinates, and a custom distance, **When** the user runs the nearest command, **Then** the tool sends the provided distance value and displays the returned result without requiring any extra formatting steps from the user
3. **Given** a service error or unreachable service, **When** the user runs the nearest command, **Then** the tool exits cleanly with a clear error message describing the failure

---

### User Story 2 - Solve a Multi-Stop Route (Priority: P2)

A service operator needs to submit an ordered list of stops and receive a solved sea route so they can validate route generation behavior against real scenarios.

**Why this priority**: This validates the main planning capability of the service and exercises both structured request payloads and returned route data.

**Independent Test**: Can be fully tested by running the solve command with a valid list of two or more stops and confirming that the tool submits the stops in order, uses the default speed when none is provided, and prints the solved route as formatted JSON.

**Acceptance Scenarios**:

1. **Given** a valid service endpoint and a valid ordered stop list, **When** the user runs the solve command without an explicit speed, **Then** the tool submits the stop list using the default vessel speed and displays the solved route as formatted JSON
2. **Given** a valid service endpoint, valid ordered stops, and a custom speed, **When** the user runs the solve command, **Then** the tool sends the provided speed value and preserves stop order in the request
3. **Given** malformed stop input, **When** the user runs the solve command, **Then** the tool rejects the request locally and shows the user how to provide stops correctly

---

### User Story 3 - Recover From Configuration and Input Failures (Priority: P3)

A service operator needs immediate, actionable feedback when required credentials, required arguments, or request inputs are missing so they can correct the issue without inspecting source code.

**Why this priority**: A tester is only useful if failures are diagnosable. Clear guidance reduces wasted time during manual API checks.

**Independent Test**: Can be fully tested by invoking commands without the required service key, with missing required arguments, and with invalid values to confirm that the tool fails predictably and explains how to recover.

**Acceptance Scenarios**:

1. **Given** the required service key is not available, **When** the user runs any command, **Then** the tool stops before making the request and explains that the key is missing
2. **Given** required command arguments are omitted, **When** the user requests help or runs an incomplete command, **Then** the tool shows command usage guidance for the relevant operation
3. **Given** the service returns a non-success response with structured error details, **When** the user runs a command, **Then** the tool surfaces the error details in a readable form and exits with a non-zero status

### Edge Cases

- How does the tool behave when latitude or longitude values are outside valid geographic ranges?
- What happens when the nearest command receives a zero or negative distance value?
- What happens when the solve command receives fewer than two stops or a stop that does not contain exactly one longitude and one latitude?
- How does the tool present responses that are valid but do not contain the expected result fields?
- How does the tool behave when the service returns non-JSON content for an error response?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a command-line entry point named `geosearoute-cli`
- **FR-002**: System MUST provide a `nearest` command that accepts latitude and longitude as required inputs
- **FR-003**: System MUST allow the `nearest` command to accept an optional search distance and MUST use a default value of 500 kilometers when no distance is provided
- **FR-004**: System MUST send the `nearest` request to the sea-route service as a nearest-point lookup using the supplied coordinates and distance
- **FR-005**: System MUST provide a `solve` command that accepts an ordered list of route stops, where each stop is defined by longitude and latitude
- **FR-006**: System MUST require at least two stops for the `solve` command so a route can be evaluated
- **FR-007**: System MUST allow the `solve` command to accept an optional vessel speed and MUST use a default value of 24 knots when no speed is provided
- **FR-008**: System MUST send the `solve` request to the sea-route service as a route-solving operation using the supplied ordered stops and speed
- **FR-009**: System MUST display successful service responses as human-readable formatted JSON
- **FR-010**: System MUST provide command-specific help output and top-level help output describing available commands, required inputs, and optional inputs
- **FR-011**: System MUST detect when the required service key is missing and present an actionable error before attempting the request
- **FR-012**: System MUST validate command inputs before sending a request and MUST reject malformed coordinates, malformed stop lists, and invalid numeric values with clear error messages
- **FR-013**: System MUST present service-side errors and transport failures in a readable form that helps the user distinguish configuration issues, request issues, and service availability issues
- **FR-014**: System MUST return a success exit status for successful requests and a non-success exit status for validation failures, missing configuration, or service/request failures

### Key Entities *(include if feature involves data)*

- **Nearest Query**: A lookup request containing a latitude, longitude, and optional search radius used to find the closest sea-route point
- **Route Solve Request**: A route-solving request containing an ordered collection of stops and an optional vessel speed
- **Stop Coordinate**: A single route waypoint represented by one longitude and one latitude, where order matters for the solved route
- **Service Credential**: The required access key or token needed to authorize requests to the sea-route service
- **Service Response**: The structured success or error payload returned by the sea-route service and displayed to the user

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A user can complete a nearest-point test from the command line in under 30 seconds after supplying coordinates and service access details
- **SC-002**: A user can complete a multi-stop solve test with at least two stops in under 60 seconds after supplying stops and service access details
- **SC-003**: 100% of successful service calls are displayed as readable formatted JSON without requiring manual reformatting
- **SC-004**: 100% of missing-credential, invalid-input, and service-error cases result in a non-success exit and an actionable error message
- **SC-005**: A first-time user can discover the available commands and required inputs using built-in help alone, without consulting external documentation

## Assumptions

- The sea-route service exposes separate nearest-point and route-solving operations that remain available to the CLI during testing
- Users running the tool have valid service access details and know the service base location they need to test
- The required service key is supplied through a standard configuration mechanism available at runtime
- A route solve request is meaningful only when at least two ordered stops are provided
- Formatted JSON output is the preferred default for both success and error payloads when the service returns structured data

## Scope Boundaries

**In Scope:**
- Manual command-line testing of the sea-route service
- Nearest-point lookups with a default and user-specified search distance
- Route-solving requests with ordered stops and a default or user-specified speed
- Built-in help, input validation, readable output, and actionable error handling
- Detection of missing service credentials before request submission

**Out of Scope:**
- Automated load testing, benchmarking, or continuous monitoring
- Interactive prompts, graphical interfaces, or browser-based tooling
- Editing, storing, or managing route data outside a single command invocation
- Retry policies, offline queuing, or advanced recovery workflows
- Support for additional service operations beyond nearest-point lookup and route solving

# Implementation Plan: Sea Route Service Tester CLI

**Branch**: `002-geosearoute-cli` | **Date**: 2026-04-15 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/002-geosearoute-cli/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

Build a dedicated Python CLI package for manual testing of the geosearoute service, following the existing haversine exploration structure while keeping runtime dependencies minimal. The tool will expose `nearest` and `solve` subcommands, use `requests` as the only non-stdlib dependency for service calls, pretty-print JSON responses, validate inputs locally before network I/O, and support configuration through environment defaults with command-line overrides.

## Technical Context

**Language/Version**: Python 3.8+  
**Primary Dependencies**: `requests` plus Python standard library (`argparse`, `json`, `os`, `sys`, `unittest`, `unittest.mock`)  
**Storage**: N/A (stateless CLI tool)  
**Testing**: Python `unittest` with `unittest.mock` for HTTP isolation  
**Target Platform**: Cross-platform command-line execution on Linux, macOS, and Windows via Python interpreter  
**Project Type**: CLI application in a dedicated root package directory  
**Performance Goals**: Local argument validation and response formatting complete in under 100 ms excluding network latency; CLI overhead beyond the HTTP request remains under 250 ms for typical payloads  
**Constraints**: Minimal runtime dependencies, only `requests` beyond stdlib; dedicated application directory; no persistence; pretty-printed JSON by default; clear non-zero exits for validation, configuration, and remote failures  
**Scale/Scope**: Single-user manual tester with two commands and small request payloads, including nearest lookups and solve requests with 2-50 ordered stops

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### I. Code Quality Excellence (Deep Code) ✅
- **Compliance**: The feature keeps CLI orchestration, request construction, validation, and response formatting in separate modules within a dedicated package.
- **Evidence**: The design follows the haversine exploration pattern of a thin `__main__` entry point delegating to testable modules.
- **Deep Code Connection**: Even though this tool calls an external API, the implementation keeps request/response behavior explicit rather than hiding it behind a framework.

### II. Test-First Development (NON-NEGOTIABLE) ✅
- **Compliance**: The plan uses `unittest` and `unittest.mock` for parser behavior, validation rules, HTTP client behavior, and command integration.
- **Evidence**: Each planned module has a corresponding test module and mock-based tests for success, error, and malformed-response paths.
- **Documentation Value**: Tests document correct command syntax, configuration precedence, and error outcomes.

### III. User Experience Consistency ✅
- **Compliance**: The new CLI mirrors the repository's existing package entry-point pattern and standard UNIX-style help/error behavior.
- **Evidence**: `geosearoute-cli` will support top-level help, command-specific help, predictable exit codes, and actionable stderr messages.
- **Consistency**: The design reuses the haversine separation between `__main__`, `cli`, validation, and domain modules.

### IV. Performance Standards & Observable Behavior ✅
- **Compliance**: Local validation and formatting goals are explicit, and failures are classified with readable output and exit codes.
- **Evidence**: The contract defines pretty-printed JSON for success and structured error reporting for missing configuration, transport issues, and service errors.
- **Observable Behavior**: Every command produces deterministic stdout/stderr behavior and measurable local overhead.

### V. Foundational Infrastructure Alignment ✅
- **Compliance**: Configuration is externalized through environment variables with optional CLI overrides, and package wiring remains in `pyproject.toml`.
- **Evidence**: No environment-specific values are hardcoded into source code; the package remains installable and runnable through standard Python tooling.
- **Infrastructure**: The feature extends the repo's packaging and documentation structure rather than introducing ad hoc scripts.

**GATE RESULT**: ✅ ALL PRINCIPLES SATISFIED - Proceed to research phase

## Phase 0: Research Complete ✅

**Output**: [research.md](research.md)
- ✅ Dedicated package layout chosen based on the existing haversine exploration
- ✅ Minimal dependency strategy confirmed: `requests` only for runtime HTTP calls
- ✅ Configuration precedence resolved: environment defaults with command-line overrides
- ✅ Solve command input shape resolved for ordered multi-stop requests
- ✅ Test strategy confirmed using `unittest` and mock-based HTTP isolation

## Phase 1: Design & Contracts Complete ✅

**Outputs**:
- ✅ [data-model.md](data-model.md) - Configuration, request, stop, and response entities
- ✅ [contracts/cli-interface.md](contracts/cli-interface.md) - Complete CLI contract with configuration precedence and examples
- ✅ [quickstart.md](quickstart.md) - Setup and usage documentation
- ✅ Agent context updated (GitHub Copilot)

### Post-Design Constitution Check ✅

#### I. Code Quality Excellence (Deep Code) ✅ ENHANCED
- **Design Evidence**: The model separates CLI parsing, environment/config resolution, request serialization, response handling, and validation.
- **Educational Structure**: The quickstart and contract make the API interaction visible instead of hiding it behind opaque tooling.
- **Reference Quality**: The dedicated package layout mirrors the existing exploration and remains easy to inspect and extend.

#### II. Test-First Development (NON-NEGOTIABLE) ✅ ENHANCED
- **Test Strategy**: The design supports isolated tests for argument parsing, precedence rules, HTTP request composition, pretty-printing, and error classification.
- **Known Behaviors**: Contract examples give testable fixtures for both commands and common failure cases.
- **Documentation**: Tests double as executable examples for manual service testing workflows.

#### III. User Experience Consistency ✅ ENHANCED
- **CLI Contract**: Command signatures, repeated stop syntax, config precedence, and exit code rules are now explicit.
- **Execution Methods**: The design supports both the installed script and `python -m geosearoute_cli` execution.
- **Error Handling**: Missing credentials, malformed coordinates, malformed stops, and remote errors all have defined outcomes.

#### IV. Performance Standards & Observable Behavior ✅ ENHANCED
- **Measurable Goals**: Local validation and formatting budgets are documented independently from network latency.
- **Error Reporting**: Error paths are classified into local validation/configuration versus remote/transport failures.
- **Exit Codes**: Standardized success and failure behavior remains aligned with the existing CLI exploration.

#### V. Foundational Infrastructure Alignment ✅ ENHANCED
- **Environment Separation**: Base URL and API key remain externalized and can be overridden without code changes.
- **Configuration**: `pyproject.toml` remains the single place for packaging and console-script registration.
- **Portability**: A dedicated package directory preserves clean package discovery and cross-platform execution.

**FINAL GATE RESULT**: ✅ ALL CONSTITUTIONAL PRINCIPLES SATISFIED WITH DESIGN ENHANCEMENT

## Ready for Implementation

The plan is complete with all design artifacts generated. The feature stays aligned with the Germaneering constitution, reuses the repository's proven CLI layout, and constrains complexity to a small dedicated package with one external runtime dependency.

## Project Structure

### Documentation (this feature)

```text
specs/002-geosearoute-cli/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── cli-interface.md
└── tasks.md
```

### Source Code (repository root)

```text
geosearoute_cli/
├── __init__.py          # Package metadata
├── __main__.py          # Entry point for `python -m geosearoute_cli`
├── cli.py               # Argument parsing and command dispatch
├── client.py            # HTTP request execution against geosearoute service
├── models.py            # Typed request/config/response data structures
└── validator.py         # Input and configuration validation

tests/
├── test_cli.py          # CLI parsing and command execution behavior
├── test_client.py       # HTTP request composition and remote error handling
├── test_models.py       # Data structure defaults and normalization
└── test_validator.py    # Coordinate, stop, and configuration validation

pyproject.toml           # Packaging, dependency, and console script configuration
README.md                # Repository-level exploration overview and usage summary
```

**Structure Decision**: Use a single dedicated root package named `geosearoute_cli` to mirror the proven haversine exploration layout while accommodating the hyphenated console script name `geosearoute-cli`. This keeps the application self-contained, testable, and easy to package without modifying the existing haversine package structure.

## Complexity Tracking

No constitutional violations or design exceptions require justification.
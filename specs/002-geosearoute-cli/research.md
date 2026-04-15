# Research: Sea Route Service Tester CLI

**Feature**: `002-geosearoute-cli`  
**Date**: 2026-04-15  
**Status**: Complete

## Key Technical Decisions

### Decision: Use a dedicated root package named `geosearoute_cli`
**Rationale**: The repository already demonstrates a working Python CLI pattern through the root-level `haversine/` package. A sibling `geosearoute_cli/` package preserves that structure, keeps the new app isolated in its own directory, and supports both `python -m geosearoute_cli` and a hyphenated console-script entry point.

**Alternatives considered**:
- Extending the existing `haversine/` package (rejected: mixes unrelated responsibilities and violates the dedicated-directory requirement)
- Using a flat single-file script (rejected: harder to test, package, and keep consistent with the existing exploration)
- Naming the package `geosearoute/` (rejected: less explicit than `geosearoute_cli` when paired with the `geosearoute-cli` command name)

### Decision: Limit runtime dependencies to `requests` plus Python standard library
**Rationale**: The feature needs a reliable HTTP client, but the user explicitly wants minimal Python dependencies. `requests` is sufficient for GET and POST interactions, timeouts, JSON submission, and readable error handling without introducing a framework.

**Alternatives considered**:
- `urllib.request` only (rejected: possible, but leads to more verbose error handling and request body composition for a tool whose primary job is HTTP interaction)
- `httpx` (rejected: unnecessary extra capability for a synchronous CLI tester)
- A full CLI framework such as `click` or `typer` (rejected: unnecessary dependency overhead since `argparse` already satisfies the requirements)

### Decision: Resolve configuration through environment variables with command-line overrides
**Rationale**: Manual testers need a convenient default workflow for repeated calls, but they also need the ability to target a different environment or temporarily override credentials during debugging. Environment defaults keep secrets out of routine command history, while command flags preserve operational flexibility.

**Chosen configuration contract**:
- `GEOSEAROUTE_BASE_URL` provides the default service base URL
- `GEOSEAROUTE_API_KEY` provides the default API key
- `--base-url` overrides the environment default
- `--api-key` overrides the environment default

**Alternatives considered**:
- Environment variables only (rejected: makes one-off environment switching cumbersome)
- Command-line options only (rejected: increases secret exposure in shell history and repeated command friction)
- Hardcoded base URL with environment-only key (rejected: reduces portability across service environments)

### Decision: Represent solve stops as repeated `--stop <lon> <lat>` arguments
**Rationale**: The API request body is JSON, but the CLI should remain human-friendly for manual testing. Repeated `--stop` options preserve order, map cleanly to `argparse`, and avoid forcing users to hand-author JSON in the shell.

**Alternatives considered**:
- Raw JSON string input for the stops body (rejected: poor ergonomics for interactive use)
- Positional alternating longitude/latitude values (rejected: error-prone and less self-documenting for multi-stop routes)
- Reading stops from a file (rejected: out of scope for a minimal manual tester)

### Decision: Reuse the repository's `unittest` testing approach with mocked HTTP calls
**Rationale**: The existing haversine exploration already uses `unittest`, and the constitution requires test-first development. `unittest.mock` is enough to simulate service responses, transport errors, and malformed payloads while keeping test dependencies at zero.

**Alternatives considered**:
- `pytest` (rejected: extra dependency with no clear benefit for this small CLI)
- Live integration tests against the real service (rejected: too fragile and environment-dependent as the primary test strategy)
- No client-level mocks (rejected: would make tests slow, flaky, and dependent on credentials)

## Integration Notes

### Existing repo pattern to preserve
- `__main__.py` should remain a thin wrapper around `cli.main()`
- Console script registration should live in `pyproject.toml`
- Tests should remain module-oriented under `tests/`
- README updates should add the new exploration alongside haversine rather than redefining the repo structure

### API interaction approach
- `nearest` sends a GET request with `lat`, `lon`, and `distance` query parameters
- `solve` sends a POST request with `speed` as a query parameter and a JSON body shaped as `{"stops": [[lon, lat], ...]}`
- Both commands pretty-print any successful JSON response exactly as returned by the service
- Non-JSON error responses are surfaced as readable stderr text with status information

## Research Validation

✅ Dedicated package layout matches the existing CLI exploration pattern  
✅ Runtime dependency count stays minimal with `requests` only  
✅ Configuration precedence is explicit and implementation-ready  
✅ Solve input format is human-friendly and maps cleanly to the required JSON payload  
✅ Test strategy is isolated, deterministic, and constitution-compliant

**Ready for Phase 1**: Design and contracts definition
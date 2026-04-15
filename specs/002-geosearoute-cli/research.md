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

### Decision: Fix the service base URL and source RapidAPI headers from lowercase environment variables
**Rationale**: The integration target is known in advance as `https://geosearoute.p.rapidapi.com`, so the CLI does not need runtime base URL selection. RapidAPI requires the `x-rapidapi-host` and `x-rapidapi-key` headers, and sourcing those values from lowercase environment variables keeps secrets and deployment-specific metadata out of command history while matching the requested operational model.

**Chosen configuration contract**:
- Base URL is fixed to `https://geosearoute.p.rapidapi.com`
- `x_rapidapi_host` provides the value for the `x-rapidapi-host` header
- `x_rapidapi_key` provides the value for the `x-rapidapi-key` header
- Missing either environment variable prevents any outbound request

**Alternatives considered**:
- Environment variable for the base URL as well (rejected: unnecessary indirection for a fixed integration target)
- Command-line flags for host and key (rejected: increases secret exposure in shell history)
- Hardcoded header values (rejected: breaks portability across accounts or RapidAPI configurations)

### Decision: Use `uv` as the preferred execution, packaging, and deployment workflow
**Rationale**: The user explicitly prefers `uv` so the CLI can be built, run, and deployed consistently. A `uv`-first workflow aligns with the repository's packaging direction and keeps installation, testing, and execution behavior predictable.

**Preferred workflow**:
- `uv sync` for environment preparation
- `uv run geosearoute-cli ...` for command execution
- `uv run python -m unittest ...` for tests
- `uv build` for distributable artifacts

**Alternatives considered**:
- `pip install -e .` as the primary workflow (rejected: still possible, but not the preferred path)
- Direct system Python invocation only (rejected: less consistent for packaging and deployment)

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
- `uv` should be the documented primary way to run, test, and build the tool

### API interaction approach
- Base URL is fixed to `https://geosearoute.p.rapidapi.com`
- `nearest` sends a GET request with `lat`, `lon`, and `distance` query parameters
- `solve` sends a POST request with `speed` as a query parameter and a JSON body shaped as `{"stops": [[lon, lat], ...]}`
- Every request includes `x-rapidapi-host` and `x-rapidapi-key` headers using values from `x_rapidapi_host` and `x_rapidapi_key`
- Both commands pretty-print any successful JSON response exactly as returned by the service
- Non-JSON error responses are surfaced as readable stderr text with status information

## Research Validation

✅ Dedicated package layout matches the existing CLI exploration pattern  
✅ Runtime dependency count stays minimal with `requests` only  
✅ RapidAPI header sourcing and fixed endpoint configuration are explicit and implementation-ready  
✅ Solve input format is human-friendly and maps cleanly to the required JSON payload  
✅ `uv`-first test and packaging workflow is aligned with the requested deployment model  
✅ Test strategy is isolated, deterministic, and constitution-compliant

**Ready for Phase 1**: Design and contracts definition
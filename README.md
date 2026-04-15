# Germaneering Lab

This repository contains runnable examples, patterns, and specifications that accompany the [Germaneering doctrine](https://germaneering.org) - a framework for building stable, observable, and aligned software systems in the age of autonomous systems.

The doctrine organizes the structural responsibilities of modern engineering into four interconnected dimensions. Each dimension addresses a different aspect of building systems that remain reliable as complexity increases.

Together, these dimensions provide a framework for understanding how engineering practice evolves in the presence of autonomous and generative technologies.

| Pillar           | Primary Form               | Essence                                                                   |
| ---------------- | -------------------------- | ------------------------------------------------------------------------- |
| **Deep Code**	   | Source code                | Implementation with awareness beneath the abstraction.                    |
| **Foundational** | Infrastructure as code     | The durable substrate (config, environments, scripts) that outlives apps. |
| **Intent Code**  | Declarative specifications | Machine‑readable objectives, constraints, and policies.                   |
| **Void Coding**  | Prototypes, sketches       | Exploration where patterns do not yet exist.                              |

## Explorations

### Haversine CLI Calculator (`haversine/`)

A minimal command-line tool demonstrating **Deep Code** principles by calculating great-circle distances using only Python standard library modules. This exploration exemplifies the Germaneering doctrine's emphasis on understanding implementations "beneath the abstraction."

**Quick Start:**
```bash
# Install and run with uv (recommended)
uv run haversine 40.7128 -74.0060 34.0522 -118.2437

# Or run directly with Python  
python -m haversine 40.7128 -74.0060 34.0522 -118.2437
```

**Deep Code Educational Examples:**

*Basic Distance Calculation:*
```bash
# New York to Los Angeles  
uv run haversine 40.7128 -74.0060 34.0522 -118.2437
# Output: 3935.75 km

# London to Paris
uv run haversine 51.5074 -0.1278 48.8566 2.3522  
# Output: 344.73 km

# Equator crossing  
uv run haversine 0 0 0 180
# Output: 20003.93 km (half Earth's circumference)
```

*Multiple Unit Systems (demonstrates measurement standards):*
```bash
# Statute miles (US/UK standard)
uv run haversine 40.7128 -74.0060 34.0522 -118.2437 --unit miles
# Output: 2445.56 miles

# Nautical miles (aviation/marine standard) 
uv run haversine 40.7128 -74.0060 34.0522 -118.2437 --unit nautical
# Output: 2125.13 nautical miles

# High precision for scientific applications
uv run haversine 40.7128 -74.0060 34.0522 -118.2437 --precision 6
# Output: 3935.746297 km
```

*Educational Error Handling:*
```bash
# Invalid coordinates demonstrate geographic constraints
uv run haversine 95 0 0 0
# Provides educational explanation of latitude/longitude limits

# Helpful usage examples on errors
uv run haversine abc def  
# Shows coordinate format requirements with real-world examples
```

**Deep Code Demonstration:**
- **Mathematical Primitives**: Haversine formula implementation using `math.sin()`, `math.cos()`, `math.radians()` - no black-box libraries
- **Zero Dependencies**: Only Python standard library (`math`, `sys`, `argparse`, `unittest`) - complete educational transparency  
- **Explicit Algorithms**: Visible great-circle distance calculation showing Earth's spherical geometry
- **Test-First Development**: Comprehensive test coverage demonstrating validation approaches for mathematical software

**Germaneering Doctrine Connection:**

This tool embodies the "awareness beneath the abstraction" principle by:

1. **Exposition Over Abstraction**: The mathematical formula is completely visible and commented, not hidden in a library
2. **Educational Transparency**: Error messages teach geographic coordinate systems rather than just reporting failures  
3. **Primitive Building Blocks**: Built from mathematical operators, not imported calculation packages
4. **Verifiable Behavior**: Every calculation step can be traced and validated manually

**Architecture & Design:**

```
haversine/
├── __init__.py          # Package initialization with version
├── models.py            # GeographicPoint coordinate validation  
├── calculator.py        # Haversine formula implementation
├── validator.py         # Input validation with geographic constraints
├── cli.py              # Command-line interface with educational errors
└── __main__.py         # Entry point for both 'uv run' and 'python -m'

tests/
├── test_models.py      # Coordinate validation edge cases
├── test_calculator.py  # Mathematical accuracy verification  
├── test_validator.py   # Input validation comprehensive coverage
└── test_cli.py        # CLI integration and error handling
```

**Features by User Story:**
1. **Basic Calculation**: Four coordinate arguments → distance in kilometers
2. **Enhanced Validation**: Geographic constraints with educational error messages  
3. **Output Formatting**: Multiple units (km/miles/nautical) with precision control (0-6 decimals)

See [haversine specification](specs/001-haversine-cli/spec.md) and [quickstart guide](specs/001-haversine-cli/quickstart.md) for complete documentation.

### GeoSeaRoute Service Tester (`geosearoute_cli/`)

A focused command-line tester for the geosearoute RapidAPI service. This exploration demonstrates a different aspect of Germaneering: a small, explicit client that keeps request construction, validation, configuration, and error handling visible instead of delegating them to a heavy framework.

**Quick Start:**
```bash
# Prepare the environment
uv sync

# Configure the RapidAPI headers used by every request
export x_rapidapi_host="geosearoute.p.rapidapi.com"
export x_rapidapi_key="your-rapidapi-key"

# Run the nearest lookup
uv run geosearoute-cli nearest 57.7089 11.9746
```

**Command Examples:**
```bash
# Default nearest lookup (distance defaults to 500 km)
uv run geosearoute-cli nearest 57.7089 11.9746

# Custom nearest lookup distance
uv run geosearoute-cli nearest 57.7089 11.9746 --distance 750

# Solve a route with the default 24-knot speed
uv run geosearoute-cli solve \
	--stop 11.9746 57.7089 \
	--stop 4.47917 51.9225

# Solve a route with additional stops and custom speed
uv run geosearoute-cli solve \
	--stop 11.9746 57.7089 \
	--stop 4.47917 51.9225 \
	--stop -5.9301 54.5973 \
	--speed 20
```

**What This Exploration Demonstrates:**
- **Minimal Dependencies**: Only `requests` beyond the Python standard library
- **Explicit Integration Boundaries**: Fixed RapidAPI endpoint with visible `x-rapidapi-host` and `x-rapidapi-key` header construction
- **Test-First Service Client Design**: Mocked HTTP tests for success paths, remote failures, transport failures, and malformed input
- **Foundational Workflow Alignment**: `uv sync`, `uv run`, and `uv build` as the primary setup, execution, and packaging path

**Architecture & Design:**

```text
geosearoute_cli/
├── __init__.py         # Package metadata and exports
├── __main__.py         # Entry point for script and module execution
├── cli.py              # argparse subcommands, output, and exit handling
├── client.py           # Fixed-endpoint RapidAPI request execution
├── models.py           # Immutable request and response models
└── validator.py        # Configuration and input validation helpers

tests/
├── test_cli.py         # Geosearoute and haversine CLI behavior
├── test_client.py      # RapidAPI request and response normalization
├── test_models.py      # Shared geosearoute model validation
└── test_validator.py   # Shared validation and environment handling
```

**Features by User Story:**
1. **Nearest Lookup**: Validate GET `/nearest` requests with default and custom distance values
2. **Solve Route**: Validate POST `/solve` requests with ordered stops and optional speed
3. **Operational Error Recovery**: Fail early on missing RapidAPI variables, malformed inputs, and service-side errors

See [geosearoute specification](specs/002-geosearoute-cli/spec.md), [quickstart guide](specs/002-geosearoute-cli/quickstart.md), and [task list](specs/002-geosearoute-cli/tasks.md) for the full implementation details.

### Future Explorations

Each subdirectory will correspond to essays on the website, with code that demonstrates the concepts in practice.

## License

Code is licensed under the Apache V2 License. See [LICENSE](./LICENSE). The associated essays remain on the Germaneering website and are not part of this repository.

## Contributing

We welcome contributions! If you have an example that illustrates Germaneering principles, please open an issue or pull request.

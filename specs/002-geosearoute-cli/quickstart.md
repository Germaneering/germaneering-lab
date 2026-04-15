# Quickstart: Sea Route Service Tester CLI

This guide shows the intended developer workflow for the `geosearoute-cli` exploration.

## Prerequisites

- Python 3.8+
- A reachable geosearoute service environment
- A valid service API key

## Installation

Install the package in editable mode from the repository root:

```bash
pip install -e .
```

## Configure Service Access

Set environment defaults for repeated manual testing:

```bash
export GEOSEAROUTE_BASE_URL="https://your-geosearoute-service.example.com"
export GEOSEAROUTE_API_KEY="your-api-key"
```

These values can be overridden per command using `--base-url` and `--api-key`.

## Inspect Available Commands

```bash
geosearoute-cli --help
geosearoute-cli nearest --help
geosearoute-cli solve --help
```

You can also run the package as a module:

```bash
python -m geosearoute_cli --help
```

## Run a Nearest Lookup

Use the default distance:

```bash
geosearoute-cli nearest 57.7089 11.9746
```

Use a custom search distance:

```bash
geosearoute-cli nearest 57.7089 11.9746 --distance 750
```

Override the target service for one command:

```bash
geosearoute-cli nearest 57.7089 11.9746 \
  --base-url https://staging.example.com \
  --api-key staging-key
```

## Run a Solve Request

Submit the minimum two ordered stops:

```bash
geosearoute-cli solve \
  --stop 11.9746 57.7089 \
  --stop 4.47917 51.9225
```

Submit additional stops with a custom speed:

```bash
geosearoute-cli solve \
  --stop 11.9746 57.7089 \
  --stop 4.47917 51.9225 \
  --stop -5.9301 54.5973 \
  --speed 20
```

## Expected Behavior

- Successful responses print pretty JSON to stdout
- Missing configuration fails before any network request
- Invalid coordinates, negative distance/speed values, and insufficient stops fail with actionable stderr messages
- Remote service errors preserve HTTP status information and any returned JSON error body

## Test Strategy

Planned implementation validation:

```bash
python -m unittest discover -s tests -p 'test_*.py'
```

Focus areas:

- top-level and command-specific help behavior
- nearest and solve request serialization
- configuration precedence between environment and CLI overrides
- pretty-printed success output
- remote error and transport failure handling
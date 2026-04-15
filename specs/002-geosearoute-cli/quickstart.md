# Quickstart: Sea Route Service Tester CLI

This guide shows the intended developer workflow for the `geosearoute-cli` exploration.

## Prerequisites

- Python 3.8+
- `uv`
- A valid RapidAPI subscription and key for the geosearoute service

## Installation

Prepare the environment from the repository root with `uv`:

```bash
uv sync
```

## Configure Service Access

Set the RapidAPI header values used by every request:

```bash
export x_rapidapi_host="geosearoute.p.rapidapi.com"
export x_rapidapi_key="your-rapidapi-key"
```

The CLI always targets `https://geosearoute.p.rapidapi.com` and uses these environment variables to populate the required RapidAPI headers.

## Inspect Available Commands

```bash
uv run geosearoute-cli --help
uv run geosearoute-cli nearest --help
uv run geosearoute-cli solve --help
```

You can also run the package as a module:

```bash
uv run python -m geosearoute_cli --help
```

## Run a Nearest Lookup

Use the default distance:

```bash
uv run geosearoute-cli nearest 57.7089 11.9746
```

Use a custom search distance:

```bash
uv run geosearoute-cli nearest 57.7089 11.9746 --distance 750
```

## Run a Solve Request

Submit the minimum two ordered stops:

```bash
uv run geosearoute-cli solve \
  --stop 11.9746 57.7089 \
  --stop 4.47917 51.9225
```

Submit additional stops with a custom speed:

```bash
uv run geosearoute-cli solve \
  --stop 11.9746 57.7089 \
  --stop 4.47917 51.9225 \
  --stop -5.9301 54.5973 \
  --speed 20
```

## Build the Package

Create distributable artifacts with:

```bash
uv build
```

## Expected Behavior

- Successful responses print pretty JSON to stdout
- Missing configuration fails before any network request
- Invalid coordinates, negative distance and speed values, and insufficient stops fail with actionable stderr messages
- Remote service errors preserve HTTP status information and any returned JSON error body
- Every request sends `x-rapidapi-host` and `x-rapidapi-key` using the lowercase environment variables above

## Test Strategy

Planned implementation validation:

```bash
uv run python -m unittest discover -s tests -p 'test_*.py'
```

Focus areas:

- top-level and command-specific help behavior
- nearest and solve request serialization
- required RapidAPI environment variable handling
- pretty-printed success output
- remote error and transport failure handling
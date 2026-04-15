"""Command-line interface for geosearoute-cli."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Sequence

from .client import GeoSeaRouteClient
from .models import NearestQuery, ServiceResponse, SolveQuery
from .validator import (
    ConfigurationError,
    ValidationError,
    parse_stop_pairs,
    resolve_service_config,
    validate_latitude,
    validate_longitude,
    validate_positive_number,
)


def create_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="geosearoute-cli",
        description="Manual tester for geosearoute service endpoints.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  uv run geosearoute-cli nearest 57.7089 11.9746\n"
            "  uv run geosearoute-cli solve --stop 11.9746 57.7089 --stop 4.47917 51.9225"
        ),
    )
    subparsers = parser.add_subparsers(dest="command")
    subparsers.required = True

    nearest_parser = subparsers.add_parser("nearest", help="Test GET /nearest")
    nearest_parser.add_argument("lat", type=float, help="Latitude in decimal degrees [-90, 90]")
    nearest_parser.add_argument("lon", type=float, help="Longitude in decimal degrees [-180, 180]")
    nearest_parser.add_argument(
        "--distance",
        type=float,
        default=500.0,
        help="Search distance in kilometers (default: 500.0)",
    )

    solve_parser = subparsers.add_parser("solve", help="Test POST /solve")
    solve_parser.add_argument(
        "--stop",
        nargs=2,
        action="append",
        required=True,
        metavar=("LON", "LAT"),
        help="Ordered route stop; repeat for each stop",
    )
    solve_parser.add_argument(
        "--speed",
        type=float,
        default=24.0,
        help="Vessel speed in knots (default: 24.0)",
    )

    return parser


def _pretty_json(payload) -> str:
    return json.dumps(payload, indent=2)


def _print_error(message: str) -> None:
    print(f"Error: {message}", file=sys.stderr)


def _render_service_error(response: ServiceResponse) -> None:
    if response.error_category == "transport":
        _print_error("Could not reach geosearoute service.")
        if response.raw_text:
            print(f"Reason: {response.raw_text}", file=sys.stderr)
        return

    status = response.status_code if response.status_code is not None else "unknown"
    _print_error(f"Service request failed with HTTP {status}.")
    if response.payload is not None:
        print(_pretty_json(response.payload), file=sys.stderr)
    elif response.raw_text:
        print(response.raw_text, file=sys.stderr)


def _build_nearest_query(parsed_args: argparse.Namespace) -> NearestQuery:
    return NearestQuery(
        latitude=validate_latitude(parsed_args.lat),
        longitude=validate_longitude(parsed_args.lon),
        distance_km=validate_positive_number("distance", parsed_args.distance),
    )


def _build_solve_query(parsed_args: argparse.Namespace) -> SolveQuery:
    stops = parse_stop_pairs(parsed_args.stop)
    return SolveQuery(
        stops=stops,
        speed_knots=validate_positive_number("speed", parsed_args.speed),
    )


def main(args: Sequence[str] | None = None) -> int:
    parser = create_argument_parser()
    try:
        parsed_args = parser.parse_args(args)
    except SystemExit as exc:
        return 0 if exc.code == 0 else 1

    try:
        config = resolve_service_config()
        client = GeoSeaRouteClient(config)
        if parsed_args.command == "nearest":
            response = client.nearest(_build_nearest_query(parsed_args))
        else:
            response = client.solve(_build_solve_query(parsed_args))
    except (ConfigurationError, ValidationError) as exc:
        _print_error(str(exc))
        return 1

    if response.is_success:
        if response.payload is not None:
            print(_pretty_json(response.payload))
        elif response.raw_text:
            print(response.raw_text)
        return 0

    _render_service_error(response)
    return 2

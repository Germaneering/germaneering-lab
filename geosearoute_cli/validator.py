"""Validation helpers for geosearoute-cli."""

from __future__ import annotations

import os
from typing import Iterable, Mapping, MutableSequence, Sequence, Tuple

from .models import FIXED_BASE_URL, ServiceConfig, StopCoordinate


class ValidationError(ValueError):
	"""Raised when CLI input fails validation."""


class ConfigurationError(ValidationError):
	"""Raised when required RapidAPI configuration is missing."""


def validate_latitude(value: float) -> float:
	number = float(value)
	if not -90.0 <= number <= 90.0:
		raise ValidationError(f"Latitude must be between -90 and 90. Got {value}.")
	return number


def validate_longitude(value: float) -> float:
	number = float(value)
	if not -180.0 <= number <= 180.0:
		raise ValidationError(f"Longitude must be between -180 and 180. Got {value}.")
	return number


def validate_positive_number(name: str, value: float) -> float:
	number = float(value)
	if number <= 0:
		raise ValidationError(f"{name} must be greater than 0. Got {value}.")
	return number


def resolve_service_config(environment: Mapping[str, str] | None = None) -> ServiceConfig:
	env = environment if environment is not None else os.environ
	missing = [name for name in ("x_rapidapi_host", "x_rapidapi_key") if not str(env.get(name, "")).strip()]
	if missing:
		message_lines = ["Missing RapidAPI environment configuration."]
		for name in missing:
			message_lines.append(f"Provide environment variable {name}.")
		raise ConfigurationError("\n".join(message_lines))
	return ServiceConfig(
		base_url=FIXED_BASE_URL,
		rapidapi_host=str(env["x_rapidapi_host"]).strip(),
		rapidapi_key=str(env["x_rapidapi_key"]).strip(),
	)


def parse_stop_pairs(raw_stops: Sequence[Sequence[str]]) -> Tuple[StopCoordinate, ...]:
	parsed_stops = []
	for index, stop in enumerate(raw_stops):
		if len(stop) != 2:
			raise ValidationError(f"Stop {index + 1} must contain exactly one longitude and one latitude.")
		longitude = validate_longitude(float(stop[0]))
		latitude = validate_latitude(float(stop[1]))
		parsed_stops.append(StopCoordinate(longitude=longitude, latitude=latitude, index=index))
	return tuple(parsed_stops)

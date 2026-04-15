"""Data models for geosearoute-cli."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple


FIXED_BASE_URL = "https://geosearoute.p.rapidapi.com"


def _require_non_blank(field_name: str, value: str) -> str:
	cleaned = value.strip() if isinstance(value, str) else ""
	if not cleaned:
		raise ValueError(f"{field_name} must not be blank")
	return cleaned


def _as_float(field_name: str, value: float) -> float:
	try:
		return float(value)
	except (TypeError, ValueError) as exc:
		raise ValueError(f"{field_name} must be numeric") from exc


def _validate_range(field_name: str, value: float, lower: float, upper: float) -> float:
	number = _as_float(field_name, value)
	if not lower <= number <= upper:
		raise ValueError(f"{field_name} must be between {lower} and {upper}")
	return number


def _validate_positive(field_name: str, value: float) -> float:
	number = _as_float(field_name, value)
	if number <= 0:
		raise ValueError(f"{field_name} must be greater than 0")
	return number


@dataclass(frozen=True)
class ServiceConfig:
	"""Runtime configuration for the fixed geosearoute RapidAPI service."""

	base_url: str
	rapidapi_host: str
	rapidapi_key: str

	def __post_init__(self) -> None:
		if self.base_url != FIXED_BASE_URL:
			raise ValueError(f"base_url must equal {FIXED_BASE_URL}")
		object.__setattr__(self, "rapidapi_host", _require_non_blank("rapidapi_host", self.rapidapi_host))
		object.__setattr__(self, "rapidapi_key", _require_non_blank("rapidapi_key", self.rapidapi_key))


@dataclass(frozen=True)
class NearestQuery:
	"""Validated nearest-point lookup input."""

	latitude: float
	longitude: float
	distance_km: float = 500.0

	def __post_init__(self) -> None:
		object.__setattr__(self, "latitude", _validate_range("latitude", self.latitude, -90.0, 90.0))
		object.__setattr__(self, "longitude", _validate_range("longitude", self.longitude, -180.0, 180.0))
		object.__setattr__(self, "distance_km", _validate_positive("distance_km", self.distance_km))


@dataclass(frozen=True)
class StopCoordinate:
	"""Single ordered stop for solve requests."""

	longitude: float
	latitude: float
	index: int

	def __post_init__(self) -> None:
		object.__setattr__(self, "longitude", _validate_range("longitude", self.longitude, -180.0, 180.0))
		object.__setattr__(self, "latitude", _validate_range("latitude", self.latitude, -90.0, 90.0))
		if self.index < 0:
			raise ValueError("index must be greater than or equal to 0")


@dataclass(frozen=True)
class SolveQuery:
	"""Validated solve request input."""

	stops: Tuple[StopCoordinate, ...]
	speed_knots: float = 24.0

	def __post_init__(self) -> None:
		if len(self.stops) < 2:
			raise ValueError("stops must contain at least two entries")
		object.__setattr__(self, "stops", tuple(self.stops))
		object.__setattr__(self, "speed_knots", _validate_positive("speed_knots", self.speed_knots))


@dataclass(frozen=True)
class ServiceRequest:
	"""Normalized outbound request."""

	method: str
	path: str
	query_params: Dict[str, Any]
	json_body: Optional[Dict[str, Any]]
	headers: Dict[str, str]


@dataclass(frozen=True)
class ServiceResponse:
	"""Normalized service response."""

	status_code: Optional[int]
	payload: Optional[Any]
	raw_text: Optional[str]
	is_success: bool
	error_category: Optional[str]
